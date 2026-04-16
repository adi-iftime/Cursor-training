# Global Rules

1. **MUST** log all decisions and actions with structured fields including `correlation_id`, `agent_id`, `action`, and `outcome`.
2. **MUST** be deterministic when possible: pin versions, avoid time-dependent logic in plans without explicit clock context.
3. **MUST** avoid destructive actions (drops, truncates, broad IAM grants, prod config wipes) without documented confirmation and ticket linkage.
4. **MUST** maintain traceability: who acted, on what artifact, why, and which guardrails were evaluated.
