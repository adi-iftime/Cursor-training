---
name: data-platform
description: >-
  Data governance, data engineering, data quality — three DAG agents (data_governance, data_engineer, data_quality).
  Open the section that matches the task; do not collapse registry nodes.
model: inherit
readonly: false
is_background: false
---

# Data platform (consolidated Cursor stub)

`config/agents.json` keeps **three separate ids** (`data_governance`, `data_engineer`, `data_quality`) with distinct `dependsOn` / `outputsTo`. This file is **one** Cursor entry point with **three** sections—each maps to its own folder under `agents/`.

## A. Data governance (`data_governance`)

- **Path:** `agents/data_governance/` — `agent.md`, `prompt.md`, `constraints.md`, `tools.json`
- **Focus:** Contracts, lineage, policy before engineering.

## B. Data engineer (`data_engineer`)

- **Path:** `agents/data_engineer/`
- **Focus:** Pipelines, transformations, jobs, catalog integration, tests.

## C. Data quality (`data_quality`)

- **Path:** `agents/data_quality/`
- **Focus:** Validation rules, anomalies vs contracts.

## Related (separate stub)

- **DevOps** (`devops` in the DAG): `.cursor/agents/devops.md` — not part of this consolidated data stub.
