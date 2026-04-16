# Multi-Agent Data Platform (Scaffold)

Production-oriented scaffold for **governed data engineering** with specialized agents, reusable skills, guardrails, and observability hooks.

## Layout


| Path          | Purpose                                                                    |
| ------------- | -------------------------------------------------------------------------- |
| `agents/`     | Agent definitions: `agent.md`, `prompt.md`, `tools.json`, `constraints.md` |
| `skills/`     | Reusable capabilities with `skill.md`, `examples.md`, `interfaces.json`    |
| `guardrails/` | Global and domain rules: `rules.md`, `checks.md`, `examples.md`            |
| `config/`     | `agents.json`, `orchestration.json`, `guardrails.json`, `skills.json`      |
| `prompts/`    | Shared prompts (e.g. `system_overview.md`)                                 |
| `utils/`      | Helpers and logging standards                                              |
| `examples/`   | Sample request, orchestration flow, example outputs                        |


## Quick start

1. Read `prompts/system_overview.md` and `config/orchestration.json` for the canonical flow.
2. Map runtime tool adapters to `agents/*/tools.json` and `skills/*/interfaces.json`.
3. Enforce guardrails via automated checks aligned with `guardrails/*/checks.md`.

## Observability

See `utils/logging_spec.md` for structured logging, metrics, and pipeline monitoring hooks.

## Extension

Add agents or skills by copying an existing folder pattern and registering entries in `config/agents.json` and `config/skills.json`.