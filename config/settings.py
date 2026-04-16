# DAG owner: planner (configuration surface) + devops (defaults for runnable deploy).
"""Shared configuration for the terminal Snake application."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
DATABASE_PATH = DATA_DIR / "snake.db"

GRID_WIDTH = 28
GRID_HEIGHT = 18
POINTS_PER_FOOD = 10
MAX_USERNAME_LEN = 64
