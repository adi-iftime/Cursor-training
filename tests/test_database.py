"""Database Agent — persistence."""

from __future__ import annotations

from pathlib import Path

from database.db import Database, ensure_user, init_schema, save_score, get_connection


def test_insert_user_and_score(tmp_path: Path) -> None:
    dbp = tmp_path / "t.db"
    conn = get_connection(dbp)
    init_schema(conn)
    uid = ensure_user(conn, "alice")
    sid = save_score(conn, uid, 42)
    assert uid >= 1
    assert sid >= 1


def test_database_facade(tmp_path: Path) -> None:
    db = Database(tmp_path / "x.db")
    uid = db.ensure_user("bob")
    db.save_score(uid, 7)
    rows = db.scores_for_user_id(uid)
    assert len(rows) == 1
    assert rows[0].score == 7
    db.close()
