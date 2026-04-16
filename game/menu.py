# DAG owner: data_engineer (UI shell) — stdin menu; security: strict username charset.
"""Text menu and username prompt (no curses)."""

from __future__ import annotations

from database.validation import ValidationError, validate_username


def show_main_menu() -> int:
    print("\n=== Snake ===\n")
    print("1. Start Game")
    print("2. View Leaderboard")
    print("3. View Users")
    print("4. Exit")
    while True:
        raw = input("Select (1-4): ").strip()
        if raw in {"1", "2", "3", "4"}:
            return int(raw)
        print("Please enter 1, 2, 3, or 4.")


def prompt_username() -> str:
    while True:
        raw = input("Username (letters, digits, _): ").strip()
        try:
            return validate_username(raw)
        except ValidationError as e:
            print(f"Invalid: {e}")
