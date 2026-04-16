# Multi-Agent Product Engineering Blueprint

Reusable blueprint for building a **governed AI engineering team** in **Cursor**: every substantive request flows **Orchestrator → Planner → specialized workers → validation → pull request → merge**. This repository packages **agent role definitions**, **workflows**, **standards**, and **automation hooks** so teams can adopt a consistent operating model across projects.

---

## Overview

This repository is a **reference implementation and template**, not a single deployed “AI runtime.” It provides:

- **Orchestrator** — Interprets user intent as a Product Owner and applies a Data Architect lens (data boundaries, scalability, cost, security).
- **Planner** — Breaks work into a **directed acyclic graph (DAG)** of tasks with explicit **dependencies** and **parallel groups**.
- **Worker agents** — Implement, test, analyze, and review within **scoped ownership** (paths, branches, or tasks per increment).
- **PR workflow** — Delivery through **Git** and **GitHub** (`gh`): PR authoring, review, fixes, merge — aligned with branch protection and CI.

The blueprint is expressed as markdown in **`.cursor/agents/`**, **`workflows/`**, **`standards/`**, deeper prompts under **`agents/`**, and registry metadata in **`config/agents.json`**. Teams copy or fork this structure into new repositories and tune agents, tools, and policies for their stack.

---

## How It Works

```text
User prompt
    → Orchestrator (work order: goal, architecture/data sketch, constraints, NFRs, correlation_id)
    → Planner (epics/stories/technical tasks, DAG, parallel groups, agent assignments)
    → Parallel workers (implementation + gates: testing, security, cost, data governance as planned)
    → PR Writer (title/body, test plan, risk)
    → PR Reviewer (quality, architecture, security, tests)
    → PR Fixer (addresses feedback)
    → Merge (policy-compliant)
```

**Orchestrator-first** means implementation agents consume a **planned task** and **ownership boundary**, not a raw ambiguous prompt. **Planner** is the control plane for sequencing and parallelism. **PR workflow** is the delivery plane for integrating change safely.

---

## Architecture

| Layer | Responsibility |
| --- | --- |
| **Orchestration** | Single entry interpretation; NFR capture; optional `jira_required`; correlation for tracing. |
| **Planning** | Task graph, dependencies, parallel execution groups, worker assignment. |
| **Execution** | Workers implement or analyze per task; conflicts avoided via ownership rules and sync points (see `workflows/execution.md`). |
| **Validation** | Automated tests, CI, security and cost reviews as defined in the plan. |
| **Delivery** | PR lifecycle: author → review → fix → merge (`workflows/pr-process.md`). |

Optional **Jira** integration: **Jira Story Writer** keeps backlog items aligned with the orchestrator/planner artifacts when policy or flags require it.

---

## Agent Roles

For each role: **what it does**, **when it is used**.

| Agent | Role | Responsibilities | When it is used |
| --- | --- | --- | --- |
| **Orchestrator** | Product Owner + Data Architect | Clarifies goals; defines scope, architecture and data model sketches, constraints, NFRs; emits structured work order. | **Every** substantive new request or major change — **mandatory entry**. |
| **Planner** | Technical program / delivery lead | Decomposes work; builds DAG; assigns agents; identifies parallel work. | After orchestrator work order; **before** parallel implementation at scale. |
| **Jira Story Writer** | Backlog author | Creates/updates Jira epics/stories; traceability to branches/PRs. | When Jira is required or team mandates ticket linkage. |
| **Backend Developer** | Server-side engineer | APIs, services, jobs, infra-as-code in scope; tests; operational notes. | Tasks touching server/runtime/back-end code paths. |
| **Frontend Developer** | Client-side engineer | UI implementation, client tests, accessibility baseline. | Tasks touching UI or client bundles. |
| **Data Engineer** | Pipeline / transformation engineer | Pipelines, jobs, transformations, catalog integration; idempotency and tests. | Data movement, modeling, or orchestration work. |
| **Tester** | Quality engineer | Test plans, automation, defect reporting; CI interpretation. | After or alongside implementation; before merge. |
| **Security Engineer** | AppSec / security reviewer | Secrets, privacy, authz/authn, unsafe patterns; merge-blocking per policy. | Security-sensitive changes or standing policy for every PR. |
| **Data Analyst** | Analytics | Metrics, dashboards, analytical validation of outputs. | When success criteria are metric- or dashboard-driven. |
| **Data Scientist** | Modeling / experimentation | Experiments, offline evaluation, reproducibility, model documentation. | ML/analytics experiments in scope. |
| **Cost Analyst** | FinOps | Cost estimates, inefficient pattern flags vs orchestrator NFRs. | Infra-heavy or spend-sensitive designs. |
| **PR Writer** | Delivery writer | PR title/body, test plan, risk, rollback; `gh` when automated. | When opening/updating a PR. |
| **PR Reviewer** | Code/architecture reviewer | Review diff vs standards; approve or request changes. | Every PR before merge. |
| **PR Fixer** | Review remediator | Implements review feedback and failing checks with minimal scope. | After review or CI failure. |

