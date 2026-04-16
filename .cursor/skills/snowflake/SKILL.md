---
name: snowflake
description: >-
  Implement SQL pipelines, stages, tasks, and dynamic tables with strong RBAC and cost controls. Full detail in repository skills/snowflake/.
---

# Cursor skill: snowflake

**Repository source:** `skills/snowflake/skill.md` and `skills/snowflake/interfaces.json`.

---

# Skill — Snowflake

## Purpose

Implement SQL pipelines, stages, tasks, and dynamic tables with strong RBAC and cost controls.

## When to use

- Data Engineer builds warehouse-centric medallion layers.
- Cost Optimizer analyzes query history; Data Quality runs SQL checks.

## Practices

- Explicit `ROLE` context; no over-broad `ACCOUNTADMIN` in automation.
- Clustering and incremental patterns for large tables.
