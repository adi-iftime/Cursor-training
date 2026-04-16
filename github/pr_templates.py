"""Universal PR description structure — mandatory for all PRs; Jira linkage conditional."""

from __future__ import annotations

# Emoji section headings (###) — must all appear in generated PR bodies.
PR_SECTION_SUMMARY = "### 🧾 Summary"
PR_SECTION_PURPOSE = "### 🎯 Purpose"
PR_SECTION_CHANGES = "### 🧩 Changes"
PR_SECTION_AGENTS = "### 🤖 Agent Contributions"
PR_SECTION_TESTING = "### 🧪 Testing"
PR_SECTION_RISK = "### ⚠️ Risk Notes"
PR_SECTION_RELATED_JIRA = "### 🔗 Related Jira Story"

# When no Jira Story exists (refactor, bugfix, docs-only, etc.) — exact line required in that section.
NO_JIRA_STORY_LINE = "No Jira story required (non-feature change)"

REQUIRED_SECTION_MARKERS: tuple[str, ...] = (
    PR_SECTION_SUMMARY,
    PR_SECTION_PURPOSE,
    PR_SECTION_CHANGES,
    PR_SECTION_AGENTS,
    PR_SECTION_TESTING,
    PR_SECTION_RISK,
    PR_SECTION_RELATED_JIRA,
)
