from __future__ import annotations

from typing import Any


class DevOpsEngineer:
    id = "devops_engineer"

    def stability_check(self, *, story_key: str, ok: bool, detail: str) -> dict[str, Any]:
        return {
            "from": self.id,
            "to": "tech_lead",
            "type": "approval" if ok else "block",
            "content": f"Stability gate: {'OK' if ok else 'NOT OK'} — {detail}",
            "jira_key": story_key,
            "context": {"ok": ok},
        }
