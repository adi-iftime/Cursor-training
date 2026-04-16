# SQL — Examples

## Idempotent merge (conceptual)

```sql
MERGE INTO silver.crm_customer AS t
USING bronze.crm_customer_staging AS s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...
```
