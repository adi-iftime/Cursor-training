"""GitHub PR Description Writer — validation, formatting, GitHubClient integration (mocked)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agents.github_pr_description_writer import run, validate_pr_writer_payload
from github.pr_formatter import format_pr_description_markdown
from github.pr_templates import NO_JIRA_STORY_LINE, PR_SECTION_RELATED_JIRA, PR_SECTION_SUMMARY


def _minimal_payload(**overrides: object) -> dict:
    base = {
        "branch_name": "feature/example",
        "owner": "acme",
        "repo": "app",
        "pull_number": 42,
        "commit_history": [{"sha": "deadbeef", "message": "feat: example"}],
        "changed_files": ["src/foo.py", "tests/test_foo.py"],
        "jira_keys": ["SCRUM-99"],
        "jira_browse_base": "https://acme.atlassian.net",
        "agent_outputs": {"tester": {"summary": "pytest green"}},
        "diff_summary": "diff --git a/src/foo.py\n+ added line\n" * 3,
    }
    base.update(overrides)
    return base  # type: ignore[return-value]


def test_format_contains_required_sections() -> None:
    body = format_pr_description_markdown(_minimal_payload())
    assert PR_SECTION_SUMMARY in body
    assert PR_SECTION_RELATED_JIRA in body
    assert "`SCRUM-99`:" in body
    assert "### ⚠️ Risk Notes" in body


def test_format_no_jira_uses_sentinel() -> None:
    body = format_pr_description_markdown(_minimal_payload(jira_keys=[]))
    assert NO_JIRA_STORY_LINE in body
    assert PR_SECTION_RELATED_JIRA in body


def test_validate_rejects_empty_files() -> None:
    p = _minimal_payload(changed_files=[])
    with pytest.raises(ValueError, match="changed_files"):
        validate_pr_writer_payload(p, client=None)


def test_validate_rejects_bad_jira_key() -> None:
    p = _minimal_payload(jira_keys=["bad"])
    with pytest.raises(ValueError, match="Invalid Jira key"):
        validate_pr_writer_payload(p, client=None)


def test_run_without_client_returns_body() -> None:
    out = run(_minimal_payload(), client=None)
    assert out["status"] == "ok"
    assert out["updated"] is False
    assert len(out["body"]) > 200
    assert PR_SECTION_RELATED_JIRA in out["body"]


def test_run_with_client_updates_pr() -> None:
    client = MagicMock()
    client.get_git_ref.return_value = {"object": {"sha": "x"}}
    client.update_pull.return_value = {
        "html_url": "https://github.com/acme/app/pull/42",
        "number": 42,
        "title": "t",
    }
    out = run(_minimal_payload(), client=client)
    assert out["updated"] is True
    client.update_pull.assert_called_once()
    _args, kwargs = client.update_pull.call_args
    assert "body" in kwargs


def test_run_retries_then_succeeds() -> None:
    client = MagicMock()
    client.get_git_ref.return_value = {"object": {"sha": "x"}}
    client.update_pull.side_effect = [RuntimeError("fail"), RuntimeError("fail"), {"html_url": "u", "number": 1, "title": "t"}]
    with patch("agents.github_pr_description_writer.time.sleep", lambda *_: None):
        out = run(_minimal_payload(), client=client)
    assert out["updated"] is True
    assert client.update_pull.call_count == 3
