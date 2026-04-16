# DAG owner: orchestrator (composition only) — thin CLI entry for the scaffold.
"""Application entry: `python -m app.cli` from repository root."""

from __future__ import annotations


def main() -> None:
    print(
        "Multi-agent data platform scaffold. "
        "See README.md, prompts/system_overview.md, and config/orchestration.json."
    )


if __name__ == "__main__":
    main()
