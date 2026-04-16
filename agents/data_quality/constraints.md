# Guardrails — Data Quality

Applies **global** + **guardrails/data_quality/**.

- Schema consistency checks are mandatory before Gold publish.
- Anomaly detection must avoid alert fatigue: thresholds with owners and runbooks.
- Rules must not leak PII in alert payloads.
