# Phase 3 SQL Analytical Layer Notes

## Engine and loading approach

DuckDB is used because the repository has no PostgreSQL setup. SQL files are executed from the repository root against a local derived database at `data/processed/ecommerce.duckdb`. The database contains views that read the cleaned CSVs directly; files under `data/cleaned/` are never modified.

`sql/01_data_validation.sql` creates the source views and reports row counts, distinct keys, and line-to-key differences. The other SQL files create analytical views and return a representative result set.

## View grains

- `amazon_sales`: Amazon order-line grain; `order_id` repeats.
- `international_sales`: international sales-line grain; no order ID.
- `may_product_prices` and `march_product_prices`: SKU/size snapshot grain; `sku` is unique in each snapshot.
- `stock_snapshot`: SKU/size/colour snapshot grain; `sku_code` is not unique.
- `warehouse_rates`: cost-head reference grain.
- `expense_report`: mixed detail/summary report grain.

## Supported SQL analyses

- `amazon_monthly_sales` and `amazon_monthly_sales_scoped`: reported amount, amount coverage, zero amount/quantity counts, reported units, distinct orders, line count, safe reported-value-per-order denominator, and month-over-month amount change using `LAG`.
- `international_monthly_sales`: reported gross amount and pieces by month, kept separate because currency is absent.
- `amazon_status_analysis`: distinct-order status proxies for cancelled, returned, and delivered labels using explicit `CASE WHEN` logic.
- `amazon_platform_performance`: source-local channel/fulfilment mix using line and distinct-order counts; it is not a cross-platform performance KPI.
- `amazon_category_performance` and `amazon_sku_performance`: category/SKU rankings using window functions.
- `amazon_product_match_summary`: left-join match coverage to the May product snapshot.
- `amazon_fulfilment_performance`, `warehouse_provider_comparison`, and `stock_snapshot_summary`: source-local operational/reference summaries; no warehouse or expense allocation is performed.

## Guardrails

- Amount and gross amount are reported sales fields, not net sales or profit.
- Amazon and international amounts are not combined across currency/scope boundaries.
- Order counts use `COUNT(DISTINCT order_id)`; line counts remain separately labelled.
- `NULLIF` protects ratio denominators from zero.
- Cancelled and returned values are status proxies, not true cancellation/return rates.
- No profit, margin, customer, inventory-turnover, or delivery-time KPI is created.
- The product join is a candidate SKU enrichment join. Parent `sku` uniqueness is checked before relying on many-to-one behavior.
