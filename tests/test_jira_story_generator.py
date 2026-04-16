"""Jira Story Generator Agent — validation and MCP contract (mocked)."""

from __future__ import annotations

import pytest

from agents.jira_story_generator import MCPIntegrationError, run
from jira.templates import assert_story_body_has_required_sections
from jira.formatter import format_jira_story_description


def test_format_includes_required_sections() -> None:
    body = format_jira_story_description(
        title="T",
        description="D",
        context={"correlation_id": "c1"},
        requested_agent="planner",
        dependencies=["SCRUM-1"],
    )
    assert_story_body_has_required_sections(body)


def test_run_requires_mcp_invoke() -> None:
    task = {
        "title": "x",
        "description": "y",
        "context": {"cloud_id": "cid"},
        "requested_agent": "planner",
        "dependencies": [],
    }
    with pytest.raises(MCPIntegrationError):
        run(task, mcp_invoke=None)


def test_run_validates_registry_agent() -> None:
    task = {
        "title": "x",
        "description": "y",
        "context": {"cloud_id": "cid"},
        "requested_agent": "not_a_real_agent_id",
        "dependencies": [],
    }

    def _mcp(tool: str, args: dict) -> dict:
        raise AssertionError("should not call MCP")

    with pytest.raises(ValueError, match="not in registry"):
        run(task, mcp_invoke=_mcp)


def test_run_happy_path_mock_mcp() -> None:
    calls: list[tuple[str, dict]] = []

    def mcp(tool: str, args: dict) -> dict:
        calls.append((tool, args))
        if tool == "getJiraIssue":
            return {"key": args["issueIdOrKey"], "fields": {"status": {"name": "To Do"}}}
        if tool == "createJiraIssue":
            return {"key": "SCRUM-4242"}
        raise AssertionError(f"unexpected tool {tool}")

    task = {
        "title": "Story title",
        "description": "Do the thing",
        "context": {"cloud_id": "cloud-123", "correlation_id": "abc"},
        "requested_agent": "data_engineer",
        "dependencies": ["SCRUM-10"],
    }
    out = run(task, mcp_invoke=mcp, cloud_id="cloud-123")
    assert out == {
        "jira_key": "SCRUM-4242",
        "summary": "Story title",
        "assigned_agent": "data_engineer",
        "status": "To Do",
    }
    assert [c[0] for c in calls].count("getJiraIssue") == 2
    assert "createJiraIssue" in [c[0] for c in calls]


def test_run_retries_create_on_transient_failure() -> None:
    attempts = {"n": 0}

    def mcp(tool: str, args: dict) -> dict:
        if tool == "getJiraIssue":
            return {"key": args["issueIdOrKey"], "fields": {"status": {"name": "Backlog"}}}
        if tool == "createJiraIssue":
            attempts["n"] += 1
            if attempts["n"] < 2:
                raise RuntimeError("transient")
            return {"key": "SCRUM-777"}
        raise AssertionError(tool)

    task = {
        "title": "R",
        "description": "",
        "context": {"cloud_id": "c"},
        "requested_agent": "tester",
        "dependencies": [],
    }
    out = run(task, mcp_invoke=mcp)
    assert out["jira_key"] == "SCRUM-777"
    assert attempts["n"] == 2
