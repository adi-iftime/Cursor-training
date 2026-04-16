# Jira documentation (optional mirror)

When **`.cursor/rules/jira-atlassian-mcp-stories.mdc`** applies, the **system of record** for stories and epics is **Jira**, created via the **Atlassian MCP** (`createJiraIssue`, etc.).

Use this folder only when you want a **local mirror** of an issue body **after** creation, for example:

`docs/jira/PROJ-123-feature-name.md` — paste the Jira description back from Jira or duplicate the markdown used in `createJiraIssue`.

**Canonical blueprint story template (field layout + MCP steps):** [`../JIRA_STORY_MULTI_AGENT_BLUEPRINT.md`](../JIRA_STORY_MULTI_AGENT_BLUEPRINT.md)
