"""Small, deterministic utilities; no experiment-dependent decision logic."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def derived_seed(seed, *parts):
    return int(digest([seed, *parts])[:8], 16) % (2**31)


def parse_object(text):
    """Accept an object or one enclosing Markdown fence; never repair semantics."""
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1])
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value


class Journal:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.stream = self.path.open("x", encoding="utf-8")
        self.previous = "0" * 64
        self.sequence = 0

    def emit(self, event, **fields):
        row = {"seq": self.sequence, "time_utc": datetime.now(timezone.utc).isoformat(),
               "event": event, "previous_hash": self.previous, **fields}
        row["event_hash"] = digest(row)
        self.stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        self.stream.flush()
        self.previous = row["event_hash"]
        self.sequence += 1
        return row

    def close(self):
        self.stream.close()


def read_journal(path):
    rows, previous = [], "0" * 64
    with Path(path).open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            row = json.loads(line)
            event_hash = row.pop("event_hash")
            if row.get("seq") != len(rows) or row.get("previous_hash") != previous or digest(row) != event_hash:
                raise ValueError("Journal integrity check failed at event %s" % len(rows))
            row["event_hash"] = event_hash
            rows.append(row)
            previous = event_hash
    return rows
