from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run_git(args: list[str], *, cwd: Path | None = None, dry_run: bool = False) -> tuple[int, str, str]:
    if dry_run:
        cmd = " ".join(["git", *args])
        return 0, f"[dry-run] {cmd}", ""
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd or REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ},
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def current_branch(*, dry_run: bool = False) -> str:
    code, out, _ = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], dry_run=dry_run)
    if code != 0:
        return "unknown"
    return out.strip()


def checkout_new_branch(branch: str, *, dry_run: bool = False) -> dict[str, Any]:
    code, out, err = _run_git(["checkout", "-B", branch], dry_run=dry_run)
    return {"ok": code == 0, "stdout": out, "stderr": err, "branch": branch}


def checkout_branch(branch: str, *, dry_run: bool = False) -> dict[str, Any]:
    code, out, err = _run_git(["checkout", branch], dry_run=dry_run)
    return {"ok": code == 0, "stdout": out, "stderr": err}


def add_commit(paths: list[str], message: str, *, dry_run: bool = False) -> dict[str, Any]:
    for p in paths:
        code, _, err = _run_git(["add", p], dry_run=dry_run)
        if code != 0:
            return {"ok": False, "stderr": err}
    code, out, err = _run_git(["commit", "-m", message], dry_run=dry_run)
    return {"ok": code == 0, "stdout": out, "stderr": err}


def merge_no_ff(branch: str, message: str, *, dry_run: bool = False) -> dict[str, Any]:
    code, out, err = _run_git(["merge", "--no-ff", branch, "-m", message], dry_run=dry_run)
    return {"ok": code == 0, "stdout": out, "stderr": err}


def try_push_upstream(branch: str, *, dry_run: bool = False) -> dict[str, Any]:
    if dry_run:
        return {"ok": True, "skipped": True, "detail": "[dry-run] push skipped"}
    code, out, err = _run_git(["push", "-u", "origin", branch])
    return {"ok": code == 0, "stdout": out, "stderr": err}


def try_gh_pr_create(title: str, body: str, head: str, base: str = "main", *, dry_run: bool = False) -> dict[str, Any]:
    if dry_run:
        return {"ok": True, "skipped": True, "detail": "[dry-run] gh pr create skipped"}
    proc = subprocess.run(
        [
            "gh",
            "pr",
            "create",
            "--title",
            title,
            "--body",
            body,
            "--head",
            head,
            "--base",
            base,
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ},
    )
    return {
        "ok": proc.returncode == 0,
        "stdout": proc.stdout or "",
        "stderr": proc.stderr or "",
    }
