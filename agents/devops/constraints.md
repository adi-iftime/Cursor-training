# Guardrails — DevOps

- Global guardrails apply.
- No plaintext secrets in repos; use approved secret managers.
- Production deploys require Security sign-off when sensitive paths touched.
- All deployments logged with `correlation_id`, artifact digest, and approver identity where applicable.
