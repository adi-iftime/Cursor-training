# Guardrails — Tester

- Global guardrails apply.
- Tests must not exfiltrate sensitive data into logs or CI artifacts.
- Flaky tests are unacceptable for gating; quarantine with explicit ticket and owner.
- Block promotion when contract-critical tests fail.
