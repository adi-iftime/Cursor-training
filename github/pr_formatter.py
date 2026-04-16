"""Format structured GitHub PR descriptions from orchestrator / workflow payloads."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from github.client import GitHubClient
from github.pr_service import PullRequestContext
from github.pr_templates import (
    NO_JIRA_STORY_LINE,
    PR_SECTION_AGENTS,
    PR_SECTION_CHANGES,
    PR_SECTION_PURPOSE,
    PR_SECTION_RELATED_JIRA,
    PR_SECTION_RISK,
    PR_SECTION_SUMMARY,
    PR_SECTION_TESTING,
    REQUIRED_SECTION_MARKERS,
)

JIRA_KEY_RE = re.compile(r"\b[A-Z][A-Z0-9_]{1,30}-\d+\b")


def _browse_url(key: str, base: str) -> str:
    b = base.rstrip("/")
    if not b:
        return f"https://<your-site>.atlassian.net/browse/{key}"
    return f"{b}/browse/{key}"


def extract_jira_keys_from_text(*texts: str) -> list[str]:
    """Collect unique Jira-style keys from free text (titles, bodies, branch names)."""
    found: set[str] = set()
    for t in texts:
        if not t:
            continue
        found.update(JIRA_KEY_RE.findall(t))
    return sorted(found)


def build_pr_writer_payload_from_context(
    ctx: PullRequestContext,
    client: GitHubClient,
    *,
    jira_keys: list[str] | None = None,
    agent_outputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Assemble the PR writer input contract from an existing PR and the shared GitHub client.

    Verifies the head branch ref exists via ``get_git_ref`` (existing integration).
    Sets ``jira_browse_base`` from env ``JIRA_BROWSE_BASE`` when not overridden in context.
    """
    owner, repo, num = ctx.owner, ctx.repo, ctx.number
    client.get_git_ref(owner, repo, f"heads/{ctx.head_ref}")
    commits = client.list_pull_commits(owner, repo, num)
    files = client.list_pull_files(owner, repo, num)
    commit_history: list[dict[str, Any]] = []
    for c in commits:
        msg = ""
        if isinstance(c.get("commit"), dict):
            msg = str(c["commit"].get("message") or "")
        commit_history.append({"sha": c.get("sha"), "message": msg.strip()})

    changed_files = [str(f.get("filename") or "") for f in files if f.get("filename")]

    merged_jira = list(
        dict.fromkeys(
            [
                *(jira_keys or []),
                *extract_jira_keys_from_text(ctx.title, ctx.body or "", ctx.head_ref),
            ]
        )
    )

    diff_summary = (ctx.diff_text or "").strip()
    if len(diff_summary) > 16000:
        diff_summary = diff_summary[:16000] + "\n\n_(diff truncated for PR description)_"

    jira_base = (os.environ.get("JIRA_BROWSE_BASE") or "").strip()

    return {
        "branch_name": ctx.head_ref,
        "owner": owner,
        "repo": repo,
        "pull_number": num,
        "commit_history": commit_history,
        "changed_files": changed_files,
        "jira_keys": merged_jira,
        "jira_browse_base": jira_base,
        "agent_outputs": dict(agent_outputs or {}),
        "diff_summary": diff_summary or _fallback_diff_summary(files),
    }


def _fallback_diff_summary(files: list[dict[str, Any]]) -> str:
    if not files:
        return "(no diff summary — empty file list from GitHub)"
    lines = [
        f"- `{f.get('filename')}`: +{f.get('additions', 0)}/-{f.get('deletions', 0)} ({f.get('status')})"
        for f in files[:80]
    ]
    return "Per-file stats from GitHub:\n" + "\n".join(lines)


def _risk_notes(agent_outputs: dict[str, Any], diff_summary: str) -> str:
    lines: list[str] = []
    sec = agent_outputs.get("security")
    if isinstance(sec, dict) and sec.get("summary"):
        lines.append(f"- Security agent: {sec.get('summary')}")
    if "password" in diff_summary.lower() or "secret" in diff_summary.lower():
        lines.append("- Diff mentions secrets/credentials — verify no leakage before merge.")
    if not lines:
        lines.append("- No automated risk flags; review diff and scope.")
    return "\n".join(lines)


