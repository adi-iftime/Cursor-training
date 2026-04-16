"""
Shared helpers for validating handoff payloads and config references.
Keep dependencies minimal; safe to import in agent runtimes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


def load_json(path: str | Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def require_keys(obj: Mapping[str, Any], keys: tuple[str, ...], *, context: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValueError(f"{context}: missing keys {missing}")


def attach_correlation_id(payload: dict[str, Any], correlation_id: str) -> dict[str, Any]:
    out = dict(payload)
    out["correlation_id"] = correlation_id
    return out
