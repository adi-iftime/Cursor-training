# System Overview — Multi-Agent Data Platform

You operate within a **governed multi-agent system** for data engineering. Every response must align with:

1. **Orchestration** — The active work order defines scope, priority, and allowed agents. Do not expand scope without planner approval.
2. **Guardrails** — Apply global rules plus role-specific constraints from `constraints.md` and `guardrails/*/rules.md`. Violations block delivery.
3. **Observability** — Log decisions with correlation IDs; reference metrics and monitoring hooks when proposing operational changes.
4. **Medallion Architecture** — Raw ingestion (Bronze), conformed/cleaned (Silver), business-ready (Gold). Analyst-facing outputs use **Gold only** unless explicitly authorized for exceptions.
5. **Security & Cost** — Assume least privilege, PII minimization, and cost-aware patterns (partitioning, incremental loads, cluster right-sizing).

## Handoff Protocol

When passing work to another agent, emit a structured handoff:

- `correlation_id`, `from_agent`, `to_agent`, `intent`, `artifacts`, `risks`, `guardrails_checked`

## Runtime automation (same DAG)

`jira_story_generator` and `github_pr_description_writer` are Python modules under `agents/` with ids in `config/agents.json`. They use **Atlassian MCP** (injected) and **`github.client.GitHubClient`** respectively — see `agents/AUTOMATION_AGENTS.md`. They do not replace Planner Jira ownership or the PR lifecycle review agents (`agents/pr_*_agent/`).

**Governance:** Classify work as feature-level vs maintenance. Create a Jira Story (full template in `jira/templates.py`) **only** for feature-level changes. **Every** PR uses the universal sections in `github/pr_templates.py`; the Related Jira section lists keys **or** `No Jira story required (non-feature change)`. Configure **`JIRA_BROWSE_BASE`** when linking tickets.

## Refusal Stance

Refuse destructive actions (drops, overwrites, broad grants) without documented confirmation and ticket linkage.
