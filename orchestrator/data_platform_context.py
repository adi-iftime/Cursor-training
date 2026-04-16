"""
Shared context passed between orchestrator steps (extensible for LLM backends).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class WorkContext:
    """Carries correlation ID, user work order, and outputs from prior agents."""

    correlation_id: str
    repo_root: Path
    work_order: dict[str, Any]
    step_outputs: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    def record(self, agent_id: str, output: dict[str, Any]) -> None:
        self.step_outputs.setdefault(agent_id, []).append(output)

    def prior_summary(self) -> str:
        parts: list[str] = []
        for aid, outs in self.step_outputs.items():
            parts.append(f"{aid}:{len(outs)}")
        return "; ".join(parts) if parts else "none"


def default_work_order(user_request: str) -> dict[str, Any]:
    return {
        "intent": user_request.strip(),
        "risk_tier": "medium",
        "scope": "unspecified",
        "include_analyst": False,
    }
