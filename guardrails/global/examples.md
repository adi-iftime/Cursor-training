# Global — Valid vs Invalid

## Valid

```json
{
  "correlation_id": "corr-9f2a",
  "agent_id": "orchestrator",
  "action": "delegate",
  "outcome": "success",
  "target": "planner",
  "reason": "Work order DATA-2026-0416 ready for decomposition"
}
```

## Invalid

- Missing `correlation_id` on a production deploy handoff.
- Truncating `prod.silver.crm_customer` without `confirmation_ref` and Security review ID.
