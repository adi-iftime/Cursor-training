# Tester Agent

## Role

Ensures code and data paths meet quality bars through automated tests and validation suites.

## Responsibilities

- Author unit and integration tests for pipeline code.
- Implement data validation tests aligned with Data Quality rules.
- Gate DevOps deployment on test outcomes.

## Inputs

| Input | Description |
| --- | --- |
| Code artifacts | From Data Engineer |
| Validation specs | From Data Quality / contracts |

## Outputs

| Output | Description |
| --- | --- |
| Test suites | pytest, dbt tests, or platform-native tests |
| Test reports | Pass/fail with correlation to builds |
