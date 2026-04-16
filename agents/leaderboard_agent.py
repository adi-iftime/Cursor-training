"""
Leaderboard Agent — global top-N ranking and per-user score lists (read model).

Queries live in `database/db.py`; this agent exposes the reporting surface.
"""

from __future__ import annotations

from database.db import Database
from database.models import LeaderboardRow, ScoreRecord, User


def top_scores(db: Database, limit: int = 20) -> list[LeaderboardRow]:
    return db.leaderboard_top(limit=limit)


def all_users(db: Database) -> list[User]:
    return db.list_users()


def scores_for_user(db: Database, user_id: int) -> list[ScoreRecord]:
    return db.scores_for_user_id(user_id)


def print_leaderboard(db: Database, limit: int = 20) -> None:
    rows = top_scores(db, limit=limit)
    print("\n--- Leaderboard (top scores) ---")
    if not rows:
        print("(no scores yet)")
        return
    for i, r in enumerate(rows, start=1):
        print(f"{i:2}. {r.username:20} {r.score:6}  {r.created_at.isoformat()}")


def print_users(db: Database) -> None:
    users = all_users(db)
    print("\n--- Registered users ---")
    if not users:
        print("(none)")
        return
    for u in users:
        print(f"  {u.id}: {u.username}")
