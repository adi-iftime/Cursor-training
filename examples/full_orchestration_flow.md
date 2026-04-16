# Full Orchestration Flow (Example)

1. **Orchestrator** creates work order `WO-2026-0416`, `correlation_id=corr-7e4c`, risk `high` (PII).
2. **Planner** opens Epic **DATA-900** and tasks: governance contract, pipeline, DQ, tests, security, devops, docs, analyst optional.
3. **Data Governance** publishes contract `CRM-G-001` (Gold grain: `region`, `day`, revenue sums) and lineage requirements.
4. **Data Engineer** implements Bronze ingest → Silver conform (hashed identifiers) → Gold aggregate with incremental partitions.
5. **Data Quality** attaches suite `CRM-G-001@v1` with null/completeness rules and anomaly monitors.
6. **Tester** runs unit + integration tests; data tests tied to contract.
7. **Security** approves after PII controls and RBAC review.
8. **DevOps** deploys via CI/CD to stage, smoke tests, then prod with monitoring hooks.
9. **Cost Optimizer** flags one query for clustering on `region`; ticket **DATA-901** opened.
10. **Documentation** updates architecture and runbooks.
11. **Data Analyst** builds Gold-only dashboard with freshness and assumptions.
