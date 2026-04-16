"""
Data platform multi-agent orchestrator — executes `config/orchestration.json` flow.

CLI:
  python -m orchestrator.data_platform_orchestrator --request "Build CRM pipeline"
  python -m orchestrator.data_platform_orchestrator --work-order path/to/order.json

Handlers live in `orchestrator/data_platform_registry.py` (stubs by default).
Swap them for LLM or service calls without changing the graph.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import uuid
from pathlib import Path
from typing import Any

from orchestrator.data_platform_context import WorkContext, default_work_order
from orchestrator.data_platform_registry import run_agent_step

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = REPO_ROOT / "logs"
ORCH_CONFIG = REPO_ROOT / "config" / "orchestration.json"


def setup_logging(*, verbose: bool = False) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    path = LOG_DIR / "data_platform_orchestrator.log"
    handlers: list[logging.Handler] = [logging.FileHandler(path, encoding="utf-8")]
    if verbose:
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=handlers,
        force=True,
    )


def load_orchestration() -> dict[str, Any]:
    return json.loads(ORCH_CONFIG.read_text(encoding="utf-8"))


def run_flow(
    work_order: dict[str, Any],
    *,
    repo_root: Path | None = None,
    correlation_id: str | None = None,
) -> dict[str, Any]:
    """
    Walk `flow` in config/orchestration.json, invoke registered handlers per step.
    Conditional steps (e.g. data_analyst) require work_order[\"include_analyst\"] True.
    """
    cid = correlation_id or str(uuid.uuid4())
    root = repo_root or REPO_ROOT
    orch = load_orchestration()
    flow = orch.get("flow") or []

    ctx = WorkContext(correlation_id=cid, repo_root=root, work_order=work_order)
    trace: list[dict[str, Any]] = []
    log = logging.getLogger(__name__)
    log.info("run_flow start correlation_id=%s", cid)

    for step in sorted(flow, key=lambda s: int(s.get("step", 0))):
        agent_id = step.get("agent")
        if not agent_id:
            continue
        if step.get("conditional") and not work_order.get("include_analyst"):
            trace.append(
                {
                    "step": step.get("step"),
                    "agent": agent_id,
                    "skipped": True,
                    "reason": "conditional_not_enabled",
                }
            )
            continue

        out = run_agent_step(agent_id, ctx, step)
        ctx.record(agent_id, out)
        trace.append(
            {
                "step": step.get("step"),
                "agent": agent_id,
                "action": step.get("action"),
                "correlation_id": cid,
                "output": out,
            }
        )
        log.info(
            "step_done step=%s agent=%s status=%s",
            step.get("step"),
            agent_id,
            out.get("status"),
        )

    result = {
        "correlation_id": cid,
        "status": "completed",
        "work_order": work_order,
        "trace": trace,
        "halt_conditions_evaluated": orch.get("haltConditions", []),
    }
    out_path = LOG_DIR / f"run_{cid}.json"
    out_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    log.info("run_flow end wrote %s", out_path)
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Data platform orchestrator")
    p.add_argument("--request", type=str, help="Natural language work request")
    p.add_argument("--work-order", type=Path, help="JSON file with work order fields")
    p.add_argument("--include-analyst", action="store_true", help="Run conditional data_analyst step")
    p.add_argument("--risk", choices=("low", "medium", "high"), default="medium")
    p.add_argument("--correlation-id", type=str, default=None)
    p.add_argument(
        "--verbose",
        action="store_true",
        help="Log steps to stdout (default: log file only; JSON on stdout)",
    )
    args = p.parse_args(argv)
    setup_logging(verbose=args.verbose)

    if args.work_order:
        wo = json.loads(Path(args.work_order).read_text(encoding="utf-8"))
    elif args.request:
        wo = default_work_order(args.request)
        wo["risk_tier"] = args.risk
    else:
        print("Provide --request or --work-order", file=sys.stderr)
        return 2

    if args.work_order is not None and args.risk:
        wo.setdefault("risk_tier", args.risk)
    if args.include_analyst:
        wo["include_analyst"] = True
    wo.setdefault("include_analyst", False)

    result = run_flow(wo, correlation_id=args.correlation_id)
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
