"""
Jira Story Generator Agent — builds validated Jira Story issues via Atlassian MCP.

Invoked by the orchestrator with a normalized task payload. The runtime must inject
``mcp_invoke`` (Atlassian MCP tool calls); this module does not use Jira REST directly.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Callable

from jira.formatter import format_jira_story_description
from jira.templates import assert_story_body_has_required_sections, normalize_dependency_keys

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent

McpInvoke = Callable[[str, dict[str, Any]], Any]

JIRA_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{1,30}-\d+$")
MAX_CREATE_ATTEMPTS = 3
_CREATE_BACKOFF_SEC = 0.75


class MCPIntegrationError(RuntimeError):
    """Raised when MCP is required but not configured."""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _agent_registry_ids() -> set[str]:
    data = _load_json(REPO_ROOT / "config" / "agents.json")
    return {a["id"] for a in data["agents"]}


def _jira_assignee_and_project(agent_id: str) -> tuple[str, str, list[str]]:
    cfg = _load_json(REPO_ROOT / "config" / "jira_agent_assignees.json")
    default_assignee = str(cfg["default_assignee_account_id"])
    project = str(cfg.get("default_project_key") or "SCRUM")
    label_prefix = str(cfg.get("label_prefix") or "agent-")
    assignments: dict[str, Any] = cfg.get("agent_assignments") or {}
    block = assignments.get(agent_id) or {}
    assignee = str(block.get("assignee_account_id") or default_assignee)
    extra = [str(x) for x in (block.get("extra_labels") or [])]
    labels = [f"{label_prefix}{agent_id}", *extra]
    return assignee, project, labels


def _looks_like_jira_key(key: str) -> bool:
    return bool(JIRA_KEY_PATTERN.match(key.strip()))


def _parse_issue_key(payload: Any) -> str:
    if isinstance(payload, dict):
        if isinstance(payload.get("key"), str):
            return payload["key"]
        for k in ("issue", "data", "issueData"):
            inner = payload.get(k)
            if isinstance(inner, dict) and isinstance(inner.get("key"), str):
                return inner["key"]
    raise ValueError(f"Cannot parse Jira issue key from MCP payload: {payload!r}")


def _parse_issue_status(payload: Any) -> str:
    if not isinstance(payload, dict):
        return "unknown"
    fields = payload.get("fields")
    if isinstance(fields, dict):
        st = fields.get("status")
        if isinstance(st, dict) and isinstance(st.get("name"), str):
            return st["name"]
    return str(payload.get("status") or "unknown")


def _validate_dependencies_keys(deps: list[str]) -> None:
    bad = [d for d in deps if not _looks_like_jira_key(d)]
    if bad:
        raise ValueError(f"Invalid Jira key format for dependencies: {bad}")


def _validate_dependency_issues_exist(
    mcp_invoke: McpInvoke,
    *,
    cloud_id: str,
    keys: list[str],
) -> None:
    for key in keys:
        logger.info("jira_story_generator validating dependency issue key=%s", key)
        out = mcp_invoke(
            "getJiraIssue",
            {"cloudId": cloud_id, "issueIdOrKey": key, "responseContentFormat": "markdown"},
        )
        if isinstance(out, dict) and out.get("error"):
            raise ValueError(f"Dependency issue not found or inaccessible: {key} ({out.get('error')})")


def _create_issue_with_retries(
    mcp_invoke: McpInvoke,
    *,
    cloud_id: str,
    project_key: str,
    summary: str,
    description: str,
    assignee_account_id: str,
    additional_fields: dict[str, Any],
) -> dict[str, Any]:
    last_err: Exception | None = None
    for attempt in range(1, MAX_CREATE_ATTEMPTS + 1):
        try:
            logger.info(
                "jira_story_generator MCP createJiraIssue attempt=%s/%s",
                attempt,
                MAX_CREATE_ATTEMPTS,
            )
            result = mcp_invoke(
                "createJiraIssue",
                {
                    "cloudId": cloud_id,
                    "projectKey": project_key,
                    "issueTypeName": "Story",
                    "summary": summary,
                    "description": description,
                    "assignee_account_id": assignee_account_id,
                    "additional_fields": additional_fields,
                    "contentFormat": "markdown",
                    "responseContentFormat": "markdown",
                },
            )
            logger.info("jira_story_generator MCP createJiraIssue response received")
            return result if isinstance(result, dict) else {"raw": result}
        except Exception as exc:  # noqa: BLE001 — surface after retries
            last_err = exc
            logger.exception(
                "jira_story_generator createJiraIssue failed attempt=%s/%s",
                attempt,
                MAX_CREATE_ATTEMPTS,
            )
            if attempt < MAX_CREATE_ATTEMPTS:
                time.sleep(_CREATE_BACKOFF_SEC * attempt)
    assert last_err is not None
    raise last_err


def _fetch_status(
    mcp_invoke: McpInvoke,
    *,
    cloud_id: str,
    issue_key: str,
) -> str:
    out = mcp_invoke(
        "getJiraIssue",
        {
            "cloudId": cloud_id,
            "issueIdOrKey": issue_key,
            "fields": ["status"],
            "responseContentFormat": "markdown",
        },
    )
    if isinstance(out, dict):
        return _parse_issue_status(out)
    return "unknown"


def run(
    task: dict[str, Any],
    *,
    mcp_invoke: McpInvoke | None = None,
    cloud_id: str | None = None,
    project_key: str | None = None,
) -> dict[str, Any]:
    """
    Execute Jira Story creation from an orchestrator work order.

    Parameters
    ----------
    task:
        ``title``, ``description``, ``context``, ``requested_agent``, ``dependencies``.
    mcp_invoke:
        Callable(tool_name, arguments) implementing Atlassian MCP (e.g. createJiraIssue).
    cloud_id:
        Atlassian cloud id; falls back to task['context']['cloud_id'] or env ATLASSIAN_CLOUD_ID.
    project_key:
        Jira project key; falls back to task context or jira_agent_assignees.json default.
    """
    if mcp_invoke is None:
        msg = "mcp_invoke is required (Atlassian MCP); direct Jira REST is not supported here."
        logger.error("jira_story_generator %s", msg)
        raise MCPIntegrationError(msg)

    try:
        title = str(task["title"])
        description = str(task.get("description") or "")
        context = task.get("context") if isinstance(task.get("context"), dict) else {}
        requested_agent = str(task["requested_agent"])
        dependencies = normalize_dependency_keys(list(task.get("dependencies") or []))
    except (KeyError, TypeError) as exc:
        logger.exception("jira_story_generator invalid task shape")
        raise ValueError(f"Invalid task payload: {exc}") from exc

    logger.info(
        "jira_story_generator incoming task title=%r requested_agent=%s deps=%s",
        title,
        requested_agent,
        dependencies,
    )

    registry = _agent_registry_ids()
    if requested_agent not in registry:
        msg = f"requested_agent not in registry: {requested_agent!r}"
        logger.error(msg)
        raise ValueError(msg)

    _validate_dependencies_keys(dependencies)

    ctx = dict(context)
    cid = cloud_id or str(ctx.get("cloud_id") or os.environ.get("ATLASSIAN_CLOUD_ID") or "").strip()
    if not cid:
        msg = "cloud_id missing: set task['context']['cloud_id'] or ATLASSIAN_CLOUD_ID"
        logger.error(msg)
        raise ValueError(msg)

    assignee_id, default_project, base_labels = _jira_assignee_and_project(requested_agent)
    proj = str(project_key or ctx.get("project_key") or default_project).strip()

    body = format_jira_story_description(
        title=title,
        description=description,
        context=ctx,
        requested_agent=requested_agent,
        dependencies=dependencies,
    )
    assert_story_body_has_required_sections(body)
    logger.info("jira_story_generator generated Jira story body (length=%s)", len(body))

    _validate_dependency_issues_exist(mcp_invoke, cloud_id=cid, keys=dependencies)
    logger.info("jira_story_generator dependency validation passed")

    labels = list(dict.fromkeys([*base_labels, "orchestrator-jira-story"]))
    additional_fields: dict[str, Any] = {"labels": labels}

    create_payload = _create_issue_with_retries(
        mcp_invoke,
        cloud_id=cid,
        project_key=proj,
        summary=title,
        description=body,
        assignee_account_id=assignee_id,
        additional_fields=additional_fields,
    )

    try:
        issue_key = _parse_issue_key(create_payload)
    except ValueError:
        logger.exception("jira_story_generator could not parse issue key from MCP response: %s", create_payload)
        raise

    status_name = _fetch_status(mcp_invoke, cloud_id=cid, issue_key=issue_key)

    result = {
        "jira_key": issue_key,
        "summary": title,
        "assigned_agent": requested_agent,
        "status": status_name,
    }
    logger.info("jira_story_generator completed %s", result)
    return result
