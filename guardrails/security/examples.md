# Security — Valid vs Invalid

## Valid

Role `TRANSFORMER_PROD` limited to `SILVER.*` write and `GOLD.*` read for specific jobs.

## Invalid

CI job uses personal access token embedded in workflow YAML for prod warehouse access.
