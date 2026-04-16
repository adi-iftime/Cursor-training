from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from org.message import validate_message

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_COMM_PATH = REPO_ROOT / "logs" / "communication.json"


def append_message(msg: dict[str, Any], *, path: Path | None = None) -> dict[str, Any]:
    """Append a validated message to the JSON array log (atomic write)."""
    comm_path = path or DEFAULT_COMM_PATH
    comm_path.parent.mkdir(parents=True, exist_ok=True)
    validated = validate_message(msg)
    existing: list[Any] = []
    if comm_path.exists():
        raw = comm_path.read_text(encoding="utf-8").strip()
        if raw:
            existing = json.loads(raw)
            if not isinstance(existing, list):
                raise ValueError(f"{comm_path} must contain a JSON array")
    existing.append(validated)
    tmp = comm_path.with_suffix(comm_path.suffix + ".tmp")
    tmp.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(comm_path)
    return validated


def read_messages(*, path: Path | None = None) -> list[dict[str, Any]]:
    comm_path = path or DEFAULT_COMM_PATH
    if not comm_path.exists():
        return []
    raw = comm_path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError(f"{comm_path} must contain a JSON array")
    return data
