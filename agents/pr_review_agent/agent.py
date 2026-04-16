"""
PR Review Agent — static analysis over unified diff + structured JSON result.
"""

from __future__ import annotations

import logging
from typing import Any

from agents.pr_review_agent.analysis import analyze_diff, highest_severity

logger = logging.getLogger(__name__)


def run(pr_context: dict[str, Any]) -> dict[str, Any]:
    """
    pr_context: expects keys from PullRequestContext.to_dict() at minimum:
      owner, repo, number, diff_text, head_ref, base_ref, head_sha
    """
    logger.info(
        "pr_review input",
        extra={
            "owner": pr_context.get("owner"),
            "repo": pr_context.get("repo"),
            "number": pr_context.get("number"),
        },
    )
    diff = pr_context.get("diff_text") or ""
    try:
        issues = analyze_diff(diff)
    except Exception as e:  # noqa: BLE001 — surface as agent error
        logger.exception("pr_review failed")
        return {
            "status": "error",
            "summary": f"Review failed: {e}",
            "issues": [],
            "actions_taken": [],
            "recommendation": "REQUEST_CHANGES",
        }

    hi = highest_severity(issues)
    if hi == "HIGH":
        rec = "REQUEST_CHANGES"
    elif hi == "MEDIUM":
        rec = "REQUEST_CHANGES"
    elif issues:
        rec = "COMMENT"
    else:
        rec = "APPROVE"

    summary = f"Found {len(issues)} issue(s); max severity={hi or 'none'}."

    out = {
        "status": "ok",
        "summary": summary,
        "issues": issues,
        "actions_taken": ["static_diff_analysis_v1"],
        "recommendation": rec,
    }
    logger.info(
        "pr_review output",
        extra={"issues": len(issues), "recommendation": rec},
    )
    return out


def run_with_diff(diff_text: str, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """Test helper: run review with raw diff only."""
    ctx = {"diff_text": diff_text, **(meta or {})}
    return run(ctx)
