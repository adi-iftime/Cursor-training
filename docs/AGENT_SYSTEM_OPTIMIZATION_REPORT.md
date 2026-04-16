# Agent system optimization report

**Scope:** `/agents`, `config/guardrails.json`, `config/skills.json`, `config/agents.json`, `config/orchestration_dag.json`, Cursor rules under `.cursor/rules/`, and related prompts.

**Date:** 2026-04-16 (repository state).

---

## 1. System analysis summary

### Architecture issues (addressed or documented)

| Issue | Finding |
| --- | --- |
| **Guardrail coverage gaps** | `guardrails.json` listed only five `byAgent` paths while the DAG has more agents. **data_governance** had no mapped guardrail directory. Coordination agents (orchestrator, planner, tester, devops, documentation) had no explicit mapping. |
| **Jira responsibility overlap** | Planner `agent.md` stated exclusive Jira creation ownership while **`jira_story_generator`** also creates Stories via MCP. Risk: conflicting instructions for Cursor sessions. |
| **Skills ↔ agents drift** | `jira_story_generator`, `github_pr_description_writer`, and PR-description workflows were absent from `skills.json` ownership, weakening discoverability. |
| **Automation vs prompt agents** | Python modules (`jira_story_generator.py`, `github_pr_description_writer.py`) live alongside folder-based agents without a single index; onboarding cost. |
| **Orchestration rules** | `orchestration_dag.json` rules did not distinguish GitHub *product* client use from PR *lifecycle* agents. |

### Redundant agents

- **No merges performed.** `agents/pr_review_agent`, `pr_fixer_agent`, `pr_rereview_agent`, and `auto_merge_agent` are **not** duplicated by `github_pr_description_writer`; they address lifecycle review/fix/merge. Domain DAG agents (data_engineer, data_quality, etc.) remain non-overlapping in responsibility.
- **Planner vs jira_story_generator** is complementary, not redundant, once ownership is explicit (Story vs per-task backlog).

### Missing capabilities (partially closed)

| Gap | Mitigation in repo |
| --- | --- |
| Explicit governance guardrails | Added `guardrails/data_governance/{rules,checks}.md`. |
| Platform coordination guardrails | Added `guardrails/platform_agent/{rules,checks}.md` and mapped coordination + automation agents in `config/guardrails.json`. |
| Discoverability of automation agents | Added `agents/AUTOMATION_AGENTS.md` and cross-links in orchestrator + system overview. |

### Skills inconsistencies (resolved in registry)

- **Jira:** `jira_story_generator` elevated to **primary** (with planner); **github_pr_description_writer** added as secondary (ticket linking in PRs).
- **GitHub:** `github_pr_description_writer` added as **primary** (with documentation, devops); `jira_story_generator` secondary for cross-links.

### Guardrail problems (before)

- Incomplete `byAgent` matrix; enforcement tooling (if any) could not route all agents to a ruleset.
- Global rules existed but several agents had no **downstream** checks file pointer.

---

## 2. Proposed improvements (implemented)

| Change | Why | Files |
| --- | --- | --- |
| **Platform agent guardrails** | Single coherent ruleset for coordination/automation agents; enforces MCP/GitHubClient boundaries and correlation IDs. | `guardrails/platform_agent/*`, `config/guardrails.json` |
| **Data governance guardrails** | Aligns registry agent with explicit contract/lineage rules. | `guardrails/data_governance/*`, `config/guardrails.json` |
| **Full `byAgent` mapping** | Every DAG agent id maps to a guardrail path. | `config/guardrails.json` |
| **Skills registry alignment** | Skills reflect Jira/ GitHub automation agents. | `config/skills.json` |
| **Clarify Jira split** | Removes Planner vs Story-generator conflict. | `agents/planner/agent.md` |
| **Automation index** | One place describes Python modules vs prompt agents. | `agents/AUTOMATION_AGENTS.md`, `agents/orchestrator/agent.md`, `prompts/system_overview.md` |
| **DAG + Cursor rules** | Clearer Jira/GitHub/automation semantics. | `config/orchestration_dag.json`, `.cursor/rules/orchestrator-dag.mdc` |
| **Version bumps** | Trace config evolution (`1.1.0`). | `config/agents.json`, `config/skills.json`, `config/guardrails.json`, `config/orchestration_dag.json` |

---

## 3. Modified artifacts (inventory)

- `config/guardrails.json`
- `config/skills.json`
- `config/agents.json` (version)
- `config/orchestration_dag.json` (version + rules)
- `guardrails/platform_agent/rules.md`, `guardrails/platform_agent/checks.md` (**new**)
- `guardrails/data_governance/rules.md`, `guardrails/data_governance/checks.md` (**new**)
- `agents/planner/agent.md`
- `agents/orchestrator/agent.md`
- `agents/AUTOMATION_AGENTS.md` (**new**)
- `prompts/system_overview.md`
- `.cursor/rules/orchestrator-dag.mdc`
- `docs/AGENT_SYSTEM_OPTIMIZATION_REPORT.md` (this file)

---

## 4. Risk assessment

| Risk | Impact | Mitigation |
| --- | --- | --- |
| **Stricter guardrail paths** | External automation expecting old `byAgent` keys only | Keys expanded, not removed; existing domain paths unchanged. |
| **Planner prompt change** | Sessions might still batch tasks if old habits | Cursor rules + planner `agent.md` now aligned; review in team channels. |
| **Skills.json primaryAgents** | Downstream tools that assume single primary per skill | Now two primaries for jira/github — document as intentional shared ownership. |
| **No automated enforcement** | JSON guardrails mapping is declarative | CI could add a lint: every `agents.json` id ∈ `guardrails.byAgent` keys. |

### Dependencies impacted

- **Orchestrator / Planner** documentation and Cursor rules — behaviorally unchanged; clarity only.
- **MCP / GitHub** — no code path changes to `agents/jira_story_generator.py` or `github/` in this refactor.
- **Tests** — `tests/test_config_json.py`, `tests/test_agents_graph.py` should remain green (JSON still valid; graph still consistent).

---

## 5. Non-goals (explicit)

- No removal of core domain agents or merger of `pr_*_agent` with DAG agents.
- No new orchestration engine or external framework.
- No change to Python agent APIs beyond documentation.
