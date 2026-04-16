"""
Tracks PR lifecycle state: cycles, issues, fixes, decisions.

Persists JSON under `state/storage/` to survive process restarts.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class PRStateRecord:
    pr_key: str
    owner: str
    repo: str
    number: int
    cycles: int = 0
    issues_found: list[dict[str, Any]] = field(default_factory=list)
    fixes_applied: list[dict[str, Any]] = field(default_factory=list)
    status: str = "open"
    final_decision: str | None = None
    last_review_summary: str | None = None
    last_rereview_verdict: str | None = None
    updated_at: str = field(default_factory=_utc_now_iso)
    history: list[dict[str, Any]] = field(default_factory=list)

    def touch(self) -> None:
        self.updated_at = _utc_now_iso()

    def append_event(self, event: str, payload: dict[str, Any]) -> None:
        self.history.append({"ts": _utc_now_iso(), "event": event, "payload": payload})
        self.touch()


class PRStateTracker:
    """JSON-backed state store keyed by owner/repo/number."""

    def __init__(self, storage_dir: str | Path | None = None) -> None:
        root = Path(__file__).resolve().parent
        self.storage_dir = Path(storage_dir) if storage_dir else root / "storage"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, pr_key: str) -> Path:
        safe = pr_key.replace("/", "_").replace(":", "_")
        return self.storage_dir / f"{safe}.json"

    @staticmethod
    def make_key(owner: str, repo: str, number: int) -> str:
        return f"{owner}/{repo}#{number}"

    def load(self, owner: str, repo: str, number: int) -> PRStateRecord:
        key = self.make_key(owner, repo, number)
        path = self._path(key)
        if not path.exists():
            rec = PRStateRecord(pr_key=key, owner=owner, repo=repo, number=number)
            self.save(rec)
            return rec
        data = json.loads(path.read_text(encoding="utf-8"))
        return PRStateRecord(**{k: v for k, v in data.items() if k in PRStateRecord.__dataclass_fields__})

    def save(self, record: PRStateRecord) -> None:
        record.touch()
        path = self._path(record.pr_key)
        path.write_text(json.dumps(asdict(record), indent=2), encoding="utf-8")

    def increment_cycle(self, owner: str, repo: str, number: int) -> PRStateRecord:
        rec = self.load(owner, repo, number)
        rec.cycles += 1
        rec.append_event("cycle_increment", {"cycles": rec.cycles})
        self.save(rec)
        return rec

    def set_issues(self, owner: str, repo: str, number: int, issues: list[dict[str, Any]]) -> PRStateRecord:
        rec = self.load(owner, repo, number)
        rec.issues_found = issues
        rec.append_event("issues_updated", {"count": len(issues)})
        self.save(rec)
        return rec

    def add_fix(self, owner: str, repo: str, number: int, fix: dict[str, Any]) -> PRStateRecord:
        rec = self.load(owner, repo, number)
        rec.fixes_applied.append(fix)
        rec.append_event("fix_applied", fix)
        self.save(rec)
        return rec

    def set_status(self, owner: str, repo: str, number: int, status: str) -> PRStateRecord:
        rec = self.load(owner, repo, number)
        rec.status = status
        rec.append_event("status", {"status": status})
        self.save(rec)
        return rec

    def set_final_decision(self, owner: str, repo: str, number: int, decision: str) -> PRStateRecord:
        rec = self.load(owner, repo, number)
        rec.final_decision = decision
        rec.append_event("final_decision", {"decision": decision})
        self.save(rec)
        return rec
