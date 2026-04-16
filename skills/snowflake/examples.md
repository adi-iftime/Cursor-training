# Snowflake — Examples

## Layer naming

`BRONZE.CRM_RAW`, `SILVER.CRM_CUSTOMER`, `GOLD.CRM_KPI_DAILY`

## Task chain

`BRONZE_LOAD` → `SILVER_MERGE` → `GOLD_AGG` (orchestrated via TASK + AFTER)
