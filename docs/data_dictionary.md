# Data dictionary

The sample dataset contains 150 fictional order records. Prices and costs are illustrative INR values.

| Field | Description |
|---|---|
| order_id | Unique transaction identifier |
| order_date | Order date (YYYY-MM-DD) |
| customer_id | Fictional customer key |
| product / category | Product and product category |
| region / city | Sales geography |
| sales_channel | Online, Retail or Partner |
| quantity | Units; must be greater than zero |
| unit_price | Selling price per unit (INR) |
| unit_cost | Cost per unit (INR) |
| revenue | quantity × unit_price |
| total_cost | quantity × unit_cost |
| profit | revenue − total_cost |
| profit_margin_pct | profit ÷ revenue × 100 |

Quality rules: required text fields cannot be blank; dates must parse; quantity and unit price must be positive; unit cost must be non-negative and no greater than unit price; first valid occurrence of an order ID is retained and later duplicates are reported.
