# Global Enforcement Checks

| Check ID | Description | On fail |
| --- | --- | --- |
| G-LOG-01 | Structured log emitted for each agent action | Block handoff |
| G-DET-01 | Random seeds / versions recorded for reproducible runs | Warn; block if prod |
| G-DES-01 | Destructive ops require `confirmation_ref` | Block |
| G-TRC-01 | Handoff includes actor, artifact refs, rationale | Block |
