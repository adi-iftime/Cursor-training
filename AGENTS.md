# Agents — repository vs Cursor

## 1. DAG / domain agents (`agents/`)

Authoritative prompts, constraints, and tools for the data platform:

- Folders: `agents/orchestrator/`, `agents/planner/`, `agents/data_engineer/`, …
- Python modules: `agents/jira_story_generator.py`, `agents/github_pr_description_writer.py`, PR lifecycle under `agents/pr_*_agent/`
- Registry: `config/agents.json`

## 2. Cursor subagents (`.cursor/agents/`)

**Cursor Subagents** UI: one YAML-backed stub per **lifecycle or domain** where it helps (e.g. **`github-pr-lifecycle.md`** for PR description + review loop + traceability; **`data-platform.md`** with sections for the three data DAG roles). Other agents stay **one stub per role** (e.g. `orchestrator.md`, `tester.md`). Each stub points to canonical packages under `agents/...` and registry ids in `config/agents.json`. Filenames use kebab-case.

## 3. Skills

- **Domain skills (orchestration):** `skills/<id>/skill.md` + `interfaces.json`
- **Cursor Skills UI:** `.cursor/skills/<id>/SKILL.md` (mirrors or wraps the above)

## 4. Guardrails

- **Authoritative:** `guardrails/<domain>/rules.md`, `checks.md`
- **Cursor Rules UI:** `.cursor/rules/guardrails-<domain>.mdc` + `guardrails-global.mdc`
- **Registry:** `config/guardrails.json`

See `.cursor/README.md` for the full mapping table.