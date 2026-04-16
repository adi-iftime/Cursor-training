from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from org.communication_log import append_message
from org.git_workflow import (
    REPO_ROOT,
    add_commit,
    checkout_branch,
    checkout_new_branch,
    current_branch,
    merge_no_ff,
    try_gh_pr_create,
    try_push_upstream,
)
from org.org_state import load_state, save_state
from org.roles import (
    BackendEngineer,
    DataEngineer,
    DevOpsEngineer,
    ProductManager,
    ReviewerAgent,
    TechLead,
    TesterAgent,
)

CONFIG_PATH = REPO_ROOT / "config" / "org_simulation.json"


def _load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def run_simulation(
    *,
    dry_run: bool = False,
    story_key: str | None = None,
    communication_log_path: Path | None = None,
    org_state_path: Path | None = None,
) -> dict[str, Any]:
    """
    Execute a minimal end-to-end org simulation for one story:
    planning → assignment → implementation (git branch + files) → review → (optional merge).
    """
    cfg = _load_config()
    state = load_state(path=org_state_path)
    sk = story_key or str(cfg.get("primary_story_key") or "SCRUM-4")
    epic = str(cfg.get("jira_epic_key") or state["sprint"].get("jira_epic_key") or "SCRUM-3")

    pm = ProductManager()
    tl = TechLead()
    be = BackendEngineer()
    rev = ReviewerAgent()
    devops = DevOpsEngineer()
    tester = TesterAgent()
    de = DataEngineer()

    out: dict[str, Any] = {"story_key": sk, "dry_run": dry_run, "phases": []}

    # STEP 1 — Sprint planning (PM)
    m1 = pm.sprint_planning_message(epic_key=epic, story_keys=[sk])
    append_message(m1, path=communication_log_path)
    state["sprint"]["status"] = "active"

    # STEP 2 — Assignment (Tech Lead)
    ticket = (state.get("jira_tickets") or {}).get(sk) or {}
    assignee = str((state.get("agent_assignments") or {}).get(sk) or "backend_engineer")
    paths = list(ticket.get("file_paths") or ["org/", "logs/communication.json", "state/org_state.json"])
    m2 = tl.assign_story(story_key=sk, engineer_role=assignee, file_paths=paths)
    append_message(m2, path=communication_log_path)

    # STEP 3 — Parallel hint: data engineer handoff (independent stub)
    m_de = de.task_handoff(
        story_key=sk,
        content="Data contracts noted; no warehouse changes for this story.",
    )
    append_message(m_de, path=communication_log_path)

    # Implementation branch + artifact
    branch = f"sim/{sk}-delivery"
    orig = current_branch(dry_run=dry_run)
    git_checkout = checkout_new_branch(branch, dry_run=dry_run)
    out["phases"].append({"name": "git_branch", "result": git_checkout})

    workspace = REPO_ROOT / "sim_workspace" / sk
    workspace.mkdir(parents=True, exist_ok=True)
    delivery = workspace / "delivery.md"
    delivery.write_text(
        f"# Delivery {sk}\n\n"
        f"- Epic: {epic}\n"
        f"- Paths: {', '.join(paths)}\n"
        f"- Acceptance: org package runnable; comms log valid.\n",
        encoding="utf-8",
    )
    rel_paths = [f"sim_workspace/{sk}/delivery.md"]

    commit_msg = f"{sk} sim delivery - org simulator workspace"
    commit_res = add_commit(rel_paths, commit_msg, dry_run=dry_run)
    out["phases"].append({"name": "git_commit", "result": commit_res})

    m_impl = be.implementation_update(story_key=sk, branch=branch, paths=rel_paths)
    append_message(m_impl, path=communication_log_path)

    # STEP 4 — Review
    review_paths = ["org/__init__.py", "logs/communication.json", "state/org_state.json", rel_paths[0]]
    verdict = rev.review_delivery(story_key=sk, delivery_paths=review_paths)
    append_message(verdict, path=communication_log_path)

    pr_url = ""
    if verdict["type"] == "approval":
        state.setdefault("prs", {})[sk] = {
            "branch": branch,
            "status": "approved",
            "reviewer": rev.id,
        }
        ticket["status"] = "In Review"
        if os.environ.get("ORG_SIM_PUSH") == "1":
            push_res = try_push_upstream(branch, dry_run=dry_run)
            out["phases"].append({"name": "git_push", "result": push_res})
        if os.environ.get("ORG_SIM_PR") == "1":
            pr_res = try_gh_pr_create(
                title=f"[{sk}] Org simulator delivery",
                body=f"Automated PR from org simulation.\n\nStory: {sk}\nEpic: {epic}",
                head=branch,
                base=str(cfg.get("base_branch") or "main"),
                dry_run=dry_run,
            )
            out["phases"].append({"name": "gh_pr", "result": pr_res})
            if pr_res.get("stdout"):
                pr_url = str(pr_res["stdout"]).strip()
                state["prs"][sk]["url"] = pr_url
    else:
        state.setdefault("prs", {})[sk] = {"branch": branch, "status": "changes_requested"}

    # Merge policy: never merge without explicit env (review-before-merge)
    merge_done = False
    if (
        verdict["type"] == "approval"
        and not dry_run
        and os.environ.get("ORG_SIM_ALLOW_MERGE") == "1"
    ):
        # Return to main and merge --no-ff (never merge in dry-run)
        co = checkout_branch(str(cfg.get("base_branch") or "main"), dry_run=dry_run)
        out["phases"].append({"name": "checkout_main", "result": co})
        if co.get("ok"):
            mg = merge_no_ff(branch, f"Merge {sk} org simulation delivery", dry_run=dry_run)
            out["phases"].append({"name": "merge", "result": mg})
            merge_done = bool(mg.get("ok"))
            checkout_branch(orig, dry_run=dry_run)

    if verdict["type"] == "approval":
        ticket["status"] = "Done" if merge_done else "Ready to merge"
        state["sprint_progress"]["done"] = 1 if merge_done else 0
    else:
        ticket["status"] = "In Progress"

    state.setdefault("jira_tickets", {})[sk] = ticket
    save_state(state, path=org_state_path)

    # STEP 6 — Post-merge checks (messages only)
    m_dev = devops.stability_check(
        story_key=sk,
        ok=verdict["type"] == "approval",
        detail="Pipeline stub: no deploy in dry-run." if dry_run else "Local merge/check complete.",
    )
    append_message(m_dev, path=communication_log_path)
    m_test = tester.regression_note(
        story_key=sk,
        passed=verdict["type"] == "approval",
        detail="pytest org tests (if run) expected green for approved path.",
    )
    append_message(m_test, path=communication_log_path)

    out["merge_done"] = merge_done
    out["review_verdict"] = verdict["type"]
    return out
