"""
Auto-merge Agent — gates on CI, verdict, severity, and workflow flags.
"""

from __future__ import annotations

import logging
from typing import Any

from github.client import GitHubClient
from github.pr_service import PullRequestContext, evaluate_ci_passed

logger = logging.getLogger(__name__)


def run(
    pr_context: dict[str, Any],
    *,
    rereview: dict[str, Any],
    remaining_issues: list[dict[str, Any]],
    client: GitHubClient | None,
    workflow: dict[str, Any],
) -> dict[str, Any]:
    owner = pr_context.get("owner")
    repo = pr_context.get("repo")
    number = pr_context.get("number")
    verdict = (rereview or {}).get("recommendation")
    auto_merge = bool(workflow.get("auto_merge_enabled", False))
    required_checks = list(workflow.get("required_checks") or [])
    threshold = str(workflow.get("severity_threshold_for_block", "HIGH"))

    logger.info(
        "auto_merge input",
        extra={
            "owner": owner,
            "repo": repo,
            "number": number,
            "verdict": verdict,
            "auto_merge_enabled": auto_merge,
        },
    )

    actions: list[str] = []

    if not auto_merge:
        return {
            "status": "ok",
            "summary": "auto_merge_enabled is false — skipping merge.",
            "issues": remaining_issues,
            "actions_taken": ["skipped_disabled"],
            "recommendation": "SKIPPED",
        }

    if pr_context.get("draft"):
        return {
            "status": "ok",
            "summary": "Draft PR cannot be auto-merged.",
            "issues": remaining_issues,
            "actions_taken": ["blocked_draft"],
            "recommendation": "BLOCKED",
        }

    if verdict != "APPROVE":
        return {
            "status": "ok",
            "summary": f"Re-review verdict is {verdict!r}; merge blocked.",
            "issues": remaining_issues,
            "actions_taken": ["blocked_verdict"],
            "recommendation": "BLOCKED",
        }

    ctx = PullRequestContext(
        owner=str(owner),
        repo=str(repo),
        number=int(number),
        title=str(pr_context.get("title") or ""),
        body=str(pr_context.get("body") or ""),
        head_sha=str(pr_context.get("head_sha") or ""),
        head_ref=str(pr_context.get("head_ref") or ""),
        base_ref=str(pr_context.get("base_ref") or ""),
        user_login=str(pr_context.get("user_login") or ""),
        draft=bool(pr_context.get("draft")),
        mergeable=pr_context.get("mergeable"),
        diff_text=str(pr_context.get("diff_text") or ""),
        combined_status=pr_context.get("combined_status") or {},
        check_runs=pr_context.get("check_runs") or {},
        raw_pull={},
    )
    ci_ok, ci_reason = evaluate_ci_passed(ctx, required_checks=required_checks)
    actions.append(f"ci_check:{ci_reason}")
    if not ci_ok:
        return {
            "status": "ok",
            "summary": f"CI not satisfied ({ci_reason}).",
            "issues": remaining_issues,
            "actions_taken": actions,
            "recommendation": "BLOCKED",
        }

    sev_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    block_level = sev_order.get(threshold, 3)
    for issue in remaining_issues:
        s = issue.get("severity")
        if s in sev_order and sev_order[s] >= block_level:
            return {
                "status": "ok",
                "summary": f"Blocked by remaining issue severity={s} (threshold={threshold}).",
                "issues": remaining_issues,
                "actions_taken": actions + ["blocked_severity"],
                "recommendation": "BLOCKED",
            }

    if client is None or owner is None or repo is None or number is None:
        return {
            "status": "error",
            "summary": "GitHub client or PR identifiers missing; cannot merge.",
            "issues": remaining_issues,
            "actions_taken": actions,
            "recommendation": "BLOCKED",
        }

    try:
        merge_method = str(workflow.get("merge_method", "merge"))
        client.merge_pull(owner, repo, int(number), merge_method=merge_method)
        actions.append("merge_api_called")
    except Exception as e:  # noqa: BLE001
        logger.exception("merge failed")
        return {
            "status": "error",
            "summary": f"Merge API failed: {e}",
            "issues": remaining_issues,
            "actions_taken": actions,
            "recommendation": "BLOCKED",
        }

    return {
        "status": "ok",
        "summary": "Merged via GitHub API.",
        "issues": remaining_issues,
        "actions_taken": actions,
        "recommendation": "MERGED",
    }
