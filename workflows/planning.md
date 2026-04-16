# Workflow — Planning

1. **Input:** Orchestrator work order.
2. **Planner** produces: epics/stories/tasks, dependency DAG, parallel groups, **agent assignments** per task (`.cursor/agents/planner.md`, `agents/planner/agent.md`).
3. **Jira:** Backlog updates via Atlassian MCP (Planner-owned); optional **Jira Writer** for orchestrator-scoped Stories when `jira_required: true`.
4. **Output:** Task graph consumed by execution phase; no implementation without accepted plan slice for the current increment.