*Automation registry IDs may differ (e.g. `github_pr_description_writer`, `cost_optimizer`); Cursor-facing aliases live under `.cursor/agents/` (e.g. `pr-writer.md`, `cost-analyst.md`).*

---

## Repository Structure

| Path | Purpose |
| --- | --- |
| **[`.cursor/agents/`](.cursor/agents/)** | Cursor agent stubs: YAML frontmatter + role description, inputs/outputs, pointers to canonical `agents/` packages or modules. |
| **[`standards/`](standards/)** | Cross-cutting rules: [`coding.md`](standards/coding.md), [`architecture.md`](standards/architecture.md), [`data.md`](standards/data.md), [`testing.md`](standards/testing.md), [`security.md`](standards/security.md), [`cost.md`](standards/cost.md). |
| **[`workflows/`](workflows/)** | Phase docs: [`orchestration.md`](workflows/orchestration.md), [`planning.md`](workflows/planning.md), [`execution.md`](workflows/execution.md), [`pr-process.md`](workflows/pr-process.md). |
| **`agents/`** | Rich definitions: `agent.md`, `prompt.md`, `tools.json`, `constraints.md` per role where applicable. |
| **`config/`** | [`agents.json`](config/agents.json) (DAG registry), orchestration and guardrail config. |
| **`docs/`** | [`MULTI_AGENT_BLUEPRINT.md`](docs/MULTI_AGENT_BLUEPRINT.md); **[`JIRA_STORY_MULTI_AGENT_BLUEPRINT.md`](docs/JIRA_STORY_MULTI_AGENT_BLUEPRINT.md)** (Jira Story fields + MCP); [`JIRA_EPIC_MULTI_AGENT_BLUEPRINT.md`](docs/JIRA_EPIC_MULTI_AGENT_BLUEPRINT.md) (long-form epic). |
| **`.cursor/rules/`** | Enforcement and guardrails (e.g. orchestrator entry, domain policies). |

---

## Usage Guide

### Use this repo as a blueprint

1. Read **[`docs/MULTI_AGENT_BLUEPRINT.md`](docs/MULTI_AGENT_BLUEPRINT.md)** and this README.
2. Open **[`.cursor/agents/orchestrator.md`](.cursor/agents/orchestrator.md)** — start every substantive task from the orchestrator mindset.
3. Apply **[`workflows/`](workflows/)** in order for your increment.
4. Enforce quality with **[`standards/`](standards/)** and **`.cursor/rules/`**.

### Jira stories for new features or applications

- **Rule:** **`.cursor/rules/jira-atlassian-mcp-stories.mdc`** — when you ask for a Jira story/epic for a new feature or app, the agent should **create/update issues in Jira** using the **Atlassian MCP** (`createJiraIssue`, etc.), not only a repo markdown file.
- **Command:** **`.cursor/commands/write-jira-story.md`** — quick checklist for that flow.
- **Template:** **[`docs/JIRA_STORY_MULTI_AGENT_BLUEPRINT.md`](docs/JIRA_STORY_MULTI_AGENT_BLUEPRINT.md)** — Jira field layout and MCP sequence.

### Create a new project using this blueprint

