# Security standards (blueprint)

- **Secrets:** Never commit secrets; use environment/secret stores; rotate and scope minimally.
- **Access:** Least privilege for service principals; review high-privilege paths in **Security** agent pass.
- **Privacy:** Minimize PII in logs and artifacts; document lawful basis and retention where applicable.
- **Dependencies:** Track CVEs; patch policy aligned with risk tier from orchestrator work order.
