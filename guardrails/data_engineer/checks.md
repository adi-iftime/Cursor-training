# Data Engineer Checks

| Check ID | Description | On fail |
| --- | --- | --- |
| DE-PII-01 | No raw PII in logs or error traces | Block merge |
| DE-MED-01 | Tables tagged with layer (`bronze`/`silver`/`gold`) | Block |
| DE-SCH-01 | Contract ID referenced in DDL or transformation header | Warn → Block in prod |
| DE-OBS-01 | Job emits start/complete events with correlation ID | Block deploy |
