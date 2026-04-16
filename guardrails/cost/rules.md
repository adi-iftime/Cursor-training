# Cost Rules

1. **MUST** avoid unnecessary full table scans; prefer partition pruning and incremental patterns.
2. **MUST** suggest partitioning and clustering where data volume warrants it.
3. **MUST** flag expensive queries and jobs with estimated cost drivers (bytes, duration, warehouse).
