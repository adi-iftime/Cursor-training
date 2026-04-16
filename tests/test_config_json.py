"""Ensure config JSON files parse (regression for invalid JSON drift)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "relative_path",
    [
        "config/agents.json",
        "config/orchestration.json",
        "config/guardrails.json",
        "config/skills.json",
    ],
)
def test_config_files_parse(repo_root: Path, relative_path: str) -> None:
    path = repo_root / relative_path
    text = path.read_text(encoding="utf-8")
    json.loads(text)
