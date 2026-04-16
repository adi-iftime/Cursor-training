from __future__ import annotations

import json
from pathlib import Path

import pytest

from org.communication_log import append_message, read_messages
from org.message import validate_message
from org.org_state import default_state, load_state, save_state
from org.simulation_engine import run_simulation


def test_validate_message_minimal() -> None:
    m = validate_message(
        {
            "from": "a",
            "to": "b",
            "type": "task",
            "content": "hello",
            "jira_key": "SCRUM-4",
            "context": {"k": 1},
        },
    )
    assert m["from"] == "a"
    assert m["type"] == "task"
    assert m["jira_key"] == "SCRUM-4"


def test_validate_message_rejects_bad_type() -> None:
    with pytest.raises(ValueError):
        validate_message({"from": "a", "to": "b", "type": "nope", "content": "x"})


def test_communication_log_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "communication.json"
    append_message(
        {"from": "pm", "to": "tl", "type": "task", "content": "plan", "jira_key": "X", "context": {}},
        path=p,
    )
    rows = read_messages(path=p)
    assert len(rows) == 1
    assert rows[0]["from"] == "pm"


def test_run_simulation_dry_run_isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    comm = tmp_path / "communication.json"
    comm.write_text("[]\n", encoding="utf-8")
    st_path = tmp_path / "org_state.json"
    save_state(default_state(), path=st_path)

    out = run_simulation(
        dry_run=True,
        story_key="SCRUM-4",
        communication_log_path=comm,
        org_state_path=st_path,
    )
    assert out["review_verdict"] == "approval"
    assert out["merge_done"] is False
    msgs = read_messages(path=comm)
    assert any(m.get("from") == "product_manager" for m in msgs)
    st = load_state(path=st_path)
    assert st["prs"]["SCRUM-4"]["status"] == "approved"
