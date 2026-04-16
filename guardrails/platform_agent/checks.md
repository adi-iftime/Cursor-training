# Platform agent — enforcement checks

| Check | Pass criteria |
| --- | --- |
| Correlation ID | Present on every structured handoff |
| Agent registry | Scheduled agents ⊆ `config/agents.json` |
| Jira traceability | Issue keys or explicit “not applicable” with rationale |
| GitHub traceability | PR URLs / branch names when repo workflow touched |
| Failure visibility | Errors surfaced to orchestrator JSON, not swallowed |
