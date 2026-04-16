# Agents — repository vs Cursor

## 1. DAG / domain agents (`agents/`)

Authoritative prompts, constraints, and tools for the data platform:

- Folders: `agents/orchestrator/`, `agents/planner/`, `agents/data_engineer/`, …
- Python modules: `agents/jira_story_generator.py`, `agents/github_pr_description_writer.py`, PR lifecycle under `agents/pr_*_agent/`
- Registry: `config/agents.json`

## 2. Cursor subagents (`.cursor/agents/`)

One file per role for the **Cursor Subagents** UI. Each file has YAML frontmatter and points to the canonical `agents/...` path. Filenames use kebab-case (e.g. `data-engineer.md`, `jira-story-generator.md`).

## 3. Skills

- **Domain skills (orchestration):** `skills/<id>/skill.md` + `interfaces.json`
- **Cursor Skills UI:** `.cursor/skills/<id>/SKILL.md` (mirrors or wraps the above)

## 4. Guardrails

- **Authoritative:** `guardrails/<domain>/rules.md`, `checks.md`
- **Cursor Rules UI:** `.cursor/rules/guardrails-<domain>.mdc` + `guardrails-global.mdc`
- **Registry:** `config/guardrails.json`

See `.cursor/README.md` for the full mapping table.