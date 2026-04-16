# DAG owner: tester
from __future__ import annotations

from pathlib import Path

from database.analytics import global_leaderboard
from database.db import Database, ensure_user, get_connection, init_schema, save_score


def test_leaderboard_order(tmp_path: Path) -> None:
    dbp = tmp_path / "x.db"
    conn = get_connection(dbp)
    init_schema(conn)
    a = ensure_user(conn, "a")
    b = ensure_user(conn, "b")
    save_score(conn, a, 10)
    save_score(conn, b, 100)
    conn.close()
    db = Database(dbp)
    rows = global_leaderboard(db, limit=10)
    assert rows[0].username == "b"
    assert rows[0].score >= rows[1].score
    db.close()
