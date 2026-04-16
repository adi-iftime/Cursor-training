# Logging Standards

## Required fields (structured JSON logs)

| Field | Description |
| --- | --- |
| `timestamp` | RFC3339 UTC |
| `level` | `DEBUG` \| `INFO` \| `WARN` \| `ERROR` |
| `correlation_id` | End-to-end trace ID |
| `agent_id` | Acting agent |
| `action` | Verb describing the operation |
| `outcome` | `success` \| `failure` \| `blocked` |
| `reason` | Human-readable when blocked or failed |

## Metrics

- **Counters**: `agent.handoffs`, `guardrail.violations`, `pipeline.deployments`
- **Histograms**: `task.duration_ms`, `query.cost_units`
- **Gauges**: `data.freshness_minutes` (Gold tables under SLA)

## Pipeline monitoring hooks

1. Register job metadata (name, environment, owner) at deploy time.
2. Emit start/complete/fail events with correlation ID propagated from orchestrator.
3. Alert on SLA breach for freshness and error rate per contract ID.
