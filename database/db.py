"""SQLite persistence (Database Agent)."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from database.models import LeaderboardRow, ScoreRecord, User


def get_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE INDEX IF NOT EXISTS idx_scores_user ON scores(user_id);
        CREATE INDEX IF NOT EXISTS idx_scores_score ON scores(score DESC);
        """
    )
    conn.commit()


def get_user_by_name(conn: sqlite3.Connection, username: str) -> User | None:
    row = conn.execute("SELECT id, username FROM users WHERE username = ?", (username.strip(),)).fetchone()
    if row is None:
        return None
    return User(id=int(row["id"]), username=str(row["username"]))


def register_user(conn: sqlite3.Connection, username: str) -> int:
    username = username.strip()
    if not username:
        raise ValueError("username required")
    cur = conn.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    return int(cur.lastrowid)


def ensure_user(conn: sqlite3.Connection, username: str) -> int:
    u = get_user_by_name(conn, username)
    if u:
        return u.id
    return register_user(conn, username)


def save_score(conn: sqlite3.Connection, user_id: int, score: int, *, when: datetime | None = None) -> int:
    when = when or datetime.now(timezone.utc)
    cur = conn.execute(
        "INSERT INTO scores (user_id, score, created_at) VALUES (?, ?, ?)",
        (user_id, int(score), when.isoformat()),
    )
    conn.commit()
    return int(cur.lastrowid)


def leaderboard_top(conn: sqlite3.Connection, limit: int = 20) -> list[LeaderboardRow]:
    rows = conn.execute(
        """
        SELECT u.username AS username, s.score AS score, s.created_at AS created_at
        FROM scores s
        JOIN users u ON u.id = s.user_id
        ORDER BY s.score DESC, s.created_at ASC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    return [
        LeaderboardRow(
            username=str(r["username"]),
            score=int(r["score"]),
            created_at=datetime.fromisoformat(str(r["created_at"])),
        )
        for r in rows
    ]


def scores_for_user(conn: sqlite3.Connection, user_id: int) -> list[ScoreRecord]:
    rows = conn.execute(
        """
        SELECT id, user_id, score, created_at
        FROM scores
        WHERE user_id = ?
        ORDER BY score DESC, created_at DESC
        """,
        (user_id,),
    ).fetchall()
    return [
        ScoreRecord(
            id=int(r["id"]),
            user_id=int(r["user_id"]),
            score=int(r["score"]),
            created_at=datetime.fromisoformat(str(r["created_at"])),
        )
        for r in rows
    ]


def list_users(conn: sqlite3.Connection) -> list[User]:
    rows = conn.execute("SELECT id, username FROM users ORDER BY username COLLATE NOCASE").fetchall()
    return [User(id=int(r["id"]), username=str(r["username"])) for r in rows]


class Database:
    """Facade for app and tests."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._conn: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = get_connection(self.path)
            init_schema(self._conn)
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def ensure_user(self, username: str) -> int:
        return ensure_user(self.connect(), username)

    def save_score(self, user_id: int, score: int) -> int:
        return save_score(self.connect(), user_id, score)

    def leaderboard_top(self, limit: int = 20) -> list[LeaderboardRow]:
        return leaderboard_top(self.connect(), limit)

    def list_users(self) -> list[User]:
        return list_users(self.connect())

    def scores_for_user_id(self, user_id: int) -> list[ScoreRecord]:
        return scores_for_user(self.connect(), user_id)
