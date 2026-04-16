# Sample User Request

> We need to land daily CRM exports from S3, conform customer records to our standard schema, and publish a Gold table for daily revenue by region. PII must be masked. Add DQ rules for key completeness and run this through our normal deploy process. After deploy, a dashboard on Gold for exec review would help.

**Implicit requirements:** Medallion layers, governance contract, tests, security review, CI/CD, cost check, optional analyst deliverable.
