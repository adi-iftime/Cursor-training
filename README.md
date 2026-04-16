# Multi-agent product engineering blueprint

Reusable **Cursor** blueprint for governed software delivery: **Orchestrator → Planner → parallel workers → validate → PR → merge**.

## Start here

| Resource | Purpose |
| --- | --- |
| [docs/MULTI_AGENT_BLUEPRINT.md](docs/MULTI_AGENT_BLUEPRINT.md) | Full architecture, agent I/O, parallel execution, security/cost gates, example prompt flow |
| [workflows/orchestration.md](workflows/orchestration.md) | Mandatory orchestrator entry |
| [workflows/planning.md](workflows/planning.md) | Planner and backlog |
| [workflows/execution.md](workflows/execution.md) | Parallel workers, ownership, sync points |
| [workflows/pr-process.md](workflows/pr-process.md) | git + `gh` delivery |
| [standards/](standards/) | coding, architecture, data, testing, security, cost |
| [.cursor/agents/](.cursor/agents/) | Cursor-facing agent definitions (YAML + role docs) |
| [config/agents.json](config/agents.json) | DAG registry for automation |

## Repository shape (this project)

| Path | Purpose |
| --- | --- |
| `agents/` | Rich agent packages: `agent.md`, `prompt.md`, `tools.json`, `constraints.md` |
| `skills/` | Reusable capabilities |
| `guardrails/` | Domain rules |
| `config/` | Agents, orchestration, guardrails, skills |
| `prompts/` | Shared prompts |
| `utils/` | Helpers and logging |
| `examples/` | Sample flows |

## Quick start

1. Read `docs/MULTI_AGENT_BLUEPRINT.md`.
2. Open `.cursor/agents/orchestrator.md` for the entry role; use `planner.md` and worker agents as needed.
3. Enforce policies via `.cursor/rules/` and `config/agents.json`.

## Observability

See `utils/logging_spec.md` for structured logging and correlation ids.

## Extension

Add agents by following an existing folder under `agents/`, registering in `config/agents.json`, and adding a stub under `.cursor/agents/` if Cursor should surface the role.
