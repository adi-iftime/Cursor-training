"""
GitHub Pull Request Description Writer — structured bodies via existing GitHubClient.

Consumes orchestrator / workflow payloads (see ``github.pr_formatter.build_pr_writer_payload_from_context``).
Does not construct ad-hoc HTTP clients; updates use ``GitHubClient.update_pull`` only.
"""

from __future__ import annotations

import logging
import re
import time
from typing import Any

from github.client import GitHubClient
from github.pr_formatter import (
    assert_non_placeholder_body,
    format_pr_description_markdown,
)

logger = logging.getLogger(__name__)

MAX_UPDATE_ATTEMPTS = 3
_UPDATE_BACKOFF_SEC = 0.75

JIRA_KEY_FULL = re.compile(r"^[A-Z][A-Z0-9_]{1,30}-\d+$")


def _validate_jira_keys(keys: list[Any]) -> None:
    for k in keys:
        s = str(k).strip()
        if not JIRA_KEY_FULL.match(s):
            raise ValueError(f"Invalid Jira key format: {k!r}")


def validate_pr_writer_payload(payload: dict[str, Any], *, client: GitHubClient | None) -> None:
    """Pre-flight checks before generating or attaching a PR description."""
    branch = str(payload.get("branch_name") or "").strip()
    if not branch:
        raise ValueError("branch_name is required")

    commits = payload.get("commit_history")
    if not isinstance(commits, list) or len(commits) == 0:
        raise ValueError("commit_history must be a non-empty list")

    files = payload.get("changed_files")
    if not isinstance(files, list) or len(files) == 0:
        raise ValueError("changed_files must be a non-empty list")

    diff_summary = str(payload.get("diff_summary") or "").strip()
    if len(diff_summary) < 12:
        raise ValueError("diff_summary is too short — supply real diff or file stats")

    jira_keys = list(payload.get("jira_keys") or [])
    _validate_jira_keys(jira_keys)

    if client is not None:
        owner = str(payload.get("owner") or "").strip()
        repo = str(payload.get("repo") or "").strip()
        num = payload.get("pull_number")
        if not owner or not repo or num is None:
            raise ValueError("owner, repo, and pull_number are required when updating GitHub")
        client.get_git_ref(owner, repo, f"heads/{branch}")


def run(
    payload: dict[str, Any],
    *,
    client: GitHubClient | None = None,
) -> dict[str, Any]:
    """
    Build a structured PR description and optionally PATCH the PR body via ``GitHubClient``.

    Input contract:
      branch_name, commit_history, changed_files, jira_keys, agent_outputs, diff_summary
      plus owner, repo, pull_number when ``client`` is provided.
    """
    logger.info(
        "github_pr_description_writer input branch=%s files=%s jira=%s",
        payload.get("branch_name"),
        len(payload.get("changed_files") or []),
        payload.get("jira_keys"),
    )

    validate_pr_writer_payload(payload, client=client)

    body = format_pr_description_markdown(payload)
    assert_non_placeholder_body(body)
    logger.info("github_pr_description_writer generated body length=%s", len(body))

    if client is None:
        logger.info("github_pr_description_writer skip GitHub update (no client)")
        return {
            "status": "ok",
            "updated": False,
            "body": body,
            "pull": None,
        }

    owner = str(payload["owner"])
    repo = str(payload["repo"])
    num = int(payload["pull_number"])

    last_exc: BaseException | None = None
    for attempt in range(1, MAX_UPDATE_ATTEMPTS + 1):
        try:
            logger.info(
                "github_pr_description_writer update_pull attempt=%s/%s",
                attempt,
                MAX_UPDATE_ATTEMPTS,
            )
            pull = client.update_pull(owner, repo, num, body=body)
            logger.info(
                "github_pr_description_writer update_pull ok url=%s",
                pull.get("html_url"),
            )
            return {
                "status": "ok",
                "updated": True,
                "body": body,
                "pull": {
                    "html_url": pull.get("html_url"),
                    "number": pull.get("number"),
                    "title": pull.get("title"),
                },
            }
        except Exception as exc:
            last_exc = exc
            logger.exception(
                "github_pr_description_writer update_pull failed attempt=%s/%s",
                attempt,
                MAX_UPDATE_ATTEMPTS,
            )
            if attempt < MAX_UPDATE_ATTEMPTS:
                time.sleep(_UPDATE_BACKOFF_SEC * attempt)

    assert last_exc is not None
    raise last_exc
