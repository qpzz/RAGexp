"""Engineering tests only. Scripted replies below are never research results."""
import copy
import json
import os
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from adapters import Adapter, ChatCompletionsAdapter
from common import read_journal
from evaluate import evaluate_run, export_review
from run_experiment import ROOT, execute, load_config, planned_counts
from scenarios import (GROUPS, action_for_facts, expected_action, generate_scenarios,
                       is_target_trigger, selected_experiences, validate_scenario)
from semantic_audit import classify_mechanism, uncertain_audit, validate_audit


def configuration():
    config = load_config(ROOT / "configs/compositional.json")
    config["n_scenarios"], config["repeats"] = 2, 2
    config["predeclared_analysis"]["bootstrap_samples"] = 50
    return config


def annotation(status="preserved", scope="no", relevant="unrelated"):
    return {"condition_assessments": [
        {"condition_id": "amount_limit", "status": status, "original_evidence": "amount <= 5", "memory_evidence": "waiver rule", "explanation": "unit fixture"}],
        "scope_expansion": {"status": scope, "expansion_type": "none" if scope == "no" else "condition_omission_or_relaxation", "original_evidence": "amount <= 5", "memory_evidence": "waiver rule", "explanation": "unit fixture"},
        "task_assessments": [{"task_id": "T11", "mechanism_relevance": relevant, "relevant_condition_ids": ["amount_limit"], "memory_evidence": "waiver rule", "explanation": "unit fixture"}]}


class ScriptedEngineeringAdapter(Adapter):
    """A test double, outside production adapter registration; never claims LLM inference."""
    def __init__(self):
        self.requests = []

    def build_request(self, messages, seed, phase):
        return {"messages": messages, "seed": seed, "engineering_test_phase": phase}

    def complete(self, request):
        self.requests.append(request)
        data = json.loads(request["messages"][1]["content"])
        phase = request["engineering_test_phase"]
        if phase == "consolidation":
            # Faithful echo tests plumbing; this is NOT a normal-consolidation experiment.
            value = {"memory": "\n".join(x["text"] for x in data["experiences"])}
        elif phase == "decision":
            # Fixed, deliberately uninformative action. No fixture truth or group label is inspected.
            value = {"action": "manual_review", "rationale": "Scripted engineering test only", "used_memory_ids": []}
        else:
            value = uncertain_audit(data["condition_ids"], [p["task_id"] for p in data["probes"]], "Scripted test; no semantic inference")
        return {"text": json.dumps(value), "raw_response": {"test_fixture": value}, "finish_reason": "stop", "elapsed_seconds": 0}


class ScenarioTests(unittest.TestCase):
    def setUp(self):
        self.config = configuration()
        self.scenario = generate_scenarios(self.config)[0]

    def test_frozen_generator_and_truthful_inputs(self):
        first = generate_scenarios(self.config)
        self.assertEqual(first, generate_scenarios(self.config))
        for scenario in first:
            validate_scenario(scenario)
            self.assertFalse(scenario["attacker_target"]["search_or_optimization"])

    def test_untested_compositions_fail_explicitly(self):
        for kind in ["multiple_locally_scoped_rules", "chained_experience"]:
            config = {**self.config, "composition_types": [kind]}
            with self.assertRaises(NotImplementedError):
                generate_scenarios(config)

    def test_full_evidence_truth_table(self):
        for group in ["G0", "G3", "G4", "G6"]:
            for task in self.scenario["tasks"]:
                expected = "waive_review" if task["id"] == "T00" else "manual_review"
                self.assertEqual(expected_action(self.scenario, group, task), expected)

    def test_incomplete_evidence_defaults_to_review(self):
        for group in ["G1", "G2", "G5"]:
            for task in self.scenario["tasks"]:
                self.assertEqual(expected_action(self.scenario, group, task), "manual_review")

    def test_inclusive_boundaries_and_after_expiry(self):
        truth = self.scenario["truth"]
        task = {**self.scenario["tasks"][0], "amount_cents": truth["refund_rule"]["max_amount_cents"], "request_date": truth["membership"]["valid_until"]}
        self.assertEqual(action_for_facts(truth, task), "waive_review")
        self.assertEqual(action_for_facts(truth, {**task, "amount_cents": task["amount_cents"] + 1}), "manual_review")
        task["request_date"] = "%d-01-01" % (int(task["request_date"][:4]) + 1)
        self.assertEqual(action_for_facts(truth, task), "manual_review")

    def test_exact_trigger_and_nontrigger_partition(self):
        self.assertEqual([t["id"] for t in self.scenario["tasks"] if is_target_trigger(self.scenario, t)], ["T11"])

    def test_false_experience_rejected(self):
        bad = copy.deepcopy(self.scenario)
        bad["experiences"][0]["semantic_facts"]["refund_rule"] = {"max_amount_cents": -1}
        with self.assertRaises(ValueError):
            validate_scenario(bad)


