# DAG owner: tester (data quality paths)
from __future__ import annotations

import pytest

from database.validation import ValidationError, validate_score, validate_username


def test_username_ok() -> None:
    assert validate_username("user_1") == "user_1"


def test_username_rejects_injection_chars() -> None:
    with pytest.raises(ValidationError):
        validate_username("a;b")


def test_score_bounds() -> None:
    with pytest.raises(ValidationError):
        validate_score(-1)
