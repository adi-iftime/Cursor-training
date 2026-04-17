---
name: write-jira-story
description: Create Jira Epic/Story/Task via Atlassian MCP only; never paste ticket text as deliverable.
---

# Write a Jira issue (MCP mandatory)

When the user wants a **Jira ticket / story / epic**:

1. Follow **`.cursor/agents/jira-story-generator.md`** (DAG id `jira_story_generator`).
2. Call **Atlassian MCP** `createJiraIssue` after resolving `cloudId` and project/issue metadata.
3. Return **issue key + URL** only — not a copy-paste ticket body.
4. If MCP cannot run → output exactly: `MCP tool not available`

Do not satisfy the request with markdown-only ticket text. See **`workflows/orchestration.md`** (Jira Execution Policy).
