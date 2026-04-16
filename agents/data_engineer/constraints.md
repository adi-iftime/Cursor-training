# Guardrails — Data Engineer

Applies **global** + **guardrails/data_engineer/** (see folder for full rules).

Summary:

- Mask PII; no raw sensitive fields in logs or sample outputs.
- Medallion boundaries and schema enforcement are mandatory.
- Optimize for performance and cost; document trade-offs.
- Modular, reusable code with logging and monitoring.
- No destructive DDL/DML on production without gated approval path.
