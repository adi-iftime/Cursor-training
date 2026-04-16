# Automation agents (Python modules)

These agents are **invoked by the orchestrator workflow or `orchestrator/pr_lifecycle_orchestrator.py`**, not by a separate framework. They share the same DAG registry ids in `config/agents.json`.

| Registry id | Module | Role |
| --- | --- | --- |
| `jira_story_generator` | `agents/jira_story_generator.py` | Builds a validated Jira **Story** via Atlassian MCP (`mcp_invoke`); upstream of planner for traceability. |
| `github_pr_description_writer` | `agents/github_pr_description_writer.py` | Builds structured PR bodies and PATCHes via `github.client.GitHubClient`. |

**Jira split:** `jira_story_generator` creates the **orchestrator-scoped Story** from the normalized task payload. The **Planner** agent remains responsible for **per-task** issue creation, epics, and ongoing Jira updates per `agents/planner/agent.md`.

**GitHub split:** PR review / fix / merge automation lives under `agents/pr_*_agent/` (lifecycle). `github_pr_description_writer` only updates PR description text using the existing client.