1. **Copy** (or submodule) the folders you need: `.cursor/agents/`, `.cursor/rules/` (adapt), `workflows/`, `standards/`, and optionally `agents/` + `config/` patterns.
2. **Register** agents your automation will run in `config/agents.json` (or your equivalent).
3. **Configure** MCP servers (e.g. Atlassian, GitHub) and secrets outside the repo.
4. **Set** branch protection and CI to match **`workflows/pr-process.md`**.

### How prompts are processed

1. User submits a **prompt** (goal, bug, feature).
2. **Orchestrator** converts it into a **work order** (no jumping to code for non-trivial scope).
3. **Planner** produces a **task graph**; workers receive **task-bound** assignments.
4. Output flows to a **PR**; humans/automation review; **merge** when policy is satisfied.

---

## Workflow Example

**Prompt:** “Add a daily revenue-by-region aggregate to the warehouse, with tests and a draft PR.”

| Step | Actor | Outcome |
| --- | --- | --- |
| 1 | User | Prompt submitted. |
| 2 | Orchestrator | Confirms grain, sources, PII, SLA, cost; `correlation_id`; work order. |
| 3 | Planner | Tasks: governance check → dbt/SQL model + tests → cost note → CI. |
| 4 | Workers | Data governance → Data Engineer implements → Tester adds/validates tests → Cost Analyst notes incremental strategy. |
| 5 | PR | PR Writer opens PR → PR Reviewer reviews → PR Fixer if needed → merge. |

---

## Standards & Governance

| Area | Source |
| --- | --- |
| **Coding** | [`standards/coding.md`](standards/coding.md) — structure, logging, errors, git conventions. |
| **Architecture** | [`standards/architecture.md`](standards/architecture.md) — modularity, boundaries, integration. |
| **Testing** | [`standards/testing.md`](standards/testing.md) — coverage expectations, CI alignment. |
| **Security** | [`standards/security.md`](standards/security.md) — secrets, privacy, access. |
| **Data** | [`standards/data.md`](standards/data.md) — lineage, quality, contracts. |
| **Cost** | [`standards/cost.md`](standards/cost.md) — FinOps awareness, inefficient patterns. |

---

## Contributing

1. **Add or change an agent** — Create/update under `agents/<role>/` (prompts, tools, constraints), add a stub under `.cursor/agents/`, and register in `config/agents.json` if the DAG should include it.
2. **Add a workflow phase** — Extend `workflows/` and link from `docs/MULTI_AGENT_BLUEPRINT.md`.
3. **Tighten governance** — Add or adjust `.cursor/rules/*.mdc` and reference them from `standards/`.
4. **Keep tests green** — Run `pytest` before merging changes that touch Python modules or automation.

---

## Important Rules

1. **Orchestrator is the mandatory entry point** for substantive engineering work (see `workflows/orchestration.md` and `.cursor/rules/blueprint-entry.mdc`).
2. **No direct implementation without planning** at the scale where ambiguity, parallelism, or governance matters — workers bind to **Planner tasks** and ownership.
3. **PR process is required** for protected branches: branch, PR, review, fix loop, merge — not direct pushes that bypass policy.

---

## Additional Resources

| Resource | Description |
| --- | --- |
| [docs/MULTI_AGENT_BLUEPRINT.md](docs/MULTI_AGENT_BLUEPRINT.md) | Deep architecture, agent I/O, parallel execution, example flow |
| [docs/JIRA_STORY_MULTI_AGENT_BLUEPRINT.md](docs/JIRA_STORY_MULTI_AGENT_BLUEPRINT.md) | **Jira Story field layout** + Atlassian MCP steps (preferred for Jira) |
| [docs/JIRA_EPIC_MULTI_AGENT_BLUEPRINT.md](docs/JIRA_EPIC_MULTI_AGENT_BLUEPRINT.md) | Long-form epic reference (see story doc for Jira fields) |
| [docs/jira/README.md](docs/jira/README.md) | Optional local mirror of Jira bodies after MCP creation |
| [AGENTS.md](AGENTS.md) | Agent index and conventions (if present) |
| [utils/logging_spec.md](utils/logging_spec.md) | Structured logging and correlation IDs |

---

*This blueprint helps teams operate a **reusable multi-agent AI engineering discipline** capable of taking a single well-formed prompt from intent to merged delivery — with explicit governance, quality gates, and traceability.*
