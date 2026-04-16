"""Leaderboard Agent — ordering."""

from __future__ import annotations

from pathlib import Path

from agents.leaderboard_agent import top_scores
from database.db import Database, ensure_user, init_schema, save_score, get_connection


def test_leaderboard_sorted_by_score_desc(tmp_path: Path) -> None:
    dbp = tmp_path / "lb.db"
    conn = get_connection(dbp)
    init_schema(conn)
    a = ensure_user(conn, "a")
    b = ensure_user(conn, "b")
    save_score(conn, a, 10)
    save_score(conn, b, 50)
    save_score(conn, a, 40)
    conn.close()

    db = Database(dbp)
    rows = top_scores(db, limit=10)
    assert [r.username for r in rows[:2]] == ["b", "a"]
    assert rows[0].score >= rows[1].score
    db.close()
