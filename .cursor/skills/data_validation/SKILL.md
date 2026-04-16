---
name: data_validation
description: >-
  Express expectations on datasets: schema, volume, uniqueness, distributions, and referential integrity. Full detail in repository skills/data_validation/.
---

# Cursor skill: data_validation

**Repository source:** `skills/data_validation/skill.md` and `skills/data_validation/interfaces.json`.

---

# Skill — Data Validation

## Purpose

Express expectations on datasets: schema, volume, uniqueness, distributions, and referential integrity.

## When to use

- Data Quality for rule specs; Tester for automated enforcement; Data Engineer for inline checks.

## Practices

- One rule set per contract version.
- Severity levels: `block`, `warn`, `monitor`.
