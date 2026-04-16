# Jira Epic — Multi-Agent Product Engineering Blueprint

> **Jira-native story layout (Summary, fields, user story, MCP steps):** use **[`JIRA_STORY_MULTI_AGENT_BLUEPRINT.md`](JIRA_STORY_MULTI_AGENT_BLUEPRINT.md)** for paste/API creation. This file remains the **long-form epic** reference.

*Copy-paste friendly epic for Jira. Adjust project keys, components, and labels to your process.*

---

## Title

**[Epic] Multi-agent AI product engineering blueprint — orchestrated delivery from prompt to merge**

---

## Description

This epic defines and tracks a **reusable, AI-assisted multi-agent engineering system** packaged as a repository blueprint for **Cursor** (and compatible automation).

**What this system is**  
A structured operating model in which **every substantive user request** is interpreted by an **Orchestrator** (acting as Product Owner + Data Architect), decomposed by a **Planner** into a dependency-aware task graph, executed by **specialized worker agents** with clear ownership, and delivered through a **mandatory pull-request workflow** (authoring, review, fixes, merge).

**Why it exists**  
Ad-hoc prompting of coding agents produces inconsistent architecture, duplicated work, conflicting edits, weak test discipline, and weak governance over data, security, and cost. This blueprint encodes **roles, handoffs, standards, and workflows** so teams can scale AI-assisted delivery without sacrificing quality or traceability.

**What problems it solves**

- **Uncontrolled scope:** Raw prompts jump to implementation without shared understanding of goals, constraints, and data boundaries.
- **Poor decomposition:** Work is not split into parallelizable, ownable tasks with explicit dependencies.
- **Merge risk:** Changes land without tests, review, or alignment to security/cost posture.
- **Operational drift:** Teams lack a single source of truth for how agents behave and what they may do.

---

## Business Value

**Why this improves development**

- **Predictability:** A fixed entry path (Orchestrator → Planner) produces comparable artifacts (work orders, task graphs) across teams and projects.
- **Velocity with safety:** Parallel execution is explicit; file and branch ownership reduce clobbering; PR workflow preserves human and automated gates.
- **Knowledge reuse:** Standards (`standards/`), workflows (`workflows/`), and agent definitions (`.cursor/agents/`, `agents/`) compound over time instead of living only in chat history.

**Impact on scalability, quality, cost**

- **Scalability:** Planner output (DAG + parallel groups) scales to larger efforts without collapsing into one undifferentiated “do everything” prompt.
- **Quality:** Tester, Security, and PR Reviewer roles create explicit quality and risk signals before merge.
- **Cost:** Cost Analyst and Data Architect (Orchestrator) lenses push back on wasteful infra and full-scan patterns early.

---

## Scope

**Included**

- **Orchestrator-first** interpretation of user intent and NFRs (performance, cost, security).
- **Planner-owned** decomposition: epics/stories/technical tasks, dependencies, parallel execution groups, agent assignment.
- **Worker execution** under scoped ownership (paths/branches per task increment).
- **Validation:** automated tests, CI signals, and security/cost review as applicable.
- **PR workflow:** PR Writer → PR Reviewer → PR Fixer → merge; `git` and GitHub CLI (`gh`) as the mechanical delivery layer when automated.
- **Governance artifacts:** `standards/`, `workflows/`, `.cursor/rules/`, `config/agents.json` registry for DAG-capable automation.
- **Traceability hooks:** Jira Story Writer for backlog items when `jira_required` (or team policy) applies.

**Not included (by default)**

- A full production runtime that replaces your CI/CD platform, identity provider, or data warehouse.
- Guaranteed out-of-the-box integrations for every external system unless configured (e.g. Atlassian MCP, cloud CLIs).
- Automatic merge without review policy compliance; human approval may still be required by org rules.
- “One click builds any app” without local policy, secrets management, and environment provisioning — those remain organization responsibilities.

---

## Functional Requirements

| ID | Requirement |
| --- | --- |
| FR-1 | **Orchestrator must process all prompts** that represent new product/engineering intent before specialized implementation begins, except for narrowly scoped meta-tasks explicitly exempted by policy (e.g. typo-only fixes), documented in `workflows/orchestration.md`. |
| FR-2 | **Planner must break down tasks** from the orchestrator work order into a structured plan: tasks, dependencies, parallel groups, and assigned agent roles. |
| FR-3 | **Worker agents must execute tasks** only when bound to **Planner task identifiers** and **ownership boundaries** for the current increment. |
| FR-4 | **PR workflow must be enforced** for protected branches: changes are introduced via feature branches and reviewed PRs per `workflows/pr-process.md`. |
| FR-5 | **Jira Story Writer** must create or update Jira issues when orchestration marks Jira as required or when the team mandates backlog traceability for the increment. |
| FR-6 | **Validation agents** (e.g. Tester, Security) must record findings in a way that can block or gate merge per severity and policy. |

