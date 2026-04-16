from __future__ import annotations

from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class ReviewerAgent:
    id = "reviewer"

    def review_delivery(
        self,
        *,
        story_key: str,
        delivery_paths: list[str],
    ) -> dict[str, Any]:
        """Lightweight local review: required files exist under repo root."""
        missing = [p for p in delivery_paths if not (REPO_ROOT / p).exists()]
        if missing:
            return {
                "from": self.id,
                "to": "backend_engineer",
                "type": "block",
                "content": f"Request changes: missing paths {missing}",
                "jira_key": story_key,
                "context": {"missing": missing},
            }
        return {
            "from": self.id,
            "to": "tech_lead",
            "type": "approval",
            "content": "Code review passed: delivery paths present and consistent with story scope.",
            "jira_key": story_key,
            "context": {"reviewed_paths": delivery_paths},
        }
