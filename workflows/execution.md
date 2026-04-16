# Workflow — Execution (parallel workers)

## Preconditions

- **Orchestrator work order** exists (`correlation_id`, scope, NFRs).
- **Planner task graph** exists: tasks with `agent_id`, dependencies, and **parallel groups** marked.
- No implementation starts without a **task id** from the plan for the current increment.

## Parallel execution

1. **Scheduler** (human or automation) picks tasks whose dependencies are satisfied.
2. **Independent tasks** run concurrently (e.g. security static review vs unit tests) when the DAG allows.
3. Each worker writes only inside its **ownership boundaries** (see `docs/MULTI_AGENT_BLUEPRINT.md` — file prefixes, branches, or directories as agreed per repo).

## Synchronization points

- **Merge to integration branch:** after all tasks for an increment complete, or at defined checkpoints.
- **Contract freeze:** shared interfaces (APIs, schemas) agreed before parallel backend + frontend work diverges.
- **CI green:** required before PR Writer opens or updates the PR.

## Conflict prevention

- **No silent overwrites:** workers do not edit the same files without coordination; use task-scoped branches or directory ownership.
- **Lock by task:** one primary assignee per file in a given increment; conflicts escalated to Planner.

## Outputs

- Code changes on feature branches, tests, artifacts, and handoff notes referencing `correlation_id` and task ids.
