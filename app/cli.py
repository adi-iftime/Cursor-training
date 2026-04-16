"""CLI entry — Integration Agent."""

from __future__ import annotations

import argparse
from pathlib import Path

from agents.integration_agent import run_application
from config.settings import DATABASE_PATH


def main() -> None:
    p = argparse.ArgumentParser(description="Terminal Snake with SQLite leaderboard")
    p.add_argument(
        "--db",
        type=Path,
        default=None,
        help=f"SQLite path (default: {DATABASE_PATH})",
    )
    args = p.parse_args()
    run_application(db_path=args.db)


if __name__ == "__main__":
    main()
