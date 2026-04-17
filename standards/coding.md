# Coding standards (blueprint)

- **Languages:** Match repository conventions; prefer explicit types in Python; avoid `Any` in public APIs unless justified.
- **Structure:** One concern per module; colocate tests (`tests/` mirroring package paths where applicable).
- **Logging:** Structured logs with `correlation_id`, `agent_id`, `action`, `outcome` (see `utils/logging_spec.md`).
- **Errors:** Fail fast; surface errors to orchestrator handoffs; do not swallow exceptions in agent boundaries.
- **Git:** Feature branches `feature/<ticket-or-slug>-short-description`; commits imperative mood, scoped lines.