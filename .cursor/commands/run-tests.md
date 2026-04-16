---
name: run-tests
description: Run the Python test suite with pytest from the repository root
---

# Run tests

Execute from the workspace root:

```bash
python -m pytest -q
```

For a single file:

```bash
python -m pytest tests/test_agents_graph.py -q
```

Ensure dev dependencies are installed (`requirements-dev.txt`).
