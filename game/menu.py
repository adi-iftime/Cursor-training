"""Text menu for terminal (Menu Agent). No curses — stdout/stdin only."""

from __future__ import annotations


def show_main_menu() -> int:
    """
    Display main menu and return choice 1–4.

    1 Start Game
    2 View Leaderboard
    3 View Users
    4 Exit
    """
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
        name = input("Username (letters/numbers/_): ").strip()
        if 1 <= len(name) <= 64 and all(c.isalnum() or c == "_" for c in name):
            return name
        print("Invalid username. Use 1–64 chars: letters, digits, underscore.")
