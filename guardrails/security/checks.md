# Security Checks

| Check ID | Description | On fail |
| --- | --- | --- |
| SEC-PII-01 | PII fields mapped to controls (masking, RBAC) | Block |
| SEC-IAM-01 | IAM diff within policy bounds | Block prod |
| SEC-LEAK-01 | Secret scan + public exposure checks clean | Block |
