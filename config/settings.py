# DAG owner: planner (configuration surface) + devops (defaults for runnable deploy).
"""Shared repository configuration."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
