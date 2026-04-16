---
name: agents-registry
description: Show where the DAG agent registry and edges are defined
---

# Agents registry

Open or summarize:

- `config/agents.json` — agent ids, `dependsOn`, `outputsTo`
- `config/orchestration_dag.json` — waves and parallelism

Validate with: `python -m pytest tests/test_agents_graph.py -q`
