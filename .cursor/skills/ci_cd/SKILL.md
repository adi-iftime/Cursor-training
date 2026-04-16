---
name: ci_cd
description: >-
  Define continuous integration and delivery pipelines with gated promotions. Full detail in repository skills/ci_cd/.
---

# Cursor skill: ci_cd

**Repository source:** `skills/ci_cd/skill.md` and `skills/ci_cd/interfaces.json`.

---

# Skill — CI/CD

## Purpose

Define continuous integration and delivery pipelines with gated promotions.

## When to use

- DevOps for build/test/deploy; Tester for test stage integration.

## Practices

- Separate workflows for `dev`, `stage`, `prod` with manual approvals where required.
- Artifact immutability: image digest or wheel hash pinned per release.
