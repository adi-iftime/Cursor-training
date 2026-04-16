# DAG owner: data_analyst — read-only ranking and per-user analytics.
"""Leaderboard and user score surfaces (no writes)."""

from __future__ import annotations

from database.db import Database
from database.models import LeaderboardRow, ScoreRecord


def global_leaderboard(db: Database, limit: int = 50) -> list[LeaderboardRow]:
    return db.leaderboard_top(limit=limit)


def user_score_history(db: Database, user_id: int) -> list[ScoreRecord]:
    return db.scores_for_user_id(user_id)
