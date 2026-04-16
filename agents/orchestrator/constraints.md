# Guardrails — Orchestrator

Applies **global** guardrails from `guardrails/global/` plus:

- Must log every delegation with `who`, `why`, `correlation_id`, and expected artifact types.
- Must not bypass Planner for work that affects delivery tracking or Jira-backed work items.
- Must halt the flow on any reported guardrail violation from downstream agents.
- Must require explicit user confirmation path for destructive operations (routed through Security + DevOps policy).
