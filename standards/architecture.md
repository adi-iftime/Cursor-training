# Architecture standards (blueprint)

- **Layers:** Prefer clear boundaries — API / domain / data access; avoid leaking storage details into UI or orchestration prompts.
- **Data:** Medallion-style thinking where applicable (Bronze → Silver → Gold); contracts owned before implementation (`agents/data_governance`).
- **Orchestration:** Single entry through **Orchestrator**; execution only from **Planner** task graph (`config/agents.json` + DAG).
- **Integrations:** Jira via Atlassian MCP; GitHub product API via `github.client.GitHubClient` — no duplicate HTTP stacks.
- **Parallelism:** Independent tasks run in parallel waves; synchronization at merge and governance gates (see `workflows/execution.md`).
