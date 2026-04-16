"""
PR Fixer Agent — minimal automated fixes via GitHub Contents API (optional).
"""

from __future__ import annotations

import base64
import logging
from typing import Any

from github.client import GitHubClient, GitHubAPIError

logger = logging.getLogger(__name__)


def _decode_content(node: dict[str, Any]) -> str:
    enc = node.get("encoding")
    content = node.get("content") or ""
    if enc == "base64":
        return base64.b64decode(content).decode("utf-8", errors="replace")
    return content


def _fix_eof_newline(
    client: GitHubClient,
    owner: str,
    repo: str,
    branch: str,
    path: str,
) -> tuple[bool, str]:
    try:
        node = client.get_file_contents(owner, repo, path, ref=branch)
    except GitHubAPIError as e:
        return False, f"fetch_failed:{e}"
    if isinstance(node, list):
        return False, "path_is_directory"
    text = _decode_content(node)
    if text.endswith("\n"):
        return True, "already_ok"
    sha = node.get("sha")
    if not sha:
        return False, "missing_blob_sha"
    new_text = text + "\n"
    try:
        client.put_file_contents(
            owner,
            repo,
            path,
            message=f"chore: add missing newline at EOF for {path}",
            content_text=new_text,
            branch=branch,
            sha=sha,
        )
    except GitHubAPIError as e:
        return False, f"put_failed:{e}"
    return True, "committed"


def run(
    pr_context: dict[str, Any],
    review_issues: list[dict[str, Any]],
    *,
    client: GitHubClient | None = None,
    workflow: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Attempts safe autofixes. Requires `client` and token for remote fixes.
    `workflow` may include `enable_eof_autofix` (default True).
    """
    wf = workflow or {}
    enable_eof = bool(wf.get("enable_eof_autofix", True))
    actions: list[str] = []
    remaining = list(review_issues)

    owner = pr_context.get("owner")
    repo = pr_context.get("repo")
    branch = pr_context.get("head_ref")

    logger.info(
        "pr_fixer input",
        extra={"owner": owner, "repo": repo, "branch": branch, "issues": len(review_issues)},
    )

    if client is None or not owner or not repo or not branch:
        summary = "No GitHub client or incomplete PR context; cannot apply remote fixes."
        return {
            "status": "ok",
            "summary": summary,
            "issues": remaining,
            "actions_taken": ["skipped_no_client"],
            "recommendation": "MANUAL_REQUIRED",
        }

    if enable_eof:
        eof_issues = [i for i in list(remaining) if i.get("type") == "missing_eof_newline" and i.get("autofix")]
        for issue in eof_issues:
            path = issue.get("file")
            if not path or not isinstance(path, str):
                continue
            ok, reason = _fix_eof_newline(client, owner, repo, branch, path)
            actions.append(f"eof_newline:{path}:{reason}")
            if ok and reason == "committed":
                remaining = [x for x in remaining if x.get("id") != issue.get("id")]

    # Summarize remaining HIGH issues as manual
    rec = "FIXED" if len(remaining) < len(review_issues) else "PARTIAL"
    highs = [i for i in remaining if i.get("severity") == "HIGH"]
    if highs:
        rec = "MANUAL_REQUIRED"
    if len(remaining) == len(review_issues) and review_issues:
        rec = "MANUAL_REQUIRED"

    if not review_issues:
        rec = "FIXED"

    summary = f"Remaining issues: {len(remaining)} (started with {len(review_issues)})."
    out = {
        "status": "ok",
        "summary": summary,
        "issues": remaining,
        "actions_taken": actions or ["no_automatic_fix_applied"],
        "recommendation": rec,
    }
    logger.info("pr_fixer output", extra={"recommendation": out["recommendation"]})
    return out
