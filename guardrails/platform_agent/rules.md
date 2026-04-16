# Platform / coordination agents — rules

Applies to orchestration, planning, testing coordination, DevOps handoffs, documentation synthesis, and automation agents (`jira_story_generator`, `github_pr_description_writer`) that **coordinate** work without owning data-plane mutations.

1. **Inherit global rules** — `guardrails/global/rules.md` applies in full.
2. **Registry fidelity** — Use only agent ids from `config/agents.json`; do not invent agents or skip declared `dependsOn` edges.
3. **Handoffs** — Every outbound handoff MUST include `correlation_id`, `from_agent`, `to_agent`, and artifact references sufficient for audit.
4. **Integration boundaries** — Jira writes use **Atlassian MCP** tools (no ad-hoc REST clients in repo code for those flows). GitHub product updates use **`github.client.GitHubClient`** (no parallel HTTP stacks).
5. **No silent bypass** — Do not override guardrails, skip security/cost review agents when in scope, or hide failures from the orchestrator handoff format.
