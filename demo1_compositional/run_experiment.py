"""Run a frozen Stage-1 experiment; semantic audit never grades actions."""
import argparse
import json
import platform
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from adapters import ChatCompletionsAdapter
from common import Journal, derived_seed, digest
from pipeline import Caller, consolidate, decide, messages
from scenarios import (GENERATOR_VERSION, GROUPS, generate_scenarios, public_experiences,
                       public_task, selected_experiences)
from semantic_audit import uncertain_audit, validate_audit

ROOT = Path(__file__).resolve().parent


def load_config(path):
    config = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if config.get("stage") != 1:
        raise ValueError("Only Stage 1 is implemented")
    for key in ["seed", "n_scenarios", "repeats", "max_calls"]:
        if type(config.get(key)) is not int or (key != "seed" and config[key] < 1):
            raise ValueError("Invalid integer configuration: " + key)
    groups = config.get("groups")
    if not isinstance(groups, list) or not groups or len(set(groups)) != len(groups) or any(g not in GROUPS for g in groups):
        raise ValueError("Invalid groups")
    if config.get("experience_order") not in {"fixed", "counterbalanced"}:
        raise ValueError("Invalid experience_order")
    if config["adapter"].get("type") != "chat_completions":
        raise ValueError("Register a real Adapter implementation before selecting it")
    for group in groups:
        pair = GROUPS[group]["pair"]
        if pair and pair[0] not in groups:
            raise ValueError("Missing paired raw group for " + group)
    return config


def planned_counts(config, scenarios):
    decisions = sum(len(s["tasks"]) for s in scenarios) * config["repeats"] * sum(len(GROUPS[g]["variants"]) for g in config["groups"])
    summaries = len(scenarios) * config["repeats"] * sum("summary" in GROUPS[g]["variants"] for g in config["groups"])
    audits = summaries if config["semantic_audit"] else 0
    return {"decisions": decisions, "summaries": summaries, "audits": audits, "max_llm_calls": decisions + summaries + audits}


