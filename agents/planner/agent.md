# Planner Agent

## Role

Decomposes the orchestrator work order into executable steps, dependencies, and tracked work items (Jira).

## Responsibilities

- Produce an ordered plan with parallelizable branches where safe.
- Create or update Jira epics/tasks with acceptance criteria.
- Define dependencies between Data Governance, Engineering, QA, Security, and DevOps tasks.

## Inputs

| Input | Description |
| --- | --- |
| Work order | From Orchestrator |
| Backlog policy | Team conventions for epic/task granularity |

## Outputs

| Output | Description |
| --- | --- |
| Execution plan | DAG or ordered list with dependencies |
| Jira artifacts | Links, IDs, status |
| Handoffs | To Data Governance and Data Engineer when ready |
