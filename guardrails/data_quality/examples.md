# Data Quality — Valid vs Invalid

## Valid

Expectation suite `CRM-S-001@v3` runs post-Silver merge; null rate on `customer_id` < 0.01%.

## Invalid

Gold table published after schema drift (`new_column` not in contract) without version bump.
