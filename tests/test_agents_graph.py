"""Validate agents.json graph references only registered agent ids."""

from __future__ import annotations

import json
from pathlib import Path

import pytest


def test_agents_outputs_and_dependencies_reference_known_ids(repo_root: Path) -> None:
    path = repo_root / "config" / "agents.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    agents = data["agents"]
    ids = {a["id"] for a in agents}

    for agent in agents:
        aid = agent["id"]
        for dep in agent.get("dependsOn", []):
            assert dep in ids, f"{aid}.dependsOn references unknown id: {dep}"
        for target in agent.get("outputsTo", []):
            assert target in ids, f"{aid}.outputsTo references unknown id: {target}"
