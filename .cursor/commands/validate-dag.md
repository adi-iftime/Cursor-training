---
name: validate-dag
description: Validate agents.json graph consistency and config JSON parse
---

# Validate orchestration config

```bash
python -m pytest tests/test_agents_graph.py tests/test_config_json.py -q
```

Confirms every `dependsOn` / `outputsTo` target exists in `config/agents.json` and core JSON configs parse.