---

## Non-Functional Requirements

| ID | Category | Requirement |
| --- | --- | --- |
| NFR-1 | **Scalability** | The model must support larger efforts via explicit DAGs and parallel groups without collapsing ownership boundaries. |
| NFR-2 | **Maintainability** | Agent behavior is documented in `.cursor/agents/` and `agents/`; cross-cutting rules live in `standards/` and `.cursor/rules/`. |
| NFR-3 | **Modularity** | New agents and skills are added via registry + folder patterns without rewriting the core orchestration narrative. |
| NFR-4 | **Cost efficiency** | Cost Analyst and orchestrator NFRs discourage wasteful compute, storage, and network patterns; FinOps assumptions are stated explicitly. |
| NFR-5 | **Security** | Security Engineer validates secrets handling, privacy, and access control expectations; critical issues can block merge. |
| NFR-6 | **Observability** | Work artifacts reference `correlation_id` and task identifiers suitable for structured logging and audit (see `utils/logging_spec.md` where applicable). |

---

## Architecture Overview

**End-to-end flow**

1. **User prompt** → **Orchestrator** produces a structured **work order** (goal, scope, architecture/data sketch, constraints, NFRs, `correlation_id`, flags such as `jira_required`).
2. **Planner** converts the work order into a **task graph** (dependencies + parallel groups) and assigns **worker agents**.
3. **Optional:** **Jira Story Writer** syncs epics/stories to Jira when required.
4. **Workers** implement in parallel where dependencies allow; **Tester**, **Security**, and **Cost Analyst** run as gates or parallel concerns as planned.
5. **PR Writer** opens/updates the PR; **PR Reviewer** reviews; **PR Fixer** addresses feedback; branch merges to the target line per policy.

**Synchronization points**

- Interface contracts (APIs, schemas) agreed before parallel backend/frontend divergence when both are in scope.
- CI green before PR is considered ready for final review (team policy may vary).

---

## Agent Definitions (Mandatory)

### Orchestrator (Product Owner + Data Architect)

| Field | Content |
| --- | --- |
| **Name** | Orchestrator |
| **Role** | Single entry point; combines Product Owner intent with Data Architect constraints. |
| **Responsibilities** | Interpret prompts; clarify ambiguities; define business goal; propose technical architecture and data model; capture constraints and NFRs (performance, cost, security); set pointers to standards; issue a structured work order. |
| **Inputs** | User prompt; repository context; organizational policies; guardrails. |
| **Outputs** | Structured work order; `correlation_id`; flags (e.g. `jira_required`). |
| **Constraints** | No direct implementation for substantive scope; must not skip Planner for non-trivial work. |
| **Tools allowed** | Read-only exploration first; MCP as configured; no destructive git operations without explicit instruction. |

### Planner

| Field | Content |
| --- | --- |
| **Name** | Planner |
| **Role** | Work breakdown and sequencing; backlog alignment. |
| **Responsibilities** | Decompose orchestrator output into epics/stories/technical tasks; define dependencies and parallel groups; assign worker agents; maintain coherence of the task graph. |
| **Inputs** | Orchestrator work order. |
| **Outputs** | Task graph; task IDs; agent assignments; optional Jira updates. |
| **Constraints** | External backlog tooling only per team policy and MCP rules; balanced scope (no hidden mega-tasks). |
| **Tools allowed** | Atlassian MCP (when enabled and permitted); configuration and repo read helpers. |

### Jira Story Writer

| Field | Content |
| --- | --- |
| **Name** | Jira Story Writer (alias: Jira Story Generator in automation IDs) |
| **Role** | Backlog authoring and traceability. |
| **Responsibilities** | Create or refine Jira epics/stories/subtasks; align summaries and acceptance criteria with orchestrator/planner artifacts; link issues to branches/PRs when policy requires. |
| **Inputs** | Work order; task graph; acceptance criteria seeds; `jira_required` flag. |
| **Outputs** | Jira issues with required fields; traceability metadata. |
| **Constraints** | No production code changes in this role; respect Jira workflow constraints. |
| **Tools allowed** | Atlassian MCP; read-only context from repository for accurate titles and links. |

### Backend Developer

