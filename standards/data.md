# Data standards (blueprint)

- **Contracts:** Schema, semantics, and SLAs defined before pipelines depend on them; PII classification documented.
- **Lineage:** Downstream consumers must be able to trace to sources and owning agent/work order.
- **Quality:** Measurable checks (`data_quality` agent); anomalies surfaced with severity.
- **Storage:** Prefer incremental, partition-friendly patterns; document retention and cost drivers for **Cost Analyst** review.
