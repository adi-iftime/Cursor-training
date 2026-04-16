---
name: multi-agent-orchestration
description: >-
  Operates the governed multi-agent DAG for this repository: reads config/agents.json
  and config/orchestration_dag.json, respects dependsOn and parallel waves, and delegates
  to specialist agents. Use when scheduling agents, explaining wave order, or validating
  the orchestration graph.
---

# Multi-agent orchestration (this repo)

## Source files

- `config/agents.json` — agent ids, `dependsOn`, `outputsTo`
- `config/orchestration_dag.json` — waves, parallelism notes
- `config/orchestration.json` — linear flow narrative
- `agents/orchestrator/` — orchestrator prompts and constraints

## Rules

1. Never invent agent ids; use only those registered in `config/agents.json`.
2. Do not run an agent until every entry in its `dependsOn` list is satisfied.
3. In waves with `parallel: true`, run all eligible agents concurrently when dependencies allow.
4. Reference `agents/AUTOMATION_AGENTS.md` for Python modules `jira_story_generator` and `github_pr_description_writer`.

## Quick validation

From repo root: `python -m pytest tests/test_agents_graph.py -q`
