# Example Outputs per Agent

## Orchestrator

```json
{
  "work_order_id": "WO-2026-0416",
  "correlation_id": "corr-7e4c",
  "risk_tier": "high",
  "next_agent": "planner",
  "scope_summary": "CRM daily pipeline + Gold revenue by region + governed deploy"
}
```

## Planner

- Epic **DATA-900** with linked tasks and dependencies (Governance → Engineer → DQ → Tester → Security → DevOps).

## Data Governance

- Contract `CRM-G-001@v1`: columns, keys, SLA, PII classification, allowed consumers.

## Data Engineer

- Modules under `pipelines/crm/` with Bronze/Silver/Gold jobs and masked fields in Silver.

## Data Quality

- Validation run `vr-1001`: pass; anomaly monitor registered for row count vs 14d median.

## Tester

- CI report: all tests green; artifact `pytest-report-corr-7e4c.html`.

## Security

- Verdict `approved`; findings: none blocking; audit ID `SEC-5001`.

## DevOps

- Deploy `build-8842` to prod; monitoring dashboard linked; rollback tag `release-1.3.0`.

## Cost Optimizer

- Report: recommend cluster key on Gold table; est. savings 18% on weekly aggregate job.

## Documentation

- PR **#412** updating `docs/architecture/crm.md` and Mermaid data flow.

## Data Analyst

- Dashboard URL; footnote: `freshness_minutes=42`, assumptions on regional mapping table version.
