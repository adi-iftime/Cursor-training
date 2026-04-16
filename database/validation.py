# DAG owner: data_quality — input validation and invariants.
"""Validation for usernames and scores before persistence."""

from __future__ import annotations

from config.settings import MAX_USERNAME_LEN


class ValidationError(ValueError):
    """Raised when user-facing input fails governance rules."""


def validate_username(name: str) -> str:
    s = name.strip()
    if not (1 <= len(s) <= MAX_USERNAME_LEN):
        raise ValidationError("username length invalid")
    if not all(c.isalnum() or c == "_" for c in s):
        raise ValidationError("username must be alphanumeric or underscore")
    return s


def validate_score(value: int) -> int:
    v = int(value)
    if v < 0 or v > 1_000_000_000:
        raise ValidationError("score out of allowed range")
    return v
