"""
Heuristic static analysis for unified PR diffs (no LLM required).

Extensible: add patterns or plug an LLM in the agent layer later.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any


def _issue_id(parts: str) -> str:
    return hashlib.sha256(parts.encode("utf-8")).hexdigest()[:12]


_AWS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")

# AWS documentation / SDK examples — must not be treated as leaked credentials.
_KNOWN_PLACEHOLDER_AWS_ACCESS_KEY_IDS: frozenset[str] = frozenset(
    {
        "AKIAIOSFODNN7EXAMPLE",  # canonical doc / IAM examples
    }
)


def _line_has_non_placeholder_aws_key(text: str) -> bool:
    """True if any AKIA… match is not a known documentation placeholder."""
    for m in _AWS_KEY.finditer(text):
        if m.group(0) not in _KNOWN_PLACEHOLDER_AWS_ACCESS_KEY_IDS:
            return True
    return False


_GH_TOKEN = re.compile(r"\b(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]+)\b")
_PEM = re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")
_MERGE = re.compile(r"^<<<<<<< ", re.M)
_ASSIGNMENT_SECRET = re.compile(r"(password|secret|api_key|apikey)\s*=\s*['\"][^'\"]{8,}['\"]", re.I)


def analyze_diff(diff_text: str) -> list[dict[str, Any]]:
    """Return structured issues found in a unified diff string."""
    issues: list[dict[str, Any]] = []
    current_file: str | None = None
    line_in_file = 0
    sensitive_warned: set[str] = set()

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            line_in_file = 0
            continue
        if line.startswith("+") and not line.startswith("+++"):
            line_in_file += 1
            text = line[1:]
            if _AWS_KEY.search(text) and _line_has_non_placeholder_aws_key(text):
                issues.append(
                    {
                        "id": _issue_id(f"aws:{current_file}:{line_in_file}"),
                        "severity": "HIGH",
                        "type": "possible_secret_aws_key",
                        "title": "Possible AWS access key in added line",
                        "detail": "Added line matches AWS access key pattern.",
                        "file": current_file,
                        "line": line_in_file,
                    }
                )
            if _GH_TOKEN.search(text):
                issues.append(
                    {
                        "id": _issue_id(f"gh:{current_file}:{line_in_file}"),
                        "severity": "HIGH",
                        "type": "possible_secret_github_token",
                        "title": "Possible GitHub token in added line",
                        "detail": "Added line matches GitHub PAT pattern.",
                        "file": current_file,
                        "line": line_in_file,
                    }
                )
            if _PEM.search(text):
                issues.append(
                    {
                        "id": _issue_id(f"pem:{current_file}:{line_in_file}"),
                        "severity": "HIGH",
                        "type": "possible_private_key_material",
                        "title": "Possible private key block in added line",
                        "detail": "PEM private key header detected in addition.",
                        "file": current_file,
                        "line": line_in_file,
                    }
                )
            if _ASSIGNMENT_SECRET.search(text):
                issues.append(
                    {
                        "id": _issue_id(f"assign:{current_file}:{line_in_file}"),
                        "severity": "MEDIUM",
                        "type": "possible_hardcoded_secret_assignment",
                        "title": "Possible hardcoded secret assignment",
                        "detail": "Assignment-style secret pattern in added line (review manually).",
                        "file": current_file,
                        "line": line_in_file,
                    }
                )
            if (
                current_file
                and current_file not in sensitive_warned
                and current_file.endswith((".env", ".pem", ".p12", ".pfx"))
            ):
                sensitive_warned.add(current_file)
                issues.append(
                    {
                        "id": _issue_id(f"sensitive_name:{current_file}"),
                        "severity": "HIGH",
                        "type": "sensitive_file_type",
                        "title": "Sensitive file type modified",
                        "detail": f"Changes touch `{current_file}` — verify no secrets committed.",
                        "file": current_file,
                        "line": line_in_file,
                    }
                )

    if _MERGE.search(diff_text):
        issues.append(
            {
                "id": _issue_id("merge:conflict"),
                "severity": "HIGH",
                "type": "merge_conflict_markers",
                "title": "Merge conflict markers present in diff",
                "detail": "Resolve conflicts before merge.",
                "file": None,
                "line": None,
            }
        )

    # Git reports missing EOF newline per file
    current: str | None = None
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:].strip()
        if line == r"\ No newline at end of file" and current:
            issues.append(
                {
                    "id": _issue_id(f"eof:{current}"),
                    "severity": "LOW",
                    "type": "missing_eof_newline",
                    "title": "Missing newline at end of file",
                    "detail": "POSIX text files should end with a newline.",
                    "file": current,
                    "line": None,
                    "autofix": True,
                }
            )

    # De-duplicate by id preserving order
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for i in issues:
        if i["id"] in seen:
            continue
        seen.add(i["id"])
        unique.append(i)
    return unique


def highest_severity(issues: list[dict[str, Any]]) -> str | None:
    order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    best: str | None = None
    for i in issues:
        sev = i.get("severity")
        if sev not in order:
            continue
        if best is None or order[sev] > order[best]:
            best = sev
    return best


def issue_fingerprint(issue: dict[str, Any]) -> str:
    return str(
        issue.get("type", "")
        + "|"
        + str(issue.get("file", ""))
        + "|"
        + str(issue.get("line", ""))
        + "|"
        + issue.get("title", "")
    )
