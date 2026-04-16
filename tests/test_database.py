# DAG owner: tester
from __future__ import annotations

from pathlib import Path

from database.db import Database, ensure_user, get_connection, init_schema, save_score


def test_user_and_score_roundtrip(tmp_path: Path) -> None:
    dbp = tmp_path / "t.db"
    conn = get_connection(dbp)
    init_schema(conn)
    uid = ensure_user(conn, "alice")
    save_score(conn, uid, 99)
    conn.close()
    db = Database(dbp)
    rows = db.scores_for_user_id(uid)
    assert len(rows) == 1
    assert rows[0].score == 99
    db.close()
