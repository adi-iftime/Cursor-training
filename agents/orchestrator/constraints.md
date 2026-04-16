# Guardrails — Orchestrator (DAG execution)

- **Source of truth:** `config/agents.json` (node registry + `dependsOn` / `outputsTo`) and **`config/orchestration_dag.json`** (waves + parallelism). Do not invent agents, rename agents, or bypass dependencies.
- **Ordering:** Never run an agent until **all** of its `dependsOn` agents have completed successfully for the current work order (unless a conditional agent is explicitly skipped by scope).
- **Parallelism:** When multiple agents share the same wave and their dependencies are satisfied, **execute them in parallel** (conceptually concurrent tasks / sub-agents). Do not collapse the DAG into a single sequential chain if parallel is valid.
- **Planner / governance:** Do not skip **planner** or **data_governance** when the work order touches governed data or engineering delivery.
- **Downstream gates:** Do not run **cost_optimizer** before **devops** (and its prerequisites) when cost review targets deployed or deployable artifacts. Do not run **documentation** as the final consolidation pass until **wave_parallel_optimize_insight** outputs exist when in scope.
- **Jira:** Trace work with **Atlassian MCP** (issues/comments/assignments per `config/jira_agent_assignees.json` and Planner rules). Do not claim Jira updates without MCP evidence.
- **Git:** Use the real repository — branch, commit, push, PR, review, merge for substantive units of work when applicable.
