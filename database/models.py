# DAG owner: data_governance — domain entities and schema alignment.
"""Persistent domain models (users, scores)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    id: int
    username: str


@dataclass(frozen=True)
class ScoreRecord:
    id: int
    user_id: int
    score: int
    created_at: datetime


@dataclass(frozen=True)
class LeaderboardRow:
    username: str
    score: int
    created_at: datetime
