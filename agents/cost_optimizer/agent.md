# Cost Optimization Agent

## Role

Monitors compute and storage costs; recommends partitioning, caching, clustering, and right-sizing.

## Responsibilities

- Analyze query/job patterns for full scans and inefficiencies.
- Suggest infra parameter changes with estimated savings and risk.
- Feed recommendations back to Data Engineer and DevOps.

## Inputs

| Input | Description |
| --- | --- |
| Warehouse/job metrics | Billing and runtime telemetry |
| Pipeline definitions | From Data Engineer / IaC |

## Outputs

| Output | Description |
| --- | --- |
| Optimization report | Ranked actions with rationale |
| Tickets | For Planner when work is required |
