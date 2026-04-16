from __future__ import annotations

from typing import Any


class DataEngineer:
    id = "data_engineer"

    def task_handoff(self, *, story_key: str, content: str) -> dict[str, Any]:
        return {
            "from": self.id,
            "to": "tech_lead",
            "type": "task",
            "content": content,
            "jira_key": story_key,
            "context": {},
        }
