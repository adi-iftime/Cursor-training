# Jira Story — Multi-Agent Product Engineering Blueprint

This file is written in **Jira issue field layout** (Summary, type, description sections, acceptance criteria). Use it to **paste into Jira** or as the **`description` body** when creating the issue via the **Atlassian MCP** (`createJiraIssue`, `contentFormat: "markdown"`).

---

## Issue metadata (set in Jira or via MCP `additional_fields`)

| Field | Value |
| --- | --- |
| **Project** | `YOURPROJECT` (replace with your Jira project key) |
| **Issue type** | Epic *(or Story if your process tracks this work as a Story under a parent Epic)* |
| **Summary** | Multi-agent AI product engineering blueprint — orchestrated delivery from prompt to merge |
| **Priority** | *(per team policy)* |
| **Labels** | `multi-agent`, `cursor`, `blueprint`, `governance`, `pr-workflow` |
| **Components** | *(optional)* Platform / Developer Experience |

**Summary (copy for Summary field)**

`Multi-agent AI product engineering blueprint — orchestrated delivery from prompt to merge`

---

## User story

**As a** platform or engineering lead  
**I want** a reusable Cursor blueprint where every substantive request flows Orchestrator → Planner → workers → PR  
**So that** teams scale AI-assisted delivery with predictable governance, quality gates, and traceability.

---

## Description

### Context

This work defines a **reusable, AI-assisted multi-agent engineering system** packaged as a repository blueprint for **Cursor** (and compatible automation).

**What this system is**  
A structured operating model where **every substantive user request** is interpreted by an **Orchestrator** (Product Owner + Data Architect), decomposed by a **Planner** into a dependency-aware task graph, executed by **specialized worker agents** with clear ownership, and delivered through a **mandatory pull-request workflow** (authoring, review, fixes, merge).

**Why it exists**  
Ad-hoc prompting produces inconsistent architecture, duplicated work, conflicting edits, weak testing discipline, and weak governance over data, security, and cost. This blueprint encodes **roles, handoffs, standards, and workflows** so teams can scale AI-assisted delivery without sacrificing quality or traceability.

**Problems solved**

- Uncontrolled scope: prompts jump to implementation without shared goals, constraints, and data boundaries.
- Poor decomposition: work is not split into parallelizable, ownable tasks with explicit dependencies.
- Merge risk: changes land without tests, review, or alignment to security/cost posture.
- Operational drift: no single source of truth for how agents behave.

### Business value

- **Predictability:** Fixed entry path (Orchestrator → Planner) produces comparable artifacts (work orders, task graphs).
- **Velocity with safety:** Parallel execution is explicit; ownership reduces clobbering; PR workflow preserves gates.
- **Knowledge reuse:** `standards/`, `workflows/`, `.cursor/agents/`, `agents/` compound over time.
- **Scalability / quality / cost:** Planner DAGs scale; Tester/Security/Reviewer roles improve quality; Cost Analyst + orchestrator NFRs constrain wasteful spend.

### Scope — included

- Orchestrator-first interpretation and NFR capture (performance, cost, security).
- Planner-owned decomposition: tasks, dependencies, parallel groups, agent assignment.
- Worker execution under scoped ownership.
- Validation: tests, CI, security/cost review as planned.
- PR workflow: PR Writer → PR Reviewer → PR Fixer → merge (`git` / `gh` when automated).
- Governance: `standards/`, `workflows/`, `.cursor/rules/`, `config/agents.json`.
- Jira Story Writer when `jira_required` or policy mandates backlog traceability.

### Scope — not included

- Replacement of enterprise CI/CD, IdP, or warehouse.
- Every external integration without configuration (Atlassian MCP, cloud CLIs, etc.).
- Merge without review policy compliance.
- “Build any app in one click” without org secrets, policy, and environments.

### Functional requirements

| ID | Requirement |
| --- | --- |
| FR-1 | Orchestrator processes prompts representing new product/engineering intent before specialized implementation (except narrowly scoped exemptions in `workflows/orchestration.md`). |
| FR-2 | Planner breaks the work order into tasks, dependencies, parallel groups, and agent roles. |
| FR-3 | Workers execute only when bound to Planner task identifiers and ownership boundaries. |
| FR-4 | PR workflow is enforced for protected branches per `workflows/pr-process.md`. |
| FR-5 | Jira Story Writer creates/updates Jira when orchestration or policy requires. |
| FR-6 | Tester/Security record findings that can gate merge per severity and policy. |

### Non-functional requirements

| ID | Category | Requirement |
| --- | --- | --- |
| NFR-1 | Scalability | DAGs and parallel groups without collapsing ownership. |
| NFR-2 | Maintainability | Agents documented under `.cursor/agents/` and `agents/`; rules in `standards/` and `.cursor/rules/`. |
| NFR-3 | Modularity | New agents/skills via registry + folder patterns. |
| NFR-4 | Cost efficiency | Cost Analyst + orchestrator discourage wasteful patterns. |
| NFR-5 | Security | Security Engineer can block merge on critical issues. |
| NFR-6 | Observability | `correlation_id` and task ids in handoffs (`utils/logging_spec.md` where applicable). |

