# Multi-agent task split (pre-implementation)

Work is split so each sub-agent owns a non-overlapping surface. Implementation lives in domain packages; `agents/` modules are the explicit boundaries for each role.

| Sub-agent | Responsibilities | Primary modules |
|-----------|------------------|-----------------|
| **Game Engine Agent** | Snake movement, direction rules, wall/self collision, tick/step loop, in-session score on food | `game/snake.py`, `game/engine.py`, `agents/game_engine_agent.py` |
| **Menu Agent** | Terminal menu rendering, option validation, navigation (play / leaderboard / users / exit) | `game/menu.py`, `agents/menu_agent.py` |
| **Database Agent** | SQLite schema, user registration, score rows with timestamps | `database/models.py`, `database/db.py`, `agents/database_agent.py` |
| **Leaderboard Agent** | Top-N global ranking, per-user score lists, sort order | `agents/leaderboard_agent.py` (queries via `database/db.py`) |
| **Testing Agent** | Pytests for scoring, persistence, leaderboard ordering, engine invariants | `tests/`, `agents/testing_agent.py` |
| **Integration Agent** | CLI entry, session flow (username → play → persist), module wiring | `app/cli.py`, `game/main.py`, `agents/integration_agent.py` |

**Integration rule:** Game logic never imports database; `app/cli.py` and `integration_agent` compose I/O, menu, engine, and persistence.
