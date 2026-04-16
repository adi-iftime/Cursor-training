"""PR description section ordering and markers for the GitHub PR Description Writer agent."""

from __future__ import annotations

# Markdown H2 headings — keep stable for automation and human skim.
PR_SECTION_SUMMARY = "## Summary"
PR_SECTION_JIRA = "## Related Jira tickets"
PR_SECTION_CHANGES = "## Changes overview"
PR_SECTION_AGENTS = "## Agent execution summary"
PR_SECTION_FILES = "## Files modified"
PR_SECTION_TESTING = "## Testing performed"
PR_SECTION_VALIDATION = "## Validation notes"
PR_SECTION_RISK = "## Risk assessment"
PR_SECTION_DEPLOY = "## Deployment notes"

REQUIRED_SECTION_MARKERS: tuple[str, ...] = (
    PR_SECTION_SUMMARY,
    PR_SECTION_JIRA,
    PR_SECTION_CHANGES,
    PR_SECTION_AGENTS,
    PR_SECTION_FILES,
    PR_SECTION_TESTING,
    PR_SECTION_VALIDATION,
    PR_SECTION_RISK,
)

OPTIONAL_DEPLOY_MARKER = PR_SECTION_DEPLOY
