# Phase 5 Validation: Product Analytics

## Decision

**PASS WITH WARNINGS**

The product analytics notebook executed successfully from top to bottom in a fresh Python process. Amazon SKU/category/variant analysis, Pareto and ABC calculations, descriptive status concentration, and separate stock-snapshot indicators were validated. Cross-source product enrichment remains unsupported because no Amazon SKU matched the product-price snapshots.

## Files inspected and changed

Inspected:

- `CODEX_PROJECT_RULES.md` / `PROJECT_RULES.md`.
- Phase 0 through Phase 4 validation reports.
- `docs/data_dictionary.md`, `docs/business_scope.md`, `docs/kpi_definition.md`.
- `sql/03_product_analysis.sql` and Phase 3 DuckDB outputs.
- Amazon sales, March/May product snapshots, and stock snapshot.

Created:

- `notebooks/04_product_analytics.ipynb`
- `scripts/build_product_analytics_notebook.py`
- `reports/product_findings.md`
- `reports/validation_reports/phase_5_validation.md`
- `tests/test_phase_5_product.py`

No file under `data/cleaned/` was modified.

## Tests performed and results

- Fresh sequential replay of all 20 notebook cells: **PASS**.
- Required Amazon fields and date coverage: **PASS**.
- May and March product snapshot SKU uniqueness: **PASS**, 1,330 unique SKUs in each.
- Amazon SKU mapping: **PASS WITH WARNING**, 0 of 7,195 Amazon SKUs matched the May snapshot and 0 sales rows matched.
- Amazon SKU-to-category/style/size consistency: **PASS**, no Amazon SKU mapped to multiple values in those dimensions.
- Product snapshot category/style consistency: **PASS**, no snapshot SKU mapped to multiple categories or styles.
- Shared non-null MRP fields across March/May snapshots: **PASS**, no conflicting values were found in the compared fields.
- Stock key validation: **PASS WITH WARNING**, five duplicate non-null `sku_code` keys; stock is not a one-row-per-SKU master.
- Product totals reconciled to Amazon reported amount and units through direct group-bys: **PASS**.
- Pareto cumulative percentages ended at 100% and were monotonic: **PASS**.
- ABC thresholds were explicitly applied: A `<=80%`, B `>80% and <=95%`, C `>95%`: **PASS**.
- Low-volume review uses the 91-day observed window and does not label products slow-moving: **PASS**.

## Reconciliation results

| Check | Result |
|---|---:|
| Amazon reported amount | `78,590,043.30` |
| Sum of category reported amount | `78,590,043.30` |
| Sum of SKU reported amount | `78,590,043.30` |
| Amazon reported units | `116,646` |
| Sum of category reported units | `116,646` |
| Sum of SKU reported units | `116,646` |
| Category Pareto endpoint | `100%` |
| SKU Pareto endpoint | `100%` |

## Assumptions and limitations

- Reported amount and units are calculated from Amazon line rows and may include cancelled or returned records because no approved order-level status precedence rule exists.
- ABC is based on reported amount within the observed Amazon window; it is not a profit, margin, or inventory-service classification.
- The Amazon sales window is `2022-03-31` to `2022-06-29`; low-volume products are not called slow-moving.
- Product-price snapshots are separate reference populations; no Amazon SKU matched them after exact comparison.
- The stock report has no date and non-unique `sku_code`; its zero-stock rows are snapshot indicators, not a time-based stockout rate.
- Amazon has no colour field, so colour analysis is limited to the separate stock snapshot.
- The shared MRP fields had no conflicting non-null values between March and May for common snapshot SKUs, but the snapshots' business definitions and timing are not confirmed.

## Unresolved issues

- Create a governed cross-source SKU crosswalk.
- Approve an order-level status precedence rule.
- Add product lifecycle dates, costs/margins, dated inventory snapshots, and demand history before rationalisation decisions.

## Final status

**PASS WITH WARNINGS**: suitable for controlled within-source product portfolio analysis. Do not use the outputs to claim profitability, slow movement, discontinuation, true return/cancellation rates, or sales-linked inventory availability.
