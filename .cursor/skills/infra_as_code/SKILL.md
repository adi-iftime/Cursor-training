---
name: infra_as_code
description: >-
  Declare infrastructure (networking, compute, IAM, monitoring) in versioned templates. Full detail in repository skills/infra_as_code/.
---

# Cursor skill: infra_as_code

**Repository source:** `skills/infra_as_code/skill.md` and `skills/infra_as_code/interfaces.json`.

---

# Skill — Infrastructure as Code

## Purpose

Declare infrastructure (networking, compute, IAM, monitoring) in versioned templates.

## When to use

- DevOps for environments; Security for IAM review; Cost Optimizer for parameter tuning suggestions.

## Practices

- Modules per environment with variable files; no prod secrets in repo.
- State locking for shared stacks.
