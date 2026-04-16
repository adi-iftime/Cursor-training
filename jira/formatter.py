"""Build Jira issue description bodies (markdown) for generated stories."""

from __future__ import annotations

import json
from typing import Any

from jira.templates import REQUIRED_STORY_SECTION_MARKERS, normalize_dependency_keys


def format_jira_story_description(
    *,
    title: str,
    description: str,
    context: dict[str, Any],
    requested_agent: str,
    dependencies: list[str],
) -> str:
    """
    Produce a markdown body containing all REQUIRED_STORY_SECTION_MARKERS in order.

    Extra orchestrator context is included verbatim under Context as JSON for traceability.
    """
    deps = normalize_dependency_keys(dependencies)
    ctx_blob = json.dumps(context, indent=2, sort_keys=True, default=str)

    lines: list[str] = [
        f"# {title.strip()}",
        "",
        "## Context",
        "",
        "Orchestrator-provided context (JSON):",
        "",
        "```json",
        ctx_blob,
        "```",
        "",
        "Narrative:",
        "",
        (description.strip() or "(no description provided)"),
        "",
        "## Acceptance criteria",
        "",
        "- Story maps to a registered agent id and validated Jira dependencies.",
        "- Issue body includes all required sections for this repository.",
        "",
        "## Dependencies",
        "",
    ]
    if deps:
        for d in deps:
            lines.append(f"- {d}")
    else:
        lines.append("- (none)")

    lines.extend(
        [
            "",
            "## Agent assignment",
            "",
            f"- **Assigned agent (registry id):** `{requested_agent}`",
            "",
        ]
    )

    body = "\n".join(lines)
    for marker in REQUIRED_STORY_SECTION_MARKERS:
        if marker not in body:
            raise ValueError(f"formatter invariant failed: missing {marker}")
    return body
