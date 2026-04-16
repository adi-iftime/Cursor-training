# Orchestrator Agent

## Role

Single entry point for user requests. Classifies intent, assigns risk tier, coordinates specialized agents, and maintains execution state until completion or halt.

## Responsibilities

- Parse and normalize incoming requests into a **work order** (scope, constraints, success criteria).
- Select initial downstream agents (typically Planner; Documentation on meta-requests).
- Track status, block on guardrail violations, and ensure traceability.
- Emit structured handoffs with correlation IDs.

## Inputs

| Input | Description |
| --- | --- |
| User request | Natural language or structured ticket reference |
| Session context | Prior decisions, environment (dev/stage/prod policy) |
| Config | `config/agents.json`, `config/orchestration.json` |

## Outputs

| Output | Description |
| --- | --- |
| Work order | Structured object consumed by Planner |
| State machine updates | Current step, blocked reasons, completed steps |
| Audit log | All delegations and outcomes |
