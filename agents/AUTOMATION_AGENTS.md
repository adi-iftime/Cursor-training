# Automation agents (Python modules)

These agents are **invoked by the orchestrator workflow or `orchestrator/pr_lifecycle_orchestrator.py`**, not by a separate framework. They share the same DAG registry ids in `config/agents.json`.

| Registry id | Module | Role |
| --- | --- | --- |
| `jira_story_generator` | `agents/jira_story_generator.py` | Builds a validated Jira **Story** via Atlassian MCP when the orchestrator sets **`jira_required: true`** (feature-level work). |
| `github_pr_description_writer` | `agents/github_pr_description_writer.py` | Builds structured PR bodies and PATCHes via `github.client.GitHubClient`. |

**Jira split:** `jira_story_generator` runs only when the work order is **feature-level** (`jira_required: true`). The **Planner** owns per-task issues and epics. **Every** PR uses `github/pr_templates.py` (Jira links or the no-Jira line).

**GitHub split:** PR review / fix / merge automation lives under `agents/pr_*_agent/` (lifecycle). `github_pr_description_writer` only updates PR description text using the existing client.

**Environment:** Set **`JIRA_BROWSE_BASE`** (e.g. `https://your-site.atlassian.net`) so PR descriptions emit real Jira URLs (`github/pr_formatter.py`).
