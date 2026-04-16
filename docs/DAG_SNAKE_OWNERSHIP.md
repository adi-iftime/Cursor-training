# Snake game — DAG agent ownership

Execution follows `config/agents.json` + `config/orchestration_dag.json`. **Parallelism:** schema/validation can be reviewed in parallel with engine design; implementation order in-repo follows dependency gates.

| Agent | Owns in this feature |
| --- | --- |
| **orchestrator** | `app/cli.py` composition; runbook `docs/SNAKE_GAME.md` |
| **planner** | Architecture boundaries, Jira stories (MCP), `config/settings.py` contract |
| **data_governance** | `database/models.py`, table shapes |
| **data_engineer** | `database/db.py`, `game/*.py` (engine, snake, menu, main) |
| **data_quality** | `database/validation.py` |
| **tester** | `tests/test_*.py` for snake |
| **security** | Parameterized SQL, username validation, no secrets in repo |
| **devops** | `scripts/run_snake.sh` |
| **cost_optimizer** | Notes: O(1) tick in `game/engine.py` |
| **data_analyst** | `database/analytics.py` (leaderboard reads) |
| **documentation** | `docs/SNAKE_GAME.md`, this file |
