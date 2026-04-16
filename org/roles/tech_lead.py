from __future__ import annotations

from typing import Any


class TechLead:
    id = "tech_lead"

    def assign_story(
        self,
        *,
        story_key: str,
        engineer_role: str,
        file_paths: list[str],
    ) -> dict[str, Any]:
        return {
            "from": self.id,
            "to": engineer_role,
            "type": "task",
            "content": f"Implement story {story_key}. Touch only agreed paths; follow architecture in org_state.",
            "jira_key": story_key,
            "context": {"file_paths": file_paths, "engineer": engineer_role},
        }
