from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE_PATH = REPO_ROOT / "state" / "org_state.json"


def default_state() -> dict[str, Any]:
    return {
        "version": 1,
        "sprint": {
            "id": "sprint-1",
            "name": "[Sim] AI Engineering Organization — Sprint 1",
            "status": "planning",
            "jira_epic_key": "SCRUM-3",
        },
        "jira_tickets": {
            "SCRUM-3": {
                "type": "Epic",
                "summary": "[Sim] AI Engineering Organization — Sprint 1",
                "status": "To Do",
            },
            "SCRUM-4": {
                "type": "Story",
                "summary": "[Sim] Implement org simulator package + comms log",
                "status": "To Do",
                "parent": "SCRUM-3",
                "assignee_role": "backend_engineer",
                "file_paths": [
                    "org/",
                    "logs/communication.json",
                    "state/org_state.json",
                ],
            },
        },
        "agent_assignments": {"SCRUM-4": "backend_engineer"},
        "prs": {},
        "blocking_issues": [],
        "communication_log_path": "logs/communication.json",
        "sprint_progress": {"total_stories": 1, "done": 0},
    }


def load_state(*, path: Path | None = None) -> dict[str, Any]:
    p = path or DEFAULT_STATE_PATH
    if not p.exists():
        st = default_state()
        save_state(st, path=p)
        return st
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("org_state must be a JSON object")
    return data


def save_state(state: dict[str, Any], *, path: Path | None = None) -> None:
    p = path or DEFAULT_STATE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(p)
