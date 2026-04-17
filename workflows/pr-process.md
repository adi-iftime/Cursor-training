# Workflow — PR & delivery (git + GitHub CLI)

## Preconditions

- Implementation and tests complete for the planned increment.
- Branch naming follows `standards/coding.md` (e.g. `feature/<ticket>-short-description`).

## Steps

1. **PR Writer** (stub **`.cursor/agents/github-pr-lifecycle.md`** §1 — registry `github_pr_description_writer` / `agents/github_pr_description_writer.py`): draft title, summary, testing notes, risk, rollback; use `gh pr create` or `gh pr edit` as the execution layer when automation applies.
2. **CI:** push branch; ensure pipeline (lint, tests, security scans) runs.
3. **PR Reviewer** (stub **`github-pr-lifecycle.md`** §2 — `agents/pr_review_agent/`): review for quality, architecture alignment (`standards/architecture.md`), security (`standards/security.md`), and cost signals (`standards/cost.md`).
4. **PR Fixer** (stub **`github-pr-lifecycle.md`** §3 — `agents/pr_fixer_agent/`): address feedback; push updates; re-request review if required.
5. **Approval & merge:** squash or merge per team policy; delete branch after merge.

## Commands (reference)

```bash
git status
git push -u origin HEAD
gh pr create --fill   # or --title / --body
gh pr view --web
gh pr checks
```

## Rules

- **All substantive changes** land via PR (no direct pushes to protected default branch).
- Reviewer may **block** on secrets, PII, or policy violations surfaced by Security agent checks.

Full PR lifecycle roles, traceability, and automation pointers: **`docs/MULTI_AGENT_BLUEPRINT.md`** §3 and **`.cursor/agents/github-pr-lifecycle.md`**.