def format_pr_description_markdown(payload: dict[str, Any]) -> str:
    """Build the full PR body markdown (universal template; Jira optional)."""
    branch = str(payload["branch_name"])
    files = payload["changed_files"]
    jira_keys = list(payload.get("jira_keys") or [])
    jira_base = str(payload.get("jira_browse_base") or os.environ.get("JIRA_BROWSE_BASE") or "").strip()
    agent_outputs = payload.get("agent_outputs") if isinstance(payload.get("agent_outputs"), dict) else {}
    diff_summary = str(payload.get("diff_summary") or "")

    if jira_keys:
        jira_section_body = "\n".join(f"- `{k}`: {_browse_url(k, jira_base)}" for k in jira_keys)
    else:
        jira_section_body = NO_JIRA_STORY_LINE

    purpose = (
        "Deliver the changes described below with CI and review gates. "
        "If Jira keys are listed, keep implementation aligned to those Stories."
        if jira_keys
        else "Non-feature or maintenance change: document rationale, tests, and risks; no feature-level Jira Story required."
    )

    change_lines = [
        "Diff-derived view (verbatim excerpt / stats; may be truncated):",
        "",
        "```text",
        diff_summary[:12000] if diff_summary else "(empty)",
        "```",
        "",
        "Files touched:",
        "",
    ]
    for f in files[:200]:
        change_lines.append(f"- `{f}`")
    if len(files) > 200:
        change_lines.append(f"- _…and {len(files) - 200} more_")

    if agent_outputs:
        agents_blob = json.dumps(agent_outputs, indent=2, default=str)
        agent_section = f"```json\n{agents_blob[:8000]}\n```"
    else:
        agent_section = "- (none)"

    testing = "- See CI / local verification noted in agent outputs and repo checks."
    if isinstance(agent_outputs.get("tester"), dict) and (agent_outputs["tester"].get("summary") or "").strip():
        testing = f"- Tester agent: {agent_outputs['tester']['summary']}"

    risk = _risk_notes(agent_outputs, diff_summary)

    parts = [
        PR_SECTION_SUMMARY,
        "",
        f"Changes on branch `{branch}` (automated scaffold; expand if needed).",
        "",
        PR_SECTION_PURPOSE,
        "",
        purpose,
        "",
        PR_SECTION_CHANGES,
        "",
        "\n".join(change_lines),
        "",
        PR_SECTION_AGENTS,
        "",
        agent_section,
        "",
        PR_SECTION_TESTING,
        "",
        testing,
        "",
        PR_SECTION_RISK,
        "",
        risk,
        "",
        PR_SECTION_RELATED_JIRA,
        "",
        jira_section_body,
        "",
    ]

    body = "\n".join(parts)
    for m in REQUIRED_SECTION_MARKERS:
        if m not in body:
            raise ValueError(f"PR formatter invariant failed: missing {m!r}")
    return body


def assert_non_placeholder_body(body: str) -> None:
    """Reject generic bodies; ensure Related Jira section is explicit (keys or no-jira line)."""
    t = body.lower()
    banned = ("lorem ipsum", "todo: fill", "placeholder pr", "tbd tbd")
    if any(b in t for b in banned):
        raise ValueError("PR body appears to be placeholder or generic")
    if PR_SECTION_RELATED_JIRA not in body:
        raise ValueError("PR body missing Related Jira section")
    if NO_JIRA_STORY_LINE not in body and not JIRA_KEY_RE.search(body):
        raise ValueError(
            "Related Jira section must list at least one Jira key or the exact no-Jira line: "
            + repr(NO_JIRA_STORY_LINE)
        )
    if len(body.strip()) < 200:
        raise ValueError("PR body too short to be a substantive description")
