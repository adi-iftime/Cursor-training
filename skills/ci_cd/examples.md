# CI/CD — Examples

## Stages

`lint` → `unit_tests` → `integration_tests` → `security_scan` → `deploy_stage` → `smoke_tests` → `deploy_prod`

## Gate

Production deploy requires green Security review artifact ID.
