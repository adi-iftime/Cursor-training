"""CLI: python -m org.run_simulation [--dry-run] [--story KEY]"""

from __future__ import annotations

import argparse
import json
import sys

from org.simulation_engine import run_simulation


def main() -> int:
    p = argparse.ArgumentParser(description="AI Engineering Organization Simulator")
    p.add_argument("--dry-run", action="store_true", help="Skip mutating git state (still writes sim_workspace + logs).")
    p.add_argument("--story", default=None, help="Jira story key (default: config org_simulation.json).")
    p.add_argument("--json", action="store_true", help="Print result as JSON.")
    args = p.parse_args()
    out = run_simulation(dry_run=args.dry_run, story_key=args.story)
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(
            f"story={out['story_key']} dry_run={out['dry_run']} "
            f"review={out['review_verdict']} merge_done={out['merge_done']}",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
