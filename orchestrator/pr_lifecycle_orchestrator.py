"""
PR lifecycle orchestrator: review → fix → re-review → (optional) merge.

CLI:
  python -m orchestrator.pr_lifecycle_orchestrator --owner ORG --repo REPO --pr NUMBER

Detection stub:
  python -m orchestrator.pr_lifecycle_orchestrator --owner ORG --repo REPO --detect
"""

from __future__ import annotations

import argparse
import copy
import json
import logging
import sys
from pathlib import Path
from typing import Any

from agents.auto_merge_agent import agent as auto_merge_agent
from agents.pr_fixer_agent import agent as pr_fixer_agent
from agents.pr_review_agent import agent as pr_review_agent
from agents.pr_rereview_agent import agent as pr_rereview_agent
from github.client import GitHubClient
from github.pr_service import fetch_pr_context, load_workflow_config
from state.pr_state_tracker import PRStateTracker


REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = REPO_ROOT / "logs"
DEFAULT_WORKFLOW_PATH = REPO_ROOT / "config" / "workflow_config.json"


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / "pr_lifecycle.log"
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not any(isinstance(h, logging.FileHandler) for h in root.handlers):
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(fmt)
        root.addHandler(fh)
    if not any(type(h) is logging.StreamHandler for h in root.handlers):
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        root.addHandler(sh)


def detect_pull_requests(client: GitHubClient, owner: str, repo: str) -> list[dict[str, Any]]:
    """Stub for webhook/cron: list open PRs."""
    pulls = client.list_pulls(owner, repo, state="open")
    logging.getLogger(__name__).info("detect_pull_requests count=%s", len(pulls))
    return pulls


def _set_rereview_verdict(tracker: PRStateTracker, owner: str, repo: str, number: int, verdict: str | None) -> None:
    rec = tracker.load(owner, repo, number)
    rec.last_rereview_verdict = verdict
    tracker.save(rec)


def run_lifecycle(
    owner: str,
    repo: str,
    pr_number: int,
    *,
    workflow_path: Path | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    setup_logging()
    log = logging.getLogger(__name__)

    wf_path = workflow_path or DEFAULT_WORKFLOW_PATH
    workflow = load_workflow_config(str(wf_path))
    max_cycles = int(workflow.get("max_cycles", 3))

    client = GitHubClient(token=token)
    tracker = PRStateTracker()
    tracker.set_status(owner, repo, pr_number, "running")

    ctx = fetch_pr_context(client, owner, repo, pr_number)
    ctx_dict: dict[str, Any] = ctx.to_dict()

    log.info("lifecycle_start pr=%s/%s#%s", owner, repo, pr_number)

    review_out = pr_review_agent.run(ctx_dict)
    tracker.set_issues(owner, repo, pr_number, review_out.get("issues") or [])
    rec = tracker.load(owner, repo, pr_number)
    rec.last_review_summary = str(review_out.get("summary") or "")
    tracker.save(rec)

    original_issues = copy.deepcopy(review_out.get("issues") or [])
    current_issues = copy.deepcopy(review_out.get("issues") or [])

    rereview_out: dict[str, Any] | None = None
    merge_out: dict[str, Any] | None = None

    for cycle in range(max_cycles):
        log.info("cycle=%s current_issues=%s", cycle, len(current_issues))
        tracker.increment_cycle(owner, repo, pr_number)

        if current_issues:
            fix_out = pr_fixer_agent.run(
                ctx_dict,
                current_issues,
                client=client,
                workflow=workflow,
            )
            for action in fix_out.get("actions_taken") or []:
                if "committed" in str(action):
                    tracker.add_fix(owner, repo, pr_number, {"action": action, "cycle": cycle})
            current_issues = list(fix_out.get("issues") or [])
            if any("committed" in str(a) for a in fix_out.get("actions_taken") or []):
                ctx = fetch_pr_context(client, owner, repo, pr_number)
                ctx_dict = ctx.to_dict()

        rereview_out = pr_rereview_agent.run(ctx_dict, original_issues)
        _set_rereview_verdict(tracker, owner, repo, pr_number, str(rereview_out.get("recommendation")))

        verdict = rereview_out.get("recommendation")
        if verdict == "APPROVE":
            merge_out = auto_merge_agent.run(
                ctx_dict,
                rereview=rereview_out,
                remaining_issues=rereview_out.get("issues") or [],
                client=client,
                workflow=workflow,
            )
            tracker.set_final_decision(owner, repo, pr_number, str(merge_out.get("recommendation")))
            tracker.set_status(owner, repo, pr_number, "completed")
            break

        current_issues = list(rereview_out.get("issues") or [])

        if cycle >= max_cycles - 1:
            tracker.set_final_decision(owner, repo, pr_number, str(verdict or "max_cycles_reached"))
            tracker.set_status(owner, repo, pr_number, "stopped")
            log.warning("max_cycles reached without approval verdict=%s", verdict)
            break

    summary = {
        "owner": owner,
        "repo": repo,
        "number": pr_number,
        "review": review_out,
        "last_issues": current_issues,
        "rereview": rereview_out,
        "merge": merge_out,
        "cycles_used": tracker.load(owner, repo, pr_number).cycles,
    }
    log.info(
        "lifecycle_end cycles_used=%s merge=%s",
        summary["cycles_used"],
        (merge_out or {}).get("recommendation"),
    )
    (LOG_DIR / f"pr_{owner}_{repo}_{pr_number}_last.json").write_text(
        json.dumps(summary, indent=2, default=str),
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Autonomous PR lifecycle orchestrator")
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--pr", type=int, default=None, help="Pull request number")
    p.add_argument("--detect", action="store_true", help="List open PRs and exit")
    p.add_argument("--workflow", type=Path, default=None)
    args = p.parse_args(argv)

    setup_logging()
    client = GitHubClient()

    if args.detect:
        pulls = detect_pull_requests(client, args.owner, args.repo)
        print(json.dumps([{"number": x.get("number"), "title": x.get("title")} for x in pulls], indent=2))
        return 0

    if args.pr is None:
        print("--pr is required unless --detect", file=sys.stderr)
        return 2

    run_lifecycle(args.owner, args.repo, args.pr, workflow_path=args.workflow)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
