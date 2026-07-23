# Phase 3: SQL Analytical Layer Validation

**Final status: PASS WITH WARNINGS**

## Environment and dependencies

- SQL engine: DuckDB 1.5.5.
- Existing dependency: pandas 2.2.3.
- Installed missing lightweight dependency: pytest 9.1.1.
- `requirements.txt` was not present; no PostgreSQL, Docker, Kaggle, cloud, or large dependency was installed.
- DuckDB successfully read `data/cleaned/amazon_sale_report_cleaned.csv` and returned 128,969 rows in the initial smoke test.
- Derived database: `data/processed/ecommerce.duckdb`.

## Files inspected and changed

Inspected:

- Seven files under `data/cleaned`.
- `docs/kpi_definition.md`.
- `reports/validation_reports/phase_0_validation.md`.
- `reports/validation_reports/phase_1_validation.md`.
- Existing repository structure and Python environment.

Created or modified:

- `sql/01_data_validation.sql`
- `sql/02_sales_analysis.sql`
- `sql/03_product_analysis.sql`
- `sql/04_operations_analysis.sql`
- `docs/sql_analysis_notes.md`
- `scripts/run_sql_layer.py`
- `tests/test_phase_3_sql.py`
- `data/processed/ecommerce.duckdb`
- `reports/validation_reports/phase_3_validation.md`

No file under `data/cleaned/` was modified.

## Queries created

- Source views and table/grain validation.
- Amazon monthly reported sales, units, distinct orders, safe reported-value-per-order denominator, and month-over-month change using `LAG`.
- International monthly gross amount and pieces, kept separate from Amazon.
- Cancellation, return, and delivery status proxies using `CASE WHEN` and distinct order flags.
- Channel and fulfilment performance.
- Category and SKU performance using `RANK()` window functions.
- Candidate product-SKU match coverage using a left join.
- Warehouse provider rate comparison and stock snapshot summaries.

## Tests and SQL execution

- All four SQL files executed successfully through DuckDB.
- `pytest -q tests/test_phase_3_sql.py`: 4 tests passed.
- Product join row-count test passed: joining Amazon sales to the unique May product snapshot did not multiply rows.
- Safe ratio and month-over-month window output tests passed.
- No profit or margin view was created.

## SQL versus Pandas reconciliation

| Result | DuckDB | Pandas | Status |
|---|---:|---:|---|
| Amazon monthly reported amount total | 78,590,043.30 | 78,590,043.30 | PASS |
| Amazon distinct order count | 120,378 | 120,378 | PASS |
| Amazon reported units | 116,646 | 116,646 | PASS |
| International monthly gross amount total | 10,834,927.19 | 10,834,927.19 | PASS |
| Stock snapshot reported units | 242,386 | 242,386 | PASS |

Floating-point display differences were below 0.01 and came from numeric representation only.

## Grain, join, and denominator validation

- Amazon order counts use `COUNT(DISTINCT order_id)`; line counts are separate columns.
- International sales have no order ID and remain a separate line-grain source.
- Product snapshot `sku` uniqueness was checked before the Amazon-to-product left join.
- Stock `sku_code` is non-unique and was not used as a one-row-per-SKU product master.
- `NULLIF` protects order-value and percentage denominators from zero.
- Cancelled and returned records are represented as labelled status proxies; they are not silently netted into a true net-sales calculation.
- Month-over-month calculations partition by the single monthly series and use the previous month via `LAG`.

## Assumptions and limitations

- `amount` and `gross_amt` are reported monetary fields, not validated net sales or profit.
- Amazon and international values are not combined because currency and source scope differ.
- The product join is a candidate SKU enrichment; unmatched SKUs remain unmatched.
- Warehouse and expense tables have no confirmed sales key and are not allocated to orders.
- True return rate, refunds, profit, margin, customer metrics, inventory turnover, delivery time, and SLA metrics remain unsupported by Phase 1 definitions.
- The database is a local derived artifact and is reproducible by running `scripts/run_sql_layer.py` from the repository root.

## Final status

**PASS WITH WARNINGS.** The SQL analytical layer is executable, reconciled, and appropriately scoped for supported sales, product, and operational analyses. Remaining warnings concern source-level currency differences, incomplete SKU matches, non-unique stock keys, and status proxies that require business-approved definitions before executive KPI reporting.
