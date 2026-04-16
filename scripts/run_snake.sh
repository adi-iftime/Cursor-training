#!/usr/bin/env bash
# DAG owner: devops — single command to run the game from repo root.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec python -m app.cli "$@"
