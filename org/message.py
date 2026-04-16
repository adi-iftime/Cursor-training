from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

MESSAGE_TYPES = frozenset({"task", "review", "question", "approval", "block"})


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def validate_message(msg: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize a structured agent message."""
    missing = [k for k in ("from", "to", "type", "content") if not msg.get(k)]
    if missing:
        raise ValueError(f"message missing required keys: {missing}")
    mtype = str(msg["type"])
    if mtype not in MESSAGE_TYPES:
        raise ValueError(f"invalid type {mtype!r}; expected one of {sorted(MESSAGE_TYPES)}")
    out: dict[str, Any] = {
        "from": str(msg["from"]),
        "to": str(msg["to"]),
        "type": mtype,
        "content": str(msg["content"]),
        "jira_key": str(msg.get("jira_key") or ""),
        "context": dict(msg.get("context") or {}),
    }
    ts = msg.get("timestamp")
    out["timestamp"] = str(ts) if ts else utc_now_iso()
    return out
