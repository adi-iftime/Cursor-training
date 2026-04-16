---
name: write-jira-story
description: Create or update Jira epic/story for a feature or app using Atlassian MCP (not file-only)
---

# Write a Jira story (Atlassian MCP)

When the user asks for a **Jira story**, **epic**, or **backlog** for a **new feature** or **application**:

1. Follow **`.cursor/rules/jira-atlassian-mcp-stories.mdc`** — use **Atlassian MCP** to create/update issues.
2. Resolve **`cloudId`** with `getAccessibleAtlassianResources`; resolve **project key** with `getVisibleJiraProjects` or ask the user.
3. Use `getJiraIssueTypeMetaWithFields` / `getJiraProjectIssueTypesMetadata` for required fields.
4. Call `createJiraIssue` with `contentFormat: "markdown"` for the description.
5. Use **`docs/JIRA_STORY_MULTI_AGENT_BLUEPRINT.md`** as the **format reference** for sections (Summary, user story, description, acceptance criteria).

Optional: save a copy under `docs/jira/` for the repo audit trail **after** the Jira issue exists, and link the Jira key in the doc footer.
