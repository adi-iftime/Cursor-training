---
name: jira-github-traceability
description: >-
  Applies balanced Jira and universal GitHub PR rules: classifies jira_required for
  feature-level work, uses Atlassian MCP for Jira writes, GitHubClient for PR bodies,
  and enforces github/pr_templates.py including Related Jira or NO_JIRA_STORY_LINE.
  Use when creating Stories, opening PRs, or reviewing traceability.
---

# Jira + GitHub traceability

## Jira (conditional)

- Create a Jira **Story** via `jira_story_generator` + MCP only when work is **feature-level** (`jira_required: true`).
- Skip Jira for refactors, minor fixes, config-only, docs-only, dependency bumps, etc.
- When a Story is created, the body must include every `##` section in `jira/templates.py`.

## GitHub (every PR)

- Follow `github/pr_templates.py`: Summary → Purpose → Changes → Agent Contributions → Testing → Risk Notes → Related Jira Story.
- Under **Related Jira Story**: list `- KEY: URL` (set `JIRA_BROWSE_BASE`) **or** the exact line `No Jira story required (non-feature change)`.

## Cursor rules

- `.cursor/rules/traceability-jira-github.mdc`
- `.cursor/rules/planner-jira-atlassian-mcp.mdc`
