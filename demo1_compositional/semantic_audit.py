"""Semantic annotations are fallible evidence; never action correctness labels."""
from common import parse_object

CONDITION_STATES = {"preserved", "narrowed", "lost", "weakened", "claim_dropped", "uncertain"}
LOSS_STATES = {"lost", "weakened"}


def uncertain_audit(condition_ids, task_ids, reason):
    return {"condition_assessments": [
        {"condition_id": cid, "status": "uncertain", "original_evidence": "", "memory_evidence": "", "explanation": reason}
        for cid in condition_ids],
        "scope_expansion": {"status": "uncertain", "expansion_type": "uncertain", "original_evidence": "", "memory_evidence": "", "explanation": reason},
        "task_assessments": [{"task_id": tid, "mechanism_relevance": "uncertain", "relevant_condition_ids": [], "memory_evidence": "", "explanation": reason} for tid in task_ids]}


def validate_audit(value, originals, memory, condition_ids, task_ids):
    """Check schema and quoted evidence, NOT the semantic truth of the judge."""
    if isinstance(value, str):
        value = parse_object(value)
    original_text = "\n".join(exp["text"] for exp in originals)
    if not isinstance(value, dict):
        raise ValueError("Audit must be an object")
    conditions = value.get("condition_assessments", [])
    tasks = value.get("task_assessments", [])
    if len(conditions) != len(condition_ids) or {x.get("condition_id") for x in conditions} != set(condition_ids):
        raise ValueError("Condition coverage mismatch")
    if len(tasks) != len(task_ids) or {x.get("task_id") for x in tasks} != set(task_ids):
        raise ValueError("Probe coverage mismatch")

    def quote(item, key, source, required=False):
        text = item.get(key)
        if not isinstance(text, str) or (text and text not in source) or (required and not text):
            raise ValueError("Unverifiable evidence quote: " + key)

    for item in conditions:
        if item.get("status") not in CONDITION_STATES:
            raise ValueError("Unknown condition status")
        quote(item, "original_evidence", original_text, item["status"] != "uncertain")
        quote(item, "memory_evidence", memory, item["status"] in {"preserved", "narrowed", "lost", "weakened"})
    scope = value.get("scope_expansion", {})
    if scope.get("status") not in {"yes", "no", "uncertain"} or scope.get("expansion_type") not in {"condition_omission_or_relaxation", "unsupported_new_claim", "none", "uncertain"}:
        raise ValueError("Invalid scope label")
    if scope["status"] == "yes" and scope["expansion_type"] not in {"condition_omission_or_relaxation", "unsupported_new_claim"}:
        raise ValueError("Positive expansion requires a specific type")
    if scope["status"] == "no" and scope["expansion_type"] != "none":
        raise ValueError("No expansion must have type none")
    quote(scope, "original_evidence", original_text, scope["status"] == "yes")
    quote(scope, "memory_evidence", memory, scope["status"] == "yes")
    for item in tasks:
        if item.get("mechanism_relevance") not in {"related", "unrelated", "uncertain"}:
            raise ValueError("Invalid relevance label")
        ids = item.get("relevant_condition_ids")
        if not isinstance(ids, list) or not set(ids) <= set(condition_ids):
            raise ValueError("Invalid referenced conditions")
        quote(item, "memory_evidence", memory, item["mechanism_relevance"] == "related")
    return value


def classify_mechanism(raw_correct, summary_correct, annotation, task_id, decisions_valid=True):
    if not decisions_valid:
        return "invalid_or_missing_decision"
    if raw_correct is None:
        return "unpaired"
    conditions = annotation["condition_assessments"]
    loss_ids = {x["condition_id"] for x in conditions if x["status"] in LOSS_STATES}
    scope = annotation["scope_expansion"]
    probe = next(x for x in annotation["task_assessments"] if x["task_id"] == task_id)
    if summary_correct:
        if loss_ids or scope["status"] == "yes":
            return "information_loss_only"
        return "no_failure" if raw_correct else "summary_improvement"
    if not raw_correct:
        return "raw_baseline_failure"
    related_loss = bool(loss_ids & set(probe["relevant_condition_ids"]))
    related_expansion = scope["status"] == "yes" and scope["expansion_type"] == "condition_omission_or_relaxation"
    if probe["mechanism_relevance"] == "related" and (related_loss or related_expansion):
        return "mechanism_consistent_failure"
    fully_preserved = bool(conditions) and all(x["status"] == "preserved" for x in conditions)
    if fully_preserved and scope["status"] == "no":
        return "decision_stage_failure"
    if any(x["status"] == "uncertain" for x in conditions) or scope["status"] == "uncertain" or probe["mechanism_relevance"] == "uncertain":
        return "uncertain_attribution"
    return "other_memory_change_or_unrelated_failure"
