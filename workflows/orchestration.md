# Workflow — Orchestration (entry)

1. **User prompt** arrives → only the **Orchestrator** interprets intent (Product Owner + Data Architect lens per `.cursor/agents/orchestrator.md` and `agents/orchestrator/agent.md`).
2. Output: structured **work order** — goal, scope, architecture sketch, data model notes, NFRs (performance, cost, security), `correlation_id`, **`jira_required`** flag.
3. No specialist worker runs before this artifact exists.

**Enforcement:** Cursor rules under `.cursor/rules/`; registry `config/agents.json` lists orchestrator as entry; full narrative in `docs/MULTI_AGENT_BLUEPRINT.md`.