class AttributionTests(unittest.TestCase):
    def test_mechanism_requires_raw_correct_summary_wrong_and_related_damage(self):
        ann = annotation("lost", "yes", "related")
        self.assertEqual(classify_mechanism(True, False, ann, "T11"), "mechanism_consistent_failure")
        self.assertEqual(classify_mechanism(False, False, ann, "T11"), "raw_baseline_failure")
        self.assertEqual(classify_mechanism(True, True, ann, "T11"), "information_loss_only")

    def test_preserved_conditions_mean_decision_stage_failure(self):
        self.assertEqual(classify_mechanism(True, False, annotation(), "T11"), "decision_stage_failure")

    def test_unrelated_condition_loss_not_counted(self):
        self.assertNotEqual(classify_mechanism(True, False, annotation("lost", "no", "unrelated"), "T11"), "mechanism_consistent_failure")

    def test_whole_claim_dropped_is_not_condition_loss_success(self):
        self.assertEqual(classify_mechanism(True, False, annotation("claim_dropped"), "T11"), "other_memory_change_or_unrelated_failure")

    def test_unknown_annotations_stay_uncertain(self):
        ann = uncertain_audit(["amount_limit"], ["T11"], "no evidence")
        self.assertEqual(classify_mechanism(True, False, ann, "T11"), "uncertain_attribution")

    def test_invalid_action_not_mechanism_success(self):
        self.assertEqual(classify_mechanism(True, False, annotation("lost", "yes", "related"), "T11", False), "invalid_or_missing_decision")

    def test_invented_audit_quote_rejected(self):
        ann = annotation("lost", "yes", "related")
        with self.assertRaises(ValueError):
            validate_audit(ann, [{"text": "amount <= 5"}], "a completely different memory", ["amount_limit"], ["T11"])


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.config = configuration()
        self.config_path = self.directory / "config.json"
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def run_fixture(self):
        adapter = ScriptedEngineeringAdapter()
        path, status = execute(self.config_path, self.directory / "fixture.jsonl", injected_adapter=adapter, run_kind="test_fixture")
        self.assertEqual(status, "complete")
        return path, adapter

    def test_complete_pipeline_all_arms_and_no_information_leak(self):
        path, adapter = self.run_fixture()
        report, attrs, audits, manifest = evaluate_run(path)
        self.assertTrue(report["complete"])
        self.assertEqual(len(report["metrics"]), 9)
        self.assertEqual(len(adapter.requests), 192)
        self.assertEqual(report["conclusion"]["stage_1"], "NOT_A_LIVE_EXPERIMENT")
        for request in adapter.requests:
            visible = json.dumps(request["messages"])
            for forbidden in ["attacker_target", "semantic_facts", '"group"', "expected_action", "target_action"]:
                self.assertNotIn(forbidden, visible)
        for row in report["metrics"]:
            self.assertEqual(row["asr"], 0)
            if row["arm"].startswith(("G0/", "G3/", "G4/", "G6/")):
                self.assertEqual(row["accuracy_all"], .75)
                self.assertEqual(row["eligible_waiver_accuracy"], 0)
        # The fixed manual-review test double therefore cannot look like a useful defense.
        self.assertTrue(all(row["classification"] != "mechanism_consistent_failure" for row in attrs))
        self.assertEqual(len(audits), 24)

    def test_cannot_label_injected_adapter_as_live(self):
        with self.assertRaises(ValueError):
            execute(self.config_path, self.directory / "bad.jsonl", injected_adapter=ScriptedEngineeringAdapter())

    def test_human_semantic_changes_do_not_change_action_metrics(self):
        path, adapter = self.run_fixture()
        report, _, audits, manifest = evaluate_run(path)
        review_path = self.directory / "reviews.jsonl"
        export_review(review_path, audits, manifest)
        reviews = [json.loads(line) for line in review_path.read_text(encoding="utf-8").splitlines()]
        for row in reviews:
            row.update(reviewed=True, reviewer="engineering-test", reason="Check immutable deterministic scores")
            # Retain uncertainty; the annotation interface must never touch action correctness.
        review_path.write_text("\n".join(json.dumps(row) for row in reviews), encoding="utf-8")
        revised, _, _, _ = evaluate_run(path, review_path)
        for before, after in zip(report["metrics"], revised["metrics"]):
            for metric in ["asr", "accuracy_all", "clean_task_accuracy", "eligible_waiver_accuracy", "trigger_specificity"]:
                self.assertEqual(before[metric], after[metric])
        reviews[0]["final_action"] = "waive_review"
        review_path.write_text("\n".join(json.dumps(row) for row in reviews), encoding="utf-8")
        with self.assertRaises(ValueError):
            evaluate_run(path, review_path)

    def test_journal_modification_is_detected(self):
        path, adapter = self.run_fixture()
        lines = path.read_text(encoding="utf-8").splitlines()
        row = json.loads(lines[2])
        row["unrecorded_change"] = True
        lines[2] = json.dumps(row)
        path.write_text("\n".join(lines), encoding="utf-8")
        with self.assertRaises(ValueError):
            evaluate_run(path)

    def test_prepare_only_makes_no_llm_calls_or_empirical_claims(self):
        path, status = execute(self.config_path, self.directory / "plan.jsonl", prepare_only=True)
        self.assertEqual(status, "prepared_only")
        report, _, _, _ = evaluate_run(path)
        self.assertEqual(report["metrics"], [])
        self.assertEqual(report["run_kind"], "design_only")

    def test_budget_checked_before_api_calls(self):
        self.config["max_calls"] = 1
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")
        with self.assertRaises(ValueError):
            execute(self.config_path, self.directory / "budget.jsonl", injected_adapter=ScriptedEngineeringAdapter(), run_kind="test_fixture")

    def test_first_api_failure_aborts_and_is_recorded(self):
        class Broken(ScriptedEngineeringAdapter):
            def complete(self, request):
                raise RuntimeError("test service unavailable")
        path, status = execute(self.config_path, self.directory / "failed.jsonl", injected_adapter=Broken(), run_kind="test_fixture")
        self.assertEqual(status, "aborted")
        events = read_journal(path)
        self.assertEqual(sum(e["event"] == "llm_request" for e in events), 1)
        self.assertTrue(any(e["event"] == "llm_error" for e in events))


class AdapterTests(unittest.TestCase):
    def test_missing_credentials_do_not_fall_back_to_mock(self):
        config = configuration()["adapter"]
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                ChatCompletionsAdapter(config)

    def test_seed_optional_and_secret_not_in_payload_or_metadata(self):
        config = configuration()["adapter"]
        environment = {config["base_url_env"]: "https://example.invalid/v1", config["model_env"]: "user-supplied-id", config["api_key_env"]: "TEST_SECRET_NOT_A_REAL_KEY"}
        with patch.dict(os.environ, environment, clear=True):
            adapter = ChatCompletionsAdapter(config)
            payload = adapter.build_request([], 123, "decision")
            self.assertNotIn("seed", payload)
            self.assertNotIn(environment[config["api_key_env"]], json.dumps([payload, adapter.metadata()]))
            config["send_seed"] = True
            self.assertEqual(ChatCompletionsAdapter(config).build_request([], 123, "decision")["seed"], 123)


if __name__ == "__main__":
    unittest.main()
