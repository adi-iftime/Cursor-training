"""
PR Re-review Agent — compares new diff analysis vs prior issue fingerprints.
"""

from __future__ import annotations

import logging
from typing import Any

from agents.pr_review_agent.analysis import analyze_diff, highest_severity, issue_fingerprint

logger = logging.getLogger(__name__)


def run(
    pr_context: dict[str, Any],
    original_issues: list[dict[str, Any]],
) -> dict[str, Any]:
    diff = pr_context.get("diff_text") or ""
    try:
        new_issues = analyze_diff(diff)
    except Exception as e:  # noqa: BLE001
        logger.exception("pr_rereview failed")
        return {
            "status": "error",
            "summary": f"Re-review failed: {e}",
            "issues": [],
            "actions_taken": [],
            "recommendation": "ESCALATE",
            "resolved_original_ids": [],
            "unresolved_original_ids": [i.get("id", "") for i in original_issues],
        }

    orig_by_fp = {issue_fingerprint(i): i for i in original_issues}
    new_by_fp = {issue_fingerprint(i): i for i in new_issues}

    resolved_ids: list[str] = []
    unresolved_ids: list[str] = []
    for fp, old in orig_by_fp.items():
        oid = old.get("id")
        if fp not in new_by_fp and oid:
            resolved_ids.append(str(oid))
        elif fp in new_by_fp and oid:
            unresolved_ids.append(str(oid))

    hi_new = highest_severity(new_issues)

    old_fps_set = set(orig_by_fp.keys())
    regressions = [
        i
        for fp, i in new_by_fp.items()
        if fp not in old_fps_set and i.get("severity") == "HIGH"
    ]

    verdict: str
    if regressions:
        verdict = "REQUEST_CHANGES"
    elif hi_new == "HIGH":
        verdict = "REQUEST_CHANGES"
    elif hi_new == "MEDIUM":
        verdict = "REQUEST_CHANGES"
    elif hi_new == "LOW" and new_issues:
        verdict = "APPROVE"
    elif not new_issues:
        verdict = "APPROVE"
    elif len(new_issues) > max(5, len(original_issues) + 3):
        verdict = "ESCALATE"
    else:
        verdict = "REQUEST_CHANGES"

    summary = (
        f"New issues={len(new_issues)}, max_severity={hi_new}, "
        f"resolved_original={len(resolved_ids)}, regressions_high={len(regressions)}."
    )

    out = {
        "status": "ok",
        "summary": summary,
        "issues": new_issues,
        "actions_taken": ["diff_reanalysis_compare_v1"],
        "recommendation": verdict,
        "resolved_original_ids": resolved_ids,
        "unresolved_original_ids": unresolved_ids,
    }
    logger.info("pr_rereview output", extra={"verdict": verdict})
    return out