def execute(config_path, output=None, prepare_only=False, injected_adapter=None, run_kind="live"):
    config = load_config(config_path)
    scenarios = generate_scenarios(config)
    counts = planned_counts(config, scenarios)
    if counts["max_llm_calls"] > config["max_calls"]:
        raise ValueError("Frozen plan needs %d calls, exceeding max_calls=%d; no calls made" % (counts["max_llm_calls"], config["max_calls"]))
    if injected_adapter is not None and run_kind != "test_fixture":
        raise ValueError("Injected adapters are restricted to explicitly labelled test_fixture runs")
    prompts = {path.stem: path.read_text(encoding="utf-8") for path in sorted((ROOT / "prompts").glob("*.txt"))}
    sources = {path.name: path.read_text(encoding="utf-8") for path in sorted(ROOT.glob("*.py"))}
    adapter = None if prepare_only else injected_adapter or ChatCompletionsAdapter(config["adapter"])
    frozen = {"config": config, "scenarios": scenarios, "prompts": prompts,
              "group_definitions": GROUPS, "generator_version": GENERATOR_VERSION,
              "source_snapshot": sources, "adapter_resolved": None if adapter is None else adapter.metadata()}
    freeze_hash = digest(frozen)
    if output is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        kind = "plan" if prepare_only else run_kind
        output = ROOT / config["results_dir"] / ("%s_%s_%s.jsonl" % (kind, stamp, freeze_hash[:8]))
    journal = Journal(output)
    caller = None
    completed, failure = False, None
    try:
        journal.emit("manifest", run_kind="design_only" if prepare_only else run_kind, stage=1,
                     freeze_hash=freeze_hash, frozen=frozen, planned_counts=counts,
                     adapter=None if adapter is None else adapter.metadata(),
                     runtime={"python": sys.version, "platform": platform.platform()},
                     declaration="Stage 1 phenomenon test. No attack optimization; no Stage 2 conclusion.")
        if prepare_only:
            journal.emit("run_end", status="prepared_only", llm_calls=0)
            return Path(output), "prepared_only"
        caller = Caller(adapter, journal, config["max_calls"])
        audit_queue = []
        for scenario in scenarios:
            for repeat in range(config["repeats"]):
                rng = random.Random(derived_seed(config["seed"], scenario["id"], repeat, "execution_order"))
                groups = list(config["groups"])
                rng.shuffle(groups)
                # A/B ordering is the same across raw, normal-summary and preserving-summary arms.
                reverse = config["experience_order"] == "counterbalanced" and (int(scenario["id"].split("_")[-1]) + repeat) % 2 == 1
                for group in groups:
                    spec = GROUPS[group]
                    originals = selected_experiences(scenario, group)
                    if reverse:
                        originals = list(reversed(originals))
                    raw_memory = public_experiences(originals)
                    base = {"scenario_id": scenario["id"], "repeat": repeat, "group": group}
                    journal.emit("episode", context=base, experience_order="reversed" if reverse else "forward",
                                 original_experiences=originals, original_memory=raw_memory)
                    variant_memories = {"raw": {"status": "ok", "records": raw_memory}}
                    if "summary" in spec["variants"]:
                        prompt = prompts["consolidate_preserve" if spec["summary_mode"] == "preserve" else "consolidate_normal"]
                        summary = consolidate(caller, prompt, raw_memory,
                                              derived_seed(config["seed"], scenario["id"], repeat, "consolidation"), base)
                        variant_memories["summary"] = summary
                        audit_queue.append((scenario, repeat, group, originals, summary))
                    variants = list(spec["variants"])
                    rng.shuffle(variants)
                    for variant in variants:
                        memory = variant_memories[variant]
                        tasks = list(scenario["tasks"])
                        rng.shuffle(tasks)
                        for task in tasks:
                            context = {**base, "variant": variant, "task_id": task["id"]}
                            if memory["status"] != "ok":
                                journal.emit("decision", context=context, status="upstream_memory_error", call_id=None,
                                             task=public_task(task), retrieved_memory=[], memory_hash=None,
                                             final_action=None, visible_rationale=None, used_memory_ids=[],
                                             tool_result={"executed": False, "action": None}, raw_response="")
                                continue
                            decide(caller, prompts["decision"], public_task(task), memory["records"],
                                   derived_seed(config["seed"], scenario["id"], repeat, task["id"], "decision"), context)
        # All acting decisions finish before any semantic audit. Outcomes are never audit inputs.
        for scenario, repeat, group, originals, summary in audit_queue:
            context = {"scenario_id": scenario["id"], "repeat": repeat, "group": group}
            condition_ids = sorted({cid for exp in originals for cid in exp["condition_ids"]})
            task_ids = [task["id"] for task in scenario["tasks"]]
            annotation = uncertain_audit(condition_ids, task_ids, "Audit disabled or memory unavailable")
            status, audit_call = "not_available", None
            if summary["status"] == "ok" and config["semantic_audit"]:
                data = {"original_experiences": public_experiences(originals), "consolidated_memory": summary["text"],
                        "condition_ids": condition_ids,
                        "probes": [{"task_id": t["id"], **public_task(t)} for t in scenario["tasks"]]}
                response = caller.call(messages(prompts["audit"], data),
                                       derived_seed(config["seed"], scenario["id"], repeat, "audit"), "semantic_audit", context)
                audit_call = response["call_id"]
                try:
                    if response["status"] != "ok":
                        raise ValueError("Truncated audit")
                    annotation = validate_audit(response["text"], originals, summary["text"], condition_ids, task_ids)
                    status = "validated_quotes_not_semantic_truth"
                except (ValueError, TypeError, KeyError, AttributeError) as exc:
                    annotation = uncertain_audit(condition_ids, task_ids, str(exc))
                    status = "invalid_audit"
            journal.emit("semantic_audit", context=context,
                         audit_key="%s:%d:%s" % (scenario["id"], repeat, group),
                         memory_hash=digest(summary["records"]), condition_ids=condition_ids,
                         annotation=annotation, status=status, audit_call_id=audit_call,
                         attribution_status="llm_unreviewed", original_experiences=originals,
                         consolidated_memory=summary["text"])
        completed = True
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)}
        journal.emit("run_error", **failure)
    finally:
        if not prepare_only:
            journal.emit("run_end", status="complete" if completed else "aborted", llm_calls=0 if caller is None else caller.calls, error=failure)
        journal.close()
    return Path(output), "complete" if completed else "aborted"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output")
    parser.add_argument("--prepare-only", action="store_true", help="Freeze inputs without calling any model; NOT an experiment result")
    args = parser.parse_args()
    try:
        path, status = execute(args.config, args.output, args.prepare_only)
    except (ValueError, NotImplementedError, OSError) as exc:
        parser.exit(2, "Configuration error: %s\n" % exc)
    print("Run: %s\nStatus: %s" % (path, status))
    if status == "aborted":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
