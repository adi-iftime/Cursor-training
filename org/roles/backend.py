from __future__ import annotations

from typing import Any


class BackendEngineer:
    id = "backend_engineer"

    def implementation_update(self, *, story_key: str, branch: str, paths: list[str]) -> dict[str, Any]:
        return {
            "from": self.id,
            "to": "reviewer",
            "type": "task",
            "content": f"Implementation ready on branch {branch}; paths: {', '.join(paths)}. Requesting review.",
            "jira_key": story_key,
            "context": {"branch": branch, "paths": paths},
        }

    def question(self, *, story_key: str, to: str, text: str) -> dict[str, Any]:
        return {
            "from": self.id,
            "to": to,
            "type": "question",
            "content": text,
            "jira_key": story_key,
            "context": {},
        }
