# Cost Checks

| Check ID | Description | On fail |
| --- | --- | --- |
| COST-SCAN-01 | Large scans have filter on partition key or incremental watermark | Warn → Block recurring |
| COST-JOB-01 | Job runtime vs SLA documented when oversized warehouse used | Warn |
| COST-FLG-01 | Top 5 expensive queries in sprint reviewed | Track in ticket |
