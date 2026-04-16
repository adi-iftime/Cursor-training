"""Tests for data platform orchestrator."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from orchestrator.data_platform_context import default_work_order
from orchestrator.data_platform_orchestrator import run_flow


def test_run_flow_runs_all_non_conditional_steps() -> None:
    wo = default_work_order("ingest CRM data")
    wo["risk_tier"] = "low"
    wo["include_analyst"] = False
    out = run_flow(wo, repo_root=Path(__file__).resolve().parent.parent)
    assert out["status"] == "completed"
    agents = [t.get("agent") for t in out["trace"] if not t.get("skipped")]
    assert "data_analyst" not in agents
    assert agents[-1] == "documentation" or "documentation" in agents


def test_conditional_analyst_runs_when_enabled() -> None:
    wo = default_work_order("dashboard")
    wo["include_analyst"] = True
    out = run_flow(wo, repo_root=Path(__file__).resolve().parent.parent)
    agents = [t.get("agent") for t in out["trace"] if not t.get("skipped")]
    assert "data_analyst" in agents


def test_writes_run_artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import orchestrator.data_platform_orchestrator as m

    monkeypatch.setattr(m, "LOG_DIR", tmp_path)
    monkeypatch.setattr(m, "setup_logging", lambda: None)
    wo = default_work_order("x")
    wo["include_analyst"] = False
    out = run_flow(wo, repo_root=m.REPO_ROOT, correlation_id="fixed-id")
    files = list(tmp_path.glob("run_*.json"))
    assert files
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["correlation_id"] == "fixed-id"
