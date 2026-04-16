"""Unit tests for utils.schema_helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from utils.schema_helpers import attach_correlation_id, load_json, require_keys


def test_require_keys_passes() -> None:
    require_keys({"a": 1}, ("a",), context="test")


def test_require_keys_raises() -> None:
    with pytest.raises(ValueError, match="missing keys"):
        require_keys({}, ("a",), context="test")


def test_attach_correlation_id() -> None:
    out = attach_correlation_id({"x": 1}, "corr-1")
    assert out == {"x": 1, "correlation_id": "corr-1"}


def test_load_json_reads_file(tmp_path: Path) -> None:
    p = tmp_path / "x.json"
    p.write_text('{"ok": true}', encoding="utf-8")
    assert load_json(p) == {"ok": True}


def test_load_json_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        load_json(tmp_path / "missing.json")


def test_load_json_invalid(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_json(p)