| Field | Content |
| --- | --- |
| **Name** | Backend Developer |
| **Role** | Server-side implementation and supporting automation. |
| **Responsibilities** | Implement APIs, services, workers, batch jobs, and relevant infra-as-code within assigned scope; add tests; document operational hooks. |
| **Inputs** | Planner task spec; interface contracts; orchestrator constraints; `correlation_id`. |
| **Outputs** | Code and tests in owned paths; implementation notes for PR Writer. |
| **Constraints** | No secrets in repo; no unrelated refactors; honor security and architecture standards. |
| **Tools allowed** | Language toolchains; test runners; linters; approved cloud/API CLIs. |

### Frontend Developer

| Field | Content |
| --- | --- |
| **Name** | Frontend Developer |
| **Role** | Client-side implementation and UX quality. |
| **Responsibilities** | Implement UI per contracts and design tokens; client tests (unit/component/e2e) as applicable; accessibility baseline. |
| **Inputs** | Planner task spec; API/schema contracts; design references. |
| **Outputs** | Frontend code and tests in owned paths; notes for review and PR body. |
| **Constraints** | No secrets embedded in client bundles; do not weaken accessibility without explicit approval. |
| **Tools allowed** | Package manager; bundler; browser tooling/MCP if enabled. |

### Data Engineer

| Field | Content |
| --- | --- |
| **Name** | Data Engineer |
| **Role** | Data movement, transformation, and operational data quality hooks. |
| **Responsibilities** | Build pipelines/jobs/models per plan; ensure idempotency where required; integrate with catalog/governance outputs; add tests and documentation. |
| **Inputs** | Planner tasks; data governance outputs; source/sink definitions. |
| **Outputs** | Pipeline code, tests, and operational runbooks or notes as required. |
| **Constraints** | PII and classified data handling per policy; no unapproved external egress. |
| **Tools allowed** | SQL/dbt/Spark/orchestration tools per project; warehouse access per least privilege. |

### Tester

| Field | Content |
| --- | --- |
| **Name** | Tester |
| **Role** | Verification and quality gates. |
| **Responsibilities** | Author/extend automated tests; define test plans for acceptance criteria; report defects with repro steps; monitor CI results. |
| **Inputs** | Implementation branch; acceptance criteria; risk-focused test priorities from orchestrator/planner. |
| **Outputs** | Tests; CI status interpretation; defect reports. |
| **Constraints** | Does not merge PRs; escalates blockers rather than silently skipping tests. |
| **Tools allowed** | `pytest` or project test stack; CI systems; coverage tools. |

### Security Engineer

| Field | Content |
| --- | --- |
| **Name** | Security Engineer |
| **Role** | Threat-aware review and policy enforcement. |
| **Responsibilities** | Review for secrets exposure, unsafe defaults, authz/authn gaps, data minimization; classify findings; recommend fixes. |
| **Inputs** | Diffs; architecture notes; data classification; dependency manifests. |
| **Outputs** | Findings with severity; merge-blocking recommendations when policy dictates. |
| **Constraints** | Must not approve critical violations without recorded exception process. |
| **Tools allowed** | Static analysis; dependency scanners; secret scanners; policy baselines. |

### Data Analyst

| Field | Content |
| --- | --- |
| **Name** | Data Analyst |
| **Role** | Analytical validation and metric alignment. |
| **Responsibilities** | Define/refine metrics; validate analytical outputs against business questions; support dashboard requirements; analyze anomalies when in scope. |
| **Inputs** | Business questions from orchestrator; datasets/metrics definitions; quality outputs. |
| **Outputs** | Analysis artifacts; metric specs; dashboard requirements. |
| **Constraints** | Production access read-only unless explicitly approved; no ungoverned data extracts. |
| **Tools allowed** | SQL/BI tools; approved analytics platforms; MCP data tools if configured. |

### Data Scientist

| Field | Content |
| --- | --- |
| **Name** | Data Scientist |
| **Role** | Experimental modeling and offline evaluation. |
| **Responsibilities** | Frame experiments; build training/evaluation pipelines; document limitations; hand off productionization boundaries to engineering as needed. |
| **Inputs** | Problem statement; datasets; privacy/ethics constraints; compute budget signals. |
| **Outputs** | Reproducible experiments; metrics; model artifacts per policy; model documentation. |
| **Constraints** | Reproducibility required; no undeclared data egress; fairness/privacy constraints per policy. |
| **Tools allowed** | Python/R ML stacks; experiment tracking; approved compute environments. |

### Cost Analyst

| Field | Content |
| --- | --- |
| **Name** | Cost Analyst (alias: Cost Optimizer in automation IDs) |
| **Role** | FinOps-oriented assessment of design choices. |
| **Responsibilities** | Estimate infra/workload costs; flag inefficient patterns; compare options against orchestrator cost NFRs. |
| **Inputs** | Architecture options; usage assumptions; telemetry/billing signals when available. |
| **Outputs** | Cost notes; recommendations; risk flags for runaway spend. |
| **Constraints** | Advisory unless elevated to policy blocker by org standards. |
| **Tools allowed** | Pricing documentation; cost APIs (read-only); observability dashboards. |

