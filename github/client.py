"""
Low-level GitHub REST client using GITHUB_TOKEN.

Uses GitHub REST API v2022-11-28 compatible endpoints.
"""

from __future__ import annotations

import base64
import json
import os
from typing import Any, Mapping
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

GITHUB_API_VERSION = "2022-11-28"
DEFAULT_BASE_URL = "https://api.github.com"


class GitHubAPIError(RuntimeError):
    """Raised when the GitHub API returns an error response."""

    def __init__(self, message: str, *, status: int | None = None, body: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class GitHubClient:
    """Minimal synchronous GitHub REST client (stdlib only)."""

    def __init__(
        self,
        token: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
    ) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN", "")
        if not self.token:
            raise ValueError("GITHUB_TOKEN is required (environment variable).")
        self.base_url = base_url.rstrip("/")

    def _headers(
        self,
        *,
        accept: str = "application/vnd.github+json",
        extra: Mapping[str, str] | None = None,
    ) -> dict[str, str]:
        h: dict[str, str] = {
            "Authorization": f"Bearer {self.token}",
            "Accept": accept,
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
            "User-Agent": "cursor-pr-lifecycle-agent/1.0",
        }
        if extra:
            h.update(dict(extra))
        return h

    def _request(
        self,
        method: str,
        path: str,
        *,
        accept: str = "application/vnd.github+json",
        body: bytes | None = None,
    ) -> tuple[int, bytes]:
        url = f"{self.base_url}{path}"
        req = Request(url, method=method, headers=self._headers(accept=accept), data=body)
        try:
            with urlopen(req, timeout=120) as resp:  # noqa: S310 — GitHub HTTPS only
                return resp.getcode() or 200, resp.read()
        except HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise GitHubAPIError(
                f"GitHub API error {e.code} for {method} {path}: {err_body[:500]}",
                status=e.code,
                body=err_body,
            ) from e

    def list_pulls(
        self,
        owner: str,
        repo: str,
        *,
        state: str = "open",
        per_page: int = 30,
    ) -> list[dict[str, Any]]:
        """List pull requests (detection / webhook stub consumer)."""
        status, data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls?state={state}&per_page={per_page}",
        )
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def get_pull(self, owner: str, repo: str, pull_number: int) -> dict[str, Any]:
        status, data = self._request("GET", f"/repos/{owner}/{repo}/pulls/{pull_number}")
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def get_pull_diff(self, owner: str, repo: str, pull_number: int) -> str:
        status, data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls/{pull_number}",
            accept="application/vnd.github.diff",
        )
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return data.decode("utf-8", errors="replace")

    def post_issue_comment(self, owner: str, repo: str, issue_number: int, body: str) -> dict[str, Any]:
        payload = json.dumps({"body": body}).encode("utf-8")
        status, data = self._request(
            "POST",
            f"/repos/{owner}/{repo}/issues/{issue_number}/comments",
            body=payload,
        )
        if status not in (200, 201):
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def list_pull_review_comments(self, owner: str, repo: str, pull_number: int) -> list[dict[str, Any]]:
        """Line-level review comments on the PR diff."""
        status, data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls/{pull_number}/comments",
        )
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def list_issue_comments(self, owner: str, repo: str, issue_number: int) -> list[dict[str, Any]]:
        status, data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/issues/{issue_number}/comments",
        )
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def list_reviews(self, owner: str, repo: str, pull_number: int) -> list[dict[str, Any]]:
        status, data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews",
        )
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def merge_pull(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        *,
        merge_method: str = "merge",
        commit_title: str | None = None,
    ) -> dict[str, Any]:
        payload_obj: dict[str, Any] = {"merge_method": merge_method}
        if commit_title:
            payload_obj["commit_title"] = commit_title
        payload = json.dumps(payload_obj).encode("utf-8")
        status, data = self._request(
            "PUT",
            f"/repos/{owner}/{repo}/pulls/{pull_number}/merge",
            body=payload,
        )
        if status not in (200, 201):
            raise GitHubAPIError(f"Merge failed status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def get_combined_status(self, owner: str, repo: str, ref: str) -> dict[str, Any]:
        """Legacy commit status (Contexts / Status API)."""
        status, data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/commits/{ref}/status",
        )
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def list_check_runs_for_commit(self, owner: str, repo: str, ref: str) -> dict[str, Any]:
        """Check Runs (GitHub Actions / modern CI)."""
        status, data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/commits/{ref}/check-runs?per_page=100",
        )
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def get_file_contents(
        self,
        owner: str,
        repo: str,
        path: str,
        *,
        ref: str,
    ) -> dict[str, Any]:
        encoded = quote(path, safe="")
        status, data = self._request(
            "GET",
            f"/repos/{owner}/{repo}/contents/{encoded}?ref={quote(ref)}",
        )
        if status != 200:
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))

    def put_file_contents(
        self,
        owner: str,
        repo: str,
        path: str,
        *,
        message: str,
        content_text: str,
        branch: str,
        sha: str | None = None,
    ) -> dict[str, Any]:
        """Create or update a single file on a branch (UTF-8 text)."""
        b64 = base64.b64encode(content_text.encode("utf-8")).decode("ascii")
        body_obj: dict[str, Any] = {
            "message": message,
            "content": b64,
            "branch": branch,
        }
        if sha:
            body_obj["sha"] = sha
        payload = json.dumps(body_obj).encode("utf-8")
        encoded = quote(path, safe="")
        status, data = self._request(
            "PUT",
            f"/repos/{owner}/{repo}/contents/{encoded}",
            body=payload,
        )
        if status not in (200, 201):
            raise GitHubAPIError(f"Unexpected status {status}", status=status)
        return json.loads(data.decode("utf-8"))
