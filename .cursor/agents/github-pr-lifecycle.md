---
name: github-pr-lifecycle
description: >-
  Consolidated GitHub/PR: description writer, review, fix, re-review, auto-merge, traceability.
  Maps to github/pr_templates.py, agents/github_pr_description_writer.py, agents/pr_*_agent/, orchestrator.pr_lifecycle_orchestrator.
model: inherit
readonly: false
is_background: false
---

# GitHub & PR lifecycle (consolidated Cursor stub)

One Cursor entry point for **seven** former stubs. Use the **section** that matches the task. The DAG registry still has a single node **`github_pr_description_writer`** for universal PR bodies; Python lifecycle agents are separate packages, not extra DAG ids.

## 1. PR description writer (registry: `github_pr_description_writer`)

- **Source:** `agents/github_pr_description_writer.py`
- **Templates / traceability:** `github/pr_templates.py`, `jira/templates.py`
- **Behavior:** Universal PR bodies via `GitHubClient` (see `agents/AUTOMATION_AGENTS.md`).

## 2. PR reviewer

- **Source:** `agents/pr_review_agent/` (`agent.py`, `prompt.md`, `schema.json`, …)
- **Behavior:** Static PR review over diff.

## 3. PR fixer

- **Source:** `agents/pr_fixer_agent/`
- **Behavior:** Applies fixes from review; push updates.

## 4. PR re-review

- **Source:** `agents/pr_rereview_agent/`
- **Behavior:** Re-review after fixes land.

## 5. Auto-merge

- **Source:** `agents/auto_merge_agent/`
- **Behavior:** Merge gate / recommendation (draft vs mergeable).

## 6. Traceability reviewer

- **Mode:** **Read-only** (use `readonly: true` when spawning a Task that only audits).
- **Patterns:** `github/pr_templates.py`, `jira/templates.py`, `.cursor/rules/traceability-jira-github.mdc`
- **Behavior:** Verify PR sections and Related Jira vs `No Jira story required (non-feature change)`; recommend fixes only.

## CLI orchestration

```bash
python -m orchestrator.pr_lifecycle_orchestrator --owner ORG --repo REPO --pr NUMBER
```

Details: `.cursor/skills/pr-lifecycle-github/SKILL.md`, `github/client.py`, `config/workflow_config.json`.