### Architecture overview

1. User prompt → Orchestrator → work order (`correlation_id`, optional `jira_required`).
2. Planner → task graph and agent assignments.
3. Optional: Jira Story Writer updates backlog.
4. Workers in parallel per DAG; Tester, Security, Cost Analyst as planned.
5. PR Writer → PR Reviewer → PR Fixer → merge.

**Sync points:** API/schema contracts before parallel backend/frontend divergence; CI green per policy before final approval.

### Agent definitions (mandatory)

| Agent | Role | Responsibilities | Inputs | Outputs | Constraints | Tools |
| --- | --- | --- | --- | --- | --- | --- |
| Orchestrator | PO + Data Architect | Intent, architecture/data sketch, NFRs, work order | Prompt, policies | Work order, `correlation_id` | No skipping Planner for non-trivial work | Read/MCP; no destructive git without instruction |
| Planner | Delivery / sequencing | DAG, parallel groups, assignments | Work order | Task graph, task IDs | MCP policy for Jira | Atlassian MCP, config reads |
| Jira Story Writer | Backlog | Issues, AC, traceability | Work order, tasks, `jira_required` | Jira issues | No prod code | Atlassian MCP |
| Backend Developer | Server-side | APIs, jobs, IaC in scope | Task spec, contracts | Code, tests | No secrets; no drive-by refactors | Toolchain, CI |
| Frontend Developer | Client-side | UI per contracts | Task spec, APIs, design | UI, tests | No secrets in bundles | Bundler, tests |
| Data Engineer | Data paths | Pipelines, models, tests | Tasks, governance | Pipelines, docs | PII policy | SQL/dbt/etc. |
| Tester | Quality | Tests, plans, defects | Branch, AC | Tests, reports | Does not merge | pytest/CI |
| Security Engineer | AppSec | Secrets, privacy, authz | Diff, architecture | Findings, severities | Can block critical | SAST, scanners |
| Data Analyst | Analytics | Metrics, validation | Questions, data | Analysis, specs | Read-only prod default | SQL/BI |
| Data Scientist | Modeling | Experiments, evaluation | Problem, data | Experiments, docs | Reproducibility; no undeclared egress | ML stack |
| Cost Analyst | FinOps | Cost estimates, flags | Architecture, usage | Cost notes | Often advisory | Pricing, dashboards |
| PR Writer | Delivery writer | PR title/body | Diff, CI | PR | Accurate scope | git, gh |
| PR Reviewer | Reviewer | Quality, architecture, security | Diff, standards | Review decision | No implementing fixes | gh, CI |
| PR Fixer | Remediator | Fix review/CI | Comments, failures | Commits | Minimal churn | git, gh |

### Workflow (step-by-step)

1. User prompt.
2. Orchestrator analysis → work order.
3. Planning → tasks + dependencies + optional Jira.
4. Parallel execution with ownership rules.
5. PR creation, review, fixes, merge.

### Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Agent conflicts on files | Ownership in plan; serialize conflicting tasks; integration checkpoints |
| Context drift | Work order in PR; task traceability; architecture review |
| Over-engineering | Document trivial-edit exemptions |
| MCP/auth gaps | Manual fallback; explicit runbook |
| Secret leakage | Security gate; scanners; redaction |

### Repository links

- `docs/MULTI_AGENT_BLUEPRINT.md`
- `workflows/orchestration.md`, `planning.md`, `execution.md`, `pr-process.md`
- `standards/`, `.cursor/agents/`, `config/agents.json`

---

## Acceptance criteria (Definition of Done)

- [ ] **AC-1** — Orchestrator-first flow is documented and enforced for substantive work (exceptions documented).
- [ ] **AC-2** — Workers do not bypass planning: execution ties to Planner task IDs and ownership.
- [ ] **AC-3** — PR workflow respected on protected branches (branch → PR → review → fix → merge).
- [ ] **AC-4** — README, workflows, standards, and agent stubs exist and cross-link.
- [ ] **AC-5** — Security and cost have named roles and standards references.

---

## MCP: create this issue in Jira

1. Call **`getAccessibleAtlassianResources`** → obtain **`cloudId`**.
2. If project key unknown: **`getVisibleJiraProjects`** (`action: "create"`).
3. Optional: **`getJiraProjectIssueTypesMetadata`** / **`getJiraIssueTypeMetaWithFields`** for required fields (Epic name, parent Epic, custom fields).
4. Call **`createJiraIssue`** with:
   - `cloudId`, `projectKey`, `issueTypeName` (`Epic` or `Story` per project),
   - `summary` (use Summary above),
   - `description` — paste **from “User story” through “Repository links”** (or full file minus this MCP section),
   - `contentFormat`: `"markdown"`,
   - `additional_fields` — e.g. `labels`, `priority`, components, Epic link field per project schema.

Do **not** rely on a local-only markdown file as the sole backlog record when the user asked to **write the Jira story** for a new feature or application: **create or update the Jira issue** via MCP unless the user explicitly opts out.
