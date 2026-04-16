"""
Integration Agent — composes menu, gameplay session, database, and leaderboard views.

Entry: `run_application()` used by `app/cli.py`.
"""

from __future__ import annotations

from pathlib import Path

from agents.database_agent import Database, default_database_path
from agents.leaderboard_agent import print_leaderboard, print_users
from agents.menu_agent import prompt_username, show_main_menu
from game.main import run_play_session


def run_application(*, db_path: Path | None = None) -> None:
    path = db_path or default_database_path()
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
                print(f"\nGame over. Score {score} saved for {user}.\n")
            elif choice == 2:
                print_leaderboard(db)
            elif choice == 3:
                print_users(db)
            else:
                print("Goodbye.")
                break
    finally:
        db.close()
