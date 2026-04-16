from __future__ import annotations

from typing import Any


class TesterAgent:
    id = "tester"

    def regression_note(self, *, story_key: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "from": self.id,
            "to": "tech_lead",
            "type": "approval" if passed else "block",
            "content": f"Regression: {'PASS' if passed else 'FAIL'} — {detail}",
            "jira_key": story_key,
            "context": {"passed": passed},
        }
