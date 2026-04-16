# Cost — Valid vs Invalid

## Valid

Daily Gold aggregate reads only last partition `event_date = current_date - 1` with clustering on `customer_id`.

## Invalid

`SELECT * FROM bronze.crm_events` full scan for a one-row lookup in a scheduled job.
