## orders 
- Grain: one row per order. Key: order_id (99,441 rows, all unique).
- Links to customers via customer_id.
- 8 statuses, clean lowercase values; 97% delivered.
- Missing delivery dates (2,965) are mostly normal: undelivered orders.
- Anomaly: some orders are 'delivered' with no delivery date -> quarantine in silver.
- All purchase dates parse as timestamps; no delivery-before-purchase cases.