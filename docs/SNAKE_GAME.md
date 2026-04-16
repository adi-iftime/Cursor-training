# Terminal Snake (DAG delivery)

## Run

From repository root:

```bash
python -m app.cli
```

Or:

```bash
./scripts/run_snake.sh
```

## Controls

- Arrow keys: move  
- `Q`: quit current session (score is still saved)

## Data

SQLite database defaults to `data/snake.db` (gitignored). Override with `--db PATH`.

## Module map (agent ownership)

See `docs/DAG_SNAKE_OWNERSHIP.md` and Jira keys in `docs/JIRA_SNAKE_KEYS.md`.
