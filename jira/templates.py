"""Strict Jira Story body structure — orchestrator-enforced standard."""

from __future__ import annotations

import re
from typing import Iterable

# All sections MUST appear in generated Story descriptions (## headings).
REQUIRED_STORY_SECTION_MARKERS: tuple[str, ...] = (
    "## Summary",
    "## Description",
    "## Goal",
    "## Scope",
    "## Assigned agents",
    "## Dependencies",
    "## File and module impact",
    "## Acceptance criteria",
    "## Testing requirements",
    "## Implementation notes",
    "## Edge cases",
    "## Definition of Done",
)

_SECTION_PATTERN = re.compile(r"^##\s+.+$", re.MULTILINE)


def story_sections_checklist() -> list[str]:
    """Human-readable checklist for prompts and validation logs."""
    return [f"- {m}" for m in REQUIRED_STORY_SECTION_MARKERS]


def assert_story_body_has_required_sections(body: str) -> None:
    """Raise ValueError if any required section heading is missing."""
    missing = [m for m in REQUIRED_STORY_SECTION_MARKERS if m not in body]
    if missing:
        raise ValueError(f"Missing required Jira story sections: {missing}")


def count_section_headings(body: str) -> int:
    """Count '##' headings (lightweight sanity check)."""
    return len(_SECTION_PATTERN.findall(body))


def normalize_dependency_keys(raw: Iterable[str]) -> list[str]:
    """Return stripped, de-duplicated dependency keys preserving order."""
    seen: set[str] = set()
    out: list[str] = []
    for item in raw:
        key = str(item).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out
