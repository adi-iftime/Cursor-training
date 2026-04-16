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
    Produce a markdown body containing all REQUIRED_STORY_SECTION_MARKERS.

    Optional orchestrator fields may be supplied on ``context``:
    ``goal``, ``scope_included``, ``scope_excluded``, ``file_module_impact``,
    ``testing_requirements``, ``implementation_notes``, ``edge_cases``,
    ``definition_of_done`` (strings or lists coerced to text).
    """
    deps = normalize_dependency_keys(dependencies)
    ctx_blob = json.dumps(context, indent=2, sort_keys=True, default=str)

    def _txt(key: str, default: str = "(not specified — orchestrator must fill before implementation)") -> str:
        v = context.get(key)
        if v is None:
            return default
        if isinstance(v, (list, tuple)):
            return "\n".join(f"- {x}" for x in v) if v else default
        return str(v).strip() or default

    scope_inc = _txt("scope_included")
    scope_exc = _txt("scope_excluded")

    lines: list[str] = [
        f"# {title.strip()}",
        "",
        "## Summary",
        "",
        title.strip(),
        "",
        "## Description",
        "",
        (description.strip() or "(no description provided)"),
        "",
        "Orchestrator context (JSON, traceability):",
        "",
        "```json",
        ctx_blob,
        "```",
        "",
        "## Goal",
        "",
        _txt("goal", "(orchestrator: state the objective)"),
        "",
        "## Scope",
        "",
        "**Included**",
        "",
        scope_inc,
        "",
        "**Excluded**",
        "",
        scope_exc,
        "",
        "## Assigned agents",
        "",
        f"- **Primary (registry id):** `{requested_agent}`",
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
            "## File and module impact",
            "",
            _txt("file_module_impact", "(list paths/modules touched or TBD)"),
            "",
            "## Acceptance criteria",
            "",
            _txt(
                "acceptance_criteria",
                "- Deliverable meets work order; tests pass; guardrails satisfied.",
            ),
            "",
            "## Testing requirements",
            "",
            _txt("testing_requirements", "- Unit/integration as applicable; CI green."),
            "",
            "## Implementation notes",
            "",
            _txt("implementation_notes", "(constraints, libraries, rollout notes)"),
            "",
            "## Edge cases",
            "",
            _txt("edge_cases", "(failure modes, idempotency, data edge cases)"),
            "",
            "## Definition of Done",
            "",
            _txt(
                "definition_of_done",
                "- Jira Story accepted; PR merged with Jira link; docs updated if required.",
            ),
            "",
        ]
    )

    body = "\n".join(lines)
    for marker in REQUIRED_STORY_SECTION_MARKERS:
        if marker not in body:
            raise ValueError(f"formatter invariant failed: missing {marker}")
    return body
