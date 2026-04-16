# Guardrails — Planner

- Global guardrails apply.
- Tickets must reference **correlation_id** and work order ID in description or custom field.
- No task may imply production deployment without Security/DevOps gates in the dependency chain.
- Plans must include a **rollback** or **safe revert** note for pipeline changes.
