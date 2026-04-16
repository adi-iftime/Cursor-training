"""
Registers callable handlers per agent id.

Replace stubs with LLM-backed implementations or remote workers by swapping
entries in AGENT_HANDLERS.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from orchestrator.data_platform_context import WorkContext

AgentHandler = Callable[[WorkContext, dict[str, Any]], dict[str, Any]]


def _read_prompt(repo_root: Path, agent_id: str) -> str | None:
    p = repo_root / "agents" / agent_id / "prompt.md"
    if not p.is_file():
        return None
    return p.read_text(encoding="utf-8")[:2000]


def _stub(
    agent_id: str,
    ctx: WorkContext,
    step: dict[str, Any],
    *,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Deterministic stub: structured payload for tracing and future LLM replacement."""
    prompt_preview = _read_prompt(ctx.repo_root, agent_id)
    out: dict[str, Any] = {
        "status": "success",
        "agent": agent_id,
        "action": step.get("action"),
        "summary": f"Stub handler for {agent_id}:{step.get('action')}; prior={ctx.prior_summary()}",
        "artifacts": [],
        "guardrails_checked": [f"agents/{agent_id}/constraints.md"],
        "prompt_loaded": bool(prompt_preview),
    }
    if extra:
        out["detail"] = extra
    return out


def handle_orchestrator(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    wo = ctx.work_order
    return _stub(
        "orchestrator",
        ctx,
        step,
        extra={
            "work_order_emitted": {
                "intent": wo.get("intent"),
                "risk_tier": wo.get("risk_tier"),
                "scope": wo.get("scope"),
            }
        },
    )


def handle_planner(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("planner", ctx, step, extra={"jira_stub": "PLAN-001"})


def handle_data_governance(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("data_governance", ctx, step, extra={"contract_stub": "CTR-001"})


def handle_data_engineer(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("data_engineer", ctx, step, extra={"layers": ["bronze", "silver", "gold"]})


def handle_data_quality(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("data_quality", ctx, step, extra={"expectations_stub": 3})


def handle_tester(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("tester", ctx, step, extra={"tests_stub": "passed"})


def handle_security(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    tier = str(ctx.work_order.get("risk_tier", "medium")).lower()
    review = "enhanced" if tier == "high" else "standard"
    return _stub("security", ctx, step, extra={"review": review})


def handle_devops(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("devops", ctx, step, extra={"deploy_target": "staging"})


def handle_cost_optimizer(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("cost_optimizer", ctx, step, extra={"savings_pct_estimate": 5})


def handle_documentation(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("documentation", ctx, step, extra={"docs_stub": "updated"})


def handle_data_analyst(ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    return _stub("data_analyst", ctx, step, extra={"layer": "gold_only"})


AGENT_HANDLERS: dict[str, AgentHandler] = {
    "orchestrator": handle_orchestrator,
    "planner": handle_planner,
    "data_governance": handle_data_governance,
    "data_engineer": handle_data_engineer,
    "data_quality": handle_data_quality,
    "tester": handle_tester,
    "security": handle_security,
    "devops": handle_devops,
    "cost_optimizer": handle_cost_optimizer,
    "documentation": handle_documentation,
    "data_analyst": handle_data_analyst,
}


def run_agent_step(agent_id: str, ctx: WorkContext, step: dict[str, Any]) -> dict[str, Any]:
    fn = AGENT_HANDLERS.get(agent_id)
    if fn is None:
        return {
            "status": "error",
            "agent": agent_id,
            "action": step.get("action"),
            "summary": f"No handler registered for agent {agent_id}",
            "artifacts": [],
        }
    return fn(ctx, step)


def handlers_as_json() -> str:
    return json.dumps(sorted(AGENT_HANDLERS.keys()), indent=2)
