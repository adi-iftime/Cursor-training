"""
Higher-level PR operations: context assembly, CI evaluation, diff retrieval.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Mapping

from github.client import GitHubClient, GitHubAPIError


@dataclass
class PullRequestContext:
    """Structured PR context passed to agents."""

    owner: str
    repo: str
    number: int
    title: str
    body: str
    head_sha: str
    head_ref: str
    base_ref: str
    user_login: str
    draft: bool
    mergeable: bool | None
    diff_text: str
    combined_status: dict[str, Any] = field(default_factory=dict)
    check_runs: dict[str, Any] = field(default_factory=dict)
    raw_pull: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "owner": self.owner,
            "repo": self.repo,
            "number": self.number,
            "title": self.title,
            "body": self.body,
            "head_sha": self.head_sha,
            "head_ref": self.head_ref,
            "base_ref": self.base_ref,
            "user_login": self.user_login,
            "draft": self.draft,
            "mergeable": self.mergeable,
            "diff_text": self.diff_text,
            "combined_status": self.combined_status,
            "check_runs": self.check_runs,
        }


def fetch_pr_context(client: GitHubClient, owner: str, repo: str, pull_number: int) -> PullRequestContext:
    raw = client.get_pull(owner, repo, pull_number)
    diff_text = client.get_pull_diff(owner, repo, pull_number)
    head_sha = raw["head"]["sha"]
    combined = {}
    checks: dict[str, Any] = {}
    try:
        combined = client.get_combined_status(owner, repo, head_sha)
    except GitHubAPIError:
        combined = {"state": "unknown", "statuses": []}
    try:
        checks = client.list_check_runs_for_commit(owner, repo, head_sha)
    except GitHubAPIError:
        checks = {"check_runs": [], "total_count": 0}

    return PullRequestContext(
        owner=owner,
        repo=repo,
        number=pull_number,
        title=raw.get("title") or "",
        body=raw.get("body") or "",
        head_sha=head_sha,
        head_ref=raw["head"]["ref"],
        base_ref=raw["base"]["ref"],
        user_login=raw["user"]["login"],
        draft=bool(raw.get("draft")),
        mergeable=raw.get("mergeable"),
        diff_text=diff_text,
        combined_status=combined,
        check_runs=checks,
        raw_pull=raw,
    )


def evaluate_ci_passed(
    ctx: PullRequestContext,
    *,
    required_checks: list[str],
) -> tuple[bool, str]:
    """
    Returns (passed, reason).

    required_checks: each entry is a case-insensitive substring that must appear
    in at least one check run name, and all matching runs must be successful.
    If required_checks is empty, all completed runs must succeed (pending fails closed).
    """
    runs = ctx.check_runs.get("check_runs") or []
    if not runs:
        state = (ctx.combined_status or {}).get("state")
        if state == "success":
            return True, "legacy_status_success"
        if state in ("failure", "error"):
            return False, f"legacy_status_{state}"
        if state == "pending":
            return False, "legacy_status_pending"
        return True, "no_check_runs_assumed_ok"

    pending = [r for r in runs if r.get("status") in ("queued", "in_progress", "waiting", "requested")]
    if pending:
        return False, f"checks_pending:{len(pending)}"

    failed = [
        r
        for r in runs
        if r.get("conclusion") is not None
        and r.get("conclusion") not in ("success", "skipped", "neutral")
    ]
    if failed:
        names = [f.get("name") for f in failed[:8]]
        return False, f"checks_failed:{names}"

    if not required_checks:
        return True, "all_check_runs_success"

    for req in required_checks:
        req_l = req.lower()
        matching = [r for r in runs if req_l in (r.get("name") or "").lower()]
        if not matching:
            return False, f"required_check_missing:{req}"
        if not all(r.get("conclusion") in ("success", "skipped", "neutral") for r in matching):
            return False, f"required_check_not_success:{req}"

    return True, "required_checks_satisfied"


def summarize_reviews(client: GitHubClient, owner: str, repo: str, pull_number: int) -> list[dict[str, Any]]:
    return client.list_reviews(owner, repo, pull_number)


def post_bot_comment(client: GitHubClient, owner: str, repo: str, pull_number: int, body: str) -> dict[str, Any]:
    return client.post_issue_comment(owner, repo, pull_number, body)


def load_workflow_config(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def workflow_config_defaults() -> Mapping[str, Any]:
    return {
        "max_cycles": 3,
        "auto_merge_enabled": False,
        "required_checks": ["ci", "test"],
        "severity_threshold_for_block": "HIGH",
    }
