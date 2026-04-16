---
name: orchestration-overview
description: Summarize where to read orchestrator, DAG, and automation agents in this repo
---

# Orchestration overview

1. **Orchestrator (Cursor role)** — `agents/orchestrator/prompt.md`, `agent.md`, `constraints.md`
2. **DAG registry** — `config/agents.json`, `config/orchestration_dag.json`
3. **Traceability** — `.cursor/rules/traceability-jira-github.mdc`, `github/pr_templates.py`, `jira/templates.py`
4. **Python automation** — `agents/AUTOMATION_AGENTS.md`, `agents/jira_story_generator.py`, `agents/github_pr_description_writer.py`

When acting as Orchestrator, set `jira_required` on the work order before delegating.
