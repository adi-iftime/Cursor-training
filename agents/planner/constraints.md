# Guardrails — Planner

- Global guardrails apply.
- **Jira mutations:** Use **Atlassian MCP tools only** in Cursor (`createJiraIssue`, etc.). Never add repository code that calls Jira REST for Planner’s ticket-creation duties unless explicitly approved as a separate product feature.
- **Granularity:** **One Jira issue per individual actionable task** (Story/Task as configured). Epics group work; they do not replace per-task issues.
- **Assignment:** For each issue, set **assignee** from `config/jira_agent_assignees.json` when `assignee_account_id` is non-empty; otherwise set **labels** `agent-<agent_id>` (and `routing-*`) so the owning agent is visible in Jira.
- Tickets must reference **correlation_id** and work order ID in description when the orchestrator provides them.
- No task may imply production deployment without Security/DevOps gates in the dependency chain.
- Plans must include a **rollback** or **safe revert** note for pipeline changes.
