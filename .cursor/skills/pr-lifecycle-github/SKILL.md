---
name: pr-lifecycle-github
description: >-
  Runs and explains the Python PR lifecycle orchestrator (review, fix, re-review, merge)
  using github.client.GitHubClient and agents under agents/pr_*_agent/. Use when the user
  asks about autonomous PR review, merge gates, or python -m orchestrator.pr_lifecycle_orchestrator.
---

# PR lifecycle (GitHub integration)

## Entry

```bash
python -m orchestrator.pr_lifecycle_orchestrator --owner ORG --repo REPO --pr NUMBER
```

## Components

- `github/client.py` — GitHub REST client (token from `GITHUB_TOKEN`)
- `github/pr_service.py` — `fetch_pr_context`, CI evaluation helpers
- `agents/pr_review_agent`, `pr_fixer_agent`, `pr_rereview_agent`, `auto_merge_agent`
- `config/workflow_config.json` — cycles, checks, optional `update_pr_description`

## Separation

PR **description** formatting for traceability is `agents/github_pr_description_writer.py`; lifecycle agents handle review/fix/merge.
