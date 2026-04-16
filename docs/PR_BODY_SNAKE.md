## What this change does

This pull request adds a **terminal Snake game**: play with the arrow keys, eat food to grow and score, and avoid walls and self-collisions. Scores are stored per user in **SQLite** so leaderboards and user lists **persist between runs**.

## Why it exists

The code is split to mirror this repo’s **multi-agent DAG** (orchestrator, planner, data governance, engineering, quality, security, etc.). Work is tracked under Jira epic **[SCRUM-6](https://levi9-team-ivfys2q6.atlassian.net/browse/SCRUM-6)** with stories **SCRUM-7**–**SCRUM-17** (one per agent role).

## How to try it

1. Check out this branch.
2. From the **repository root**:

   ```bash
   python -m app.cli
   ```

3. Menu: **Start game**, **Leaderboard**, **Users**, or **Exit**.

You can also run `./scripts/run_snake.sh`. The default database path is `data/snake.db` (gitignored).

## Docs in this branch

| File | Contents |
| --- | --- |
| `docs/SNAKE_GAME.md` | Run instructions |
| `docs/DAG_SNAKE_OWNERSHIP.md` | Module ↔ agent mapping |
| `docs/JIRA_SNAKE_KEYS.md` | Jira key list |

## Tests

```bash
python -m pytest -q
```

## For reviewers

- Confirm the game and menu behave as expected.
- Confirm scores survive a restart.
- Confirm no secrets are committed.
