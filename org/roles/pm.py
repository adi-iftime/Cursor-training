from __future__ import annotations

from typing import Any


class ProductManager:
    id = "product_manager"

    def sprint_planning_message(self, *, epic_key: str, story_keys: list[str]) -> dict[str, Any]:
        return {
            "from": self.id,
            "to": "tech_lead",
            "type": "task",
            "content": f"Sprint planning: epic {epic_key}; stories {', '.join(story_keys)}. Prioritize backlog and align acceptance criteria.",
            "jira_key": epic_key,
            "context": {"story_keys": story_keys},
        }
