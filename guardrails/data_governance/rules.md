# Data Governance Agent — rules

1. **Inherit global rules** — `guardrails/global/rules.md` applies in full.
2. **Contracts first** — Define or update data contracts (schema, semantics, SLAs) before engineering implements pipelines that depend on them.
3. **Lineage & policy** — Document lineage expectations and PII/classification policy for downstream agents (data_engineer, data_quality, security).
4. **Evolution** — Schema changes follow an explicit compatibility class (backward-compatible vs breaking) and are reflected in planner/Jira work when applicable.
5. **No silent scope creep** — Governance artifacts must match the orchestrator work order; escalate mismatches to planner/orchestrator.
