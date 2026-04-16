"""Format structured GitHub PR descriptions from orchestrator / workflow payloads."""

from __future__ import annotations

import json
import re
from typing import Any

from github.client import GitHubClient
from github.pr_service import PullRequestContext
from github.pr_templates import (
    OPTIONAL_DEPLOY_MARKER,
    PR_SECTION_AGENTS,
    PR_SECTION_CHANGES,
    PR_SECTION_FILES,
    PR_SECTION_JIRA,
    PR_SECTION_RISK,
    PR_SECTION_SUMMARY,
    PR_SECTION_TESTING,
    PR_SECTION_VALIDATION,
    REQUIRED_SECTION_MARKERS,
)

JIRA_KEY_RE = re.compile(r"\b[A-Z][A-Z0-9_]{1,30}-\d+\b")


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

    return {
        "branch_name": ctx.head_ref,
        "owner": owner,
        "repo": repo,
        "pull_number": num,
        "commit_history": commit_history,
        "changed_files": changed_files,
        "jira_keys": merged_jira,
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
        lines.append("- No automated risk flags; review diff and linked Jira scope.")
    return "\n".join(lines)


def _deploy_notes(agent_outputs: dict[str, Any]) -> str | None:
    devops = agent_outputs.get("devops")
    if isinstance(devops, dict) and devops.get("summary"):
        return str(devops["summary"])
    return None


def format_pr_description_markdown(payload: dict[str, Any]) -> str:
    """Build the full PR body markdown from a validated payload."""
    branch = str(payload["branch_name"])
    commits = payload["commit_history"]
    files = payload["changed_files"]
    jira_keys = list(payload.get("jira_keys") or [])
    agent_outputs = payload.get("agent_outputs") if isinstance(payload.get("agent_outputs"), dict) else {}
    diff_summary = str(payload.get("diff_summary") or "")

    jira_lines = "\n".join(f"- `{k}`" for k in jira_keys) if jira_keys else "- (none linked in payload)"

    commit_lines = []
    for c in commits[:40]:
        sha = str((c or {}).get("sha") or "")[:7]
        msg = str((c or {}).get("message") or "").split("\n", 1)[0][:120]
        commit_lines.append(f"- `{sha}` {msg}")
    commits_block = "\n".join(commit_lines) if commit_lines else "- (no commits in payload)"

    file_lines = "\n".join(f"- `{f}`" for f in files[:200]) if files else "- (none)"
    if len(files) > 200:
        file_lines += f"\n- _…and {len(files) - 200} more_"

    agents_blob = json.dumps(agent_outputs, indent=2, default=str) if agent_outputs else "{}"

    testing = "- See CI / local verification noted in agent outputs and repo checks."
    if isinstance(agent_outputs.get("tester"), dict) and (agent_outputs["tester"].get("summary") or "").strip():
        testing = f"- Tester agent: {agent_outputs['tester']['summary']}"

    validation = "- Branch validated via GitHub ref API; Jira keys matched expected pattern."
    if jira_keys:
        validation += f" Linked tickets: {', '.join(jira_keys)}."

    risk = _risk_notes(agent_outputs, diff_summary)
    deploy = _deploy_notes(agent_outputs)

    parts = [
        PR_SECTION_SUMMARY,
        "",
        f"Branch: `{branch}`",
        "",
        "This description was generated from the current diff, commits, linked Jira keys, and agent outputs (no invented changes).",
        "",
        PR_SECTION_JIRA,
        "",
        jira_lines,
        "",
        PR_SECTION_CHANGES,
        "",
        "Diff-derived summary (verbatim excerpt / stats; may be truncated):",
        "",
        "```text",
        diff_summary[:12000] if diff_summary else "(empty)",
        "```",
        "",
        PR_SECTION_AGENTS,
        "",
        "```json",
        agents_blob[:8000],
        "```",
        "",
        PR_SECTION_FILES,
        "",
        file_lines,
        "",
        PR_SECTION_TESTING,
        "",
        testing,
        "",
        PR_SECTION_VALIDATION,
        "",
        validation,
        "",
        PR_SECTION_RISK,
        "",
        risk,
        "",
    ]

    if deploy:
        parts.extend(
            [
                OPTIONAL_DEPLOY_MARKER,
                "",
                deploy,
                "",
            ]
        )

    body = "\n".join(parts)
    for m in REQUIRED_SECTION_MARKERS:
        if m not in body:
            raise ValueError(f"PR formatter invariant failed: missing {m}")
    return body


def assert_non_placeholder_body(body: str) -> None:
    """Reject obviously generic bodies."""
    t = body.lower()
    banned = ("lorem ipsum", "todo: fill", "placeholder pr", "tbd tbd")
    if any(b in t for b in banned):
        raise ValueError("PR body appears to be placeholder or generic")
    if len(body.strip()) < 200:
        raise ValueError("PR body too short to be a substantive description")