### PR Writer

| Field | Content |
| --- | --- |
| **Name** | PR Writer (alias: GitHub PR Description Writer in automation IDs) |
| **Role** | Delivery packaging and PR hygiene. |
| **Responsibilities** | Author PR title/body: summary, test plan, risk, rollout/rollback; ensure links to issues/tasks; align description to actual diff scope. |
| **Inputs** | Diff summary; task IDs; CI results; reviewer checklist hints. |
| **Outputs** | Opened/updated pull request via `gh` when automated. |
| **Constraints** | Accurate scope; no smuggling unrelated changes under misleading text. |
| **Tools allowed** | `git`; GitHub CLI `gh`. |

### PR Reviewer

| Field | Content |
| --- | --- |
| **Name** | PR Reviewer |
| **Role** | Independent quality and standards gate. |
| **Responsibilities** | Review for correctness, maintainability, architecture fit, tests, security/cost signals; request changes with specifics; approve when standards met. |
| **Inputs** | PR diff; `standards/*`; orchestrator NFRs; threat model notes. |
| **Outputs** | Review comments; approve/request changes decision. |
| **Constraints** | Does not implement fixes (escalate to PR Fixer); may block merge on critical issues. |
| **Tools allowed** | `gh`; CI artifacts; linters; policy scanners. |

### PR Fixer

| Field | Content |
| --- | --- |
| **Name** | PR Fixer |
| **Role** | Closure of review feedback and CI failures. |
| **Responsibilities** | Implement requested changes; re-run tests; update PR conversation; minimize churn. |
| **Inputs** | Review comments; failing checks; policy violations to remediate. |
| **Outputs** | Additional commits; updated PR state ready for re-review. |
| **Constraints** | Minimal fix surface; no opportunistic refactors unless agreed. |
| **Tools allowed** | `git`; `gh`; local test runners; formatters/linters. |

---

## Workflow Description (Step-by-Step)

1. **User prompt** — A new goal or change request enters the system (chat, ticket, or automation).
2. **Orchestrator analysis** — Clarifies intent, defines scope, architecture/data boundaries, constraints, NFRs; emits a structured work order and `correlation_id`.
3. **Planning** — Planner converts the work order into tasks with dependencies and identifies parallel execution groups; optionally updates Jira via Jira Story Writer.
4. **Parallel execution** — Independent tasks run concurrently subject to DAG constraints; each worker respects ownership boundaries; Security, Tester, and Cost Analyst participate per plan.
5. **PR creation and review** — PR Writer opens the PR; CI runs; PR Reviewer evaluates; PR Fixer addresses feedback until approval; merge follows branch protection policy.

---

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| AC-1 | The documented system **enforces an orchestrator-first flow** for substantive engineering work, with exceptions explicitly documented. |
| AC-2 | **Agents do not bypass planning**: worker execution is tied to Planner outputs (task IDs, scope boundaries). |
| AC-3 | **PR workflow is respected** for protected branches: branch → PR → review → fix loop → merge. |
| AC-4 | **Documentation is complete**: README, workflows, standards, and agent stubs exist and cross-reference each other. |
| AC-5 | **Governance**: security and cost considerations have named owners (roles) and referenced standards. |

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| **Agent conflicts** (two workers edit the same files) | Merge conflicts, rework | Planner assigns non-overlapping ownership; serialize conflicting tasks; integration checkpoints |
| **Context drift** (implementation diverges from orchestrator intent) | Wrong product outcomes | Work order referenced in PR body; traceability to tasks; reviewer checks architecture fit |
| **Over-engineering** (too many layers for simple fixes) | Slow feedback | Document exempt classes of tiny changes; keep orchestration lightweight for true trivial edits |
| **Tooling gaps** (MCP/auth missing) | Backlog/tool steps fail | Graceful degradation: manual Jira updates; explicit “tool not available” handling in runbooks |
| **Secret leakage via prompts/logs** | Security incident | Security Engineer gate; secret scanning in CI; redaction standards |

---

## Links (Repository)

- Architecture narrative: `docs/MULTI_AGENT_BLUEPRINT.md`
- Workflows: `workflows/orchestration.md`, `workflows/planning.md`, `workflows/execution.md`, `workflows/pr-process.md`
- Standards: `standards/`
- Cursor agents: `.cursor/agents/`
- Automation registry: `config/agents.json`
