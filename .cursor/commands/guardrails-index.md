---
name: guardrails-index
description: Point to guardrails domains and Cursor rule files
---

# Guardrails

- **Repo:** `guardrails/<domain>/rules.md` and `checks.md`
- **Cursor Rules UI:** `.cursor/rules/guardrails-*.mdc` (mirrors domains)
- **Registry:** `config/guardrails.json` maps agents → guardrail paths

Global rules apply to every session (`guardrails-global.mdc`).
