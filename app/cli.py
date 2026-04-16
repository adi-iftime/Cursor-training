# DAG owner: orchestrator (composition only) — wires menu, play, persistence, analytics.
"""Application entry: `python -m app.cli` from repository root."""

from __future__ import annotations

import argparse
from pathlib import Path

from config.settings import DATABASE_PATH
from database.analytics import global_leaderboard
from database.db import Database
from game.main import run_play_session
from game.menu import prompt_username, show_main_menu


def _print_leaderboard(db: Database) -> None:
    rows = global_leaderboard(db, limit=50)
    print("\n--- Leaderboard ---")
    if not rows:
        print("(no scores yet)")
        return
    for i, r in enumerate(rows, start=1):
        print(f"{i:2}. {r.username:20} {r.score:8}  {r.created_at.isoformat()}")


def _print_users(db: Database) -> None:
    users = db.list_users()
    print("\n--- Users ---")
    if not users:
        print("(none)")
        return
    for u in users:
        print(f"  {u.id}: {u.username}")


def main() -> None:
    p = argparse.ArgumentParser(description="Terminal Snake with SQLite leaderboard")
    p.add_argument("--db", type=Path, default=None, help=f"SQLite DB (default: {DATABASE_PATH})")
    args = p.parse_args()
    path = args.db or DATABASE_PATH
    db = Database(path)
    try:
        db.connect()
        while True:
            choice = show_main_menu()
            if choice == 1:
                user = prompt_username()
                uid = db.ensure_user(user)
                score = run_play_session()
                db.save_score(uid, score)
                print(f"\nSession ended. Score {score} saved for {user}.\n")
            elif choice == 2:
                _print_leaderboard(db)
            elif choice == 3:
                _print_users(db)
            else:
                print("Goodbye.")
                break
    finally:
        db.close()


if __name__ == "__main__":
    main()
