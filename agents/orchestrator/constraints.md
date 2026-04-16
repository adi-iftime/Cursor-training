# Guardrails — Orchestrator (DAG + balanced traceability)

## Source of truth

- **`config/agents.json`**, **`config/orchestration_dag.json`**
- **`jira/templates.py`** — full Story template **when** a Story is created
- **`github/pr_templates.py`** — **universal** PR sections for **every** PR; **`NO_JIRA_STORY_LINE`** when no ticket applies

## Jira (conditional)

- **Feature-level work** → create a Story via **`jira_story_generator`** + Atlassian **MCP** before substantive implementation; all `REQUIRED_STORY_SECTION_MARKERS` must be present.
- **Non-feature work** → **no** Jira Story; do not run `jira_story_generator` for that work order.
- Do not claim Jira updates without MCP evidence.

## GitHub / PR (universal)

- **Every** PR body MUST include all `REQUIRED_SECTION_MARKERS` in `github/pr_templates.py`.
- **Related Jira Story** section MUST contain either linked keys **or** the exact no-Jira sentence **`No Jira story required (non-feature change)`**.
- Use **`github.client.GitHubClient`** for GitHub API updates in this repository.

## Ordering and parallelism

- Never run an agent until **all** of its `dependsOn` entries are satisfied (unless an agent is explicitly out of scope).
- Parallel waves: run eligible agents concurrently per `orchestration_dag.json`.

## Failure rules

- Missing Jira when required → **stop** and create Story.
- Invalid or partial Story when Jira required → **stop** and fix.
- PR missing universal format or Related Jira rule → **stop** and fix.
