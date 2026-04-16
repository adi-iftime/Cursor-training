# Terminal Snake — architecture

## Overview

- **Domain:** `game/` — pure engine (`engine.py`, `snake.py`), stdin/stdout menu (`menu.py`), curses session (`main.py`).
- **Persistence:** `database/` — SQLite schema and `Database` facade.
- **Sub-agent facades:** `agents/*_agent.py` — non-overlapping boundaries (see `docs/MULTI_AGENT_PLAN.md`).
- **Composition:** `app/cli.py` → `agents/integration_agent.py`.

## Run

```bash
python -m app.cli
```

Optional: `python -m app.cli --db /path/to/snake.db`

## Database schema

- `users(id, username UNIQUE)`
- `scores(id, user_id FK, score, created_at ISO8601)`
