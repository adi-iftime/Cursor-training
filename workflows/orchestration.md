# Workflow — Orchestration (entry)

1. **User prompt** arrives → only the **Orchestrator** interprets intent (Product Owner + Data Architect lens per `.cursor/agents/orchestrator.md` and `agents/orchestrator/agent.md`).
2. Output: structured **work order** — goal, scope, architecture sketch, data model notes, NFRs (performance, cost, security), `correlation_id`, **`jira_required`** flag.
3. No specialist worker runs before this artifact exists.

**Enforcement:** Cursor rules under `.cursor/rules/`; registry `config/agents.json` lists orchestrator as entry; full narrative in `docs/MULTI_AGENT_BLUEPRINT.md`.

---

## Jira Execution Policy (mandatory)

- **All Jira-related actions** (create/update Epic, Story, Task, subtask, or “write a jira ticket”) **MUST** go through the **Jira Writer Agent** protocol (`.cursor/agents/jira-writer.md` / `.cursor/agents/jira-story-generator.md` — same rules).
- **Plain-text Jira generation** in chat (full description, acceptance criteria, copy-paste blocks) as a **substitute for creating an issue** is **FORBIDDEN** when Atlassian MCP is available.
- **Atlassian MCP** (`createJiraIssue`, `editJiraIssue`, …) usage is **mandatory** for fulfilling “create/write … in Jira” requests.
- A request to create Jira work is **incomplete** until **`createJiraIssue`** (or an MCP edit) **succeeds**, or the agent returns exactly **`MCP tool not available`** per Jira agent policy.
- **Orchestrator** must **delegate** Jira keywords (`jira`, `ticket`, `story`, `epic` in backlog context) per `.cursor/agents/orchestrator.md` — **no bypass**.

**Global:** External systems (Jira, GitHub, etc.) MUST be driven via **tools** (MCP, official APIs, CLI), not simulated ticket/PR text — see `.cursor/rules/mcp-external-systems.mdc`.
