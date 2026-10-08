"""LLM-generated memory and decisions. No scenario oracle is imported here."""
import json
from common import digest, parse_object


class CallBudgetExceeded(RuntimeError):
    pass


class APIAbort(RuntimeError):
    pass


class Caller:
    def __init__(self, adapter, journal, max_calls):
        self.adapter, self.journal, self.max_calls = adapter, journal, max_calls
        self.calls = 0

    def call(self, messages, seed, phase, context):
        if self.calls >= self.max_calls:
            raise CallBudgetExceeded("Predeclared call budget exhausted; no automatic increase")
        request = self.adapter.build_request(messages, seed, phase)
        call_id = "call_%06d" % self.calls
        self.calls += 1
        self.journal.emit("llm_request", call_id=call_id, phase=phase, context=context,
                          requested_seed=seed, request_hash=digest(request), request=request)
        try:
            result = self.adapter.complete(request)
            self.journal.emit("llm_response", call_id=call_id, phase=phase, context=context, **result)
            truncated = result.get("finish_reason") in {"length", "max_tokens"}
            return {"call_id": call_id, "status": "truncated" if truncated else "ok", **result}
        except Exception as exc:
            self.journal.emit("llm_error", call_id=call_id, phase=phase, context=context,
                              error_type=type(exc).__name__, error=str(exc),
                              raw_response=getattr(exc, "raw", None), http_status=getattr(exc, "status", None))
            raise APIAbort("API call failed; the frozen run is aborted, not retried or silently changed") from exc


def messages(system, data):
    return [{"role": "system", "content": system},
            {"role": "user", "content": json.dumps(data, ensure_ascii=False)}]


def consolidate(caller, prompt, original_memory, seed, context):
    result = caller.call(messages(prompt, {"experiences": original_memory}), seed, "consolidation", context)
    text, records, status = None, [], result["status"]
    if status == "ok":
        try:
            obj = parse_object(result["text"])
            text = obj["memory"]
            if not isinstance(text, str):
                raise ValueError("memory must be text")
            # Preserve verbatim generated text, including an empty memory.
            records = [{"record_id": "memory_0", "text": text}] if text else []
        except (KeyError, TypeError, ValueError) as exc:
            status = "parse_error"
            caller.journal.emit("parse_error", phase="consolidation", context=context, error=str(exc))
    caller.journal.emit("memory", context=context, status=status, call_id=result["call_id"],
                        original_memory=original_memory, consolidated_memory=text,
                        memory_after=records, memory_hash=digest(records),
                        raw_consolidation_response=result.get("text", ""))
    return {"status": status, "records": records, "text": text, "call_id": result["call_id"]}


def decide(caller, prompt, task, retrieved_memory, seed, context):
    caller.journal.emit("retrieval", context=context, strategy="all_records_in_current_episode",
                        retrieved_memory=retrieved_memory, memory_hash=digest(retrieved_memory))
    result = caller.call(messages(prompt, {"task": task, "memory": retrieved_memory}), seed, "decision", context)
    action, rationale, used, status = None, None, [], result["status"]
    if status == "ok":
        try:
            obj = parse_object(result["text"])
            action, rationale, used = obj["action"], obj["rationale"], obj.get("used_memory_ids", [])
            if action not in {"manual_review", "waive_review"} or not isinstance(rationale, str):
                raise ValueError("Invalid action or visible rationale")
            if not isinstance(used, list) or any(not isinstance(x, str) for x in used):
                raise ValueError("used_memory_ids must be a list of strings")
            if not set(used) <= {r["record_id"] for r in retrieved_memory}:
                raise ValueError("Unknown memory ID in decision")
        except (KeyError, TypeError, ValueError) as exc:
            status, action = "parse_error", None
            caller.journal.emit("parse_error", phase="decision", context=context, error=str(exc))
    if status != "ok":
        action = None
    # Simulated tool accepts the valid LLM choice; it never knows the correct answer.
    tool_result = {"executed": action is not None, "action": action}
    caller.journal.emit("decision", context=context, status=status, call_id=result["call_id"],
                        task=task, retrieved_memory=retrieved_memory, memory_hash=digest(retrieved_memory),
                        final_action=action, visible_rationale=rationale, used_memory_ids=used,
                        tool_result=tool_result, raw_response=result.get("text", ""))
