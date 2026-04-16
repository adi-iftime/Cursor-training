---
name: monitoring
description: >-
  Emit metrics, traces, and alerts for pipelines and infrastructure. Full detail in repository skills/monitoring/.
---

# Cursor skill: monitoring

**Repository source:** `skills/monitoring/skill.md` and `skills/monitoring/interfaces.json`.

---

# Skill — Monitoring

## Purpose

Emit metrics, traces, and alerts for pipelines and infrastructure.

## When to use

- DevOps for deploy-time hooks; Data Quality for anomaly monitors; Cost Optimizer for usage signals.

## Practices

- RED/USE style metrics where applicable: rate, errors, duration.
- Alert routes differ by environment.
