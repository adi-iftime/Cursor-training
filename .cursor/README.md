# Cursor project configuration (full mirror)

This directory is what **Cursor Settings → Project** indexes for **Rules**, **Skills**, **Commands**, and **Subagents**.

## Layout

| Directory | Source of truth in repo | Purpose |
| --- | --- | --- |
| **`rules/*.mdc`** | Mix: orchestration + **guardrails** | Cursor **Rules** (alwaysApply / globs). Guardrail domains mirror `guardrails/<domain>/`. |
| **`skills/*/SKILL.md`** | `skills/<id>/skill.md` + 3 repo-specific skills | Cursor **Skills** (`name` + `description` in YAML). |
| **`commands/*.md`** | Project-defined | Slash **Commands** (`name` + `description`). |
| **`agents/*.md`** | `agents/<role>/` + Python agents | Cursor **Subagents** (YAML: `name`, `description`, `model`, `readonly`, `is_background`). |
| **`guardrails/*.md`** | Index only | Human-readable pointers to `guardrails/` (authoritative markdown). |

## Counts (approximate)

- **Subagents:** one `.md` per DAG agent + automation + PR lifecycle (`agents/*.md`).
- **Skills:** every `skills/*/skill.md` → `.cursor/skills/<id>/SKILL.md`, plus `multi-agent-orchestration`, `jira-github-traceability`, `pr-lifecycle-github`.
- **Commands:** testing, DAG validation, orchestration overview, agents registry, guardrails index.
- **Rules:** existing orchestration/Jira rules + `guardrails-*.mdc` + `repository-config.mdc` + `cursor-guardrails-registry.mdc`.

## Maintenance

- Edit **authoritative** content under `agents/`, `skills/`, `guardrails/` in the repo root.
- Regenerate or edit **Cursor** mirrors here when you add a new agent, skill domain, or guardrail folder.
- **Reload the Cursor window** after bulk changes so the UI rescans `.cursor/`.

## Duplicate paths

- **Registry agents** live in `agents/<name>/` (prompts, constraints). **Cursor subagents** in `.cursor/agents/` are thin delegates with pointers to those paths.
- **Domain skills** live in `skills/`; `.cursor/skills/` embeds or references the same text for the Skills UI.
