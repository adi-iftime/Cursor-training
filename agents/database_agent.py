"""
Database Agent — SQLite schema, users, scores with timestamps.

Implementation modules: `database/models.py`, `database/db.py`.
"""

from __future__ import annotations

from pathlib import Path

from config.settings import DATABASE_PATH
from database.db import Database, get_connection, init_schema

__all__ = ["Database", "get_connection", "init_schema", "default_database_path"]


def default_database_path() -> Path:
    return DATABASE_PATH
