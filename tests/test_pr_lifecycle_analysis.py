"""Unit tests for PR lifecycle diff analysis and CI evaluation."""

from __future__ import annotations

from agents.pr_review_agent.analysis import analyze_diff
from github.pr_service import PullRequestContext, evaluate_ci_passed


def test_analyze_diff_detects_aws_key() -> None:
    diff = """
diff --git a/x.py b/x.py
--- a/x.py
+++ b/x.py
@@ -1 +1 @@
+key = AKIAIOSFODNN7EXAMPLE
"""
    issues = analyze_diff(diff)
    assert any(i["type"] == "possible_secret_aws_key" for i in issues)


def test_analyze_diff_merge_conflict() -> None:
    diff = "<<<<<<< HEAD\n"
    issues = analyze_diff(diff)
    assert any(i["type"] == "merge_conflict_markers" for i in issues)


def test_evaluate_ci_passed_required_check_substring() -> None:
    ctx = PullRequestContext(
        owner="o",
        repo="r",
        number=1,
        title="t",
        body="",
        head_sha="abc",
        head_ref="h",
        base_ref="main",
        user_login="u",
        draft=False,
        mergeable=True,
        diff_text="",
        combined_status={},
        check_runs={
            "check_runs": [
                {
                    "name": "ci / tests",
                    "status": "completed",
                    "conclusion": "success",
                }
            ]
        },
    )
    ok, reason = evaluate_ci_passed(ctx, required_checks=["ci", "test"])
    assert ok is True
    assert "satisfied" in reason
