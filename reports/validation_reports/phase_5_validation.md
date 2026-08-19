# Phase 5 Validation: Product Analytics

## Decision

**PASS WITH WARNINGS**

Phase 5 product contribution and reported-sales ABC now use the explicit `delivered_status_proxy` scope. Reported-source status totals remain separate, and no unsupported sales-to-price or sales-to-stock join is performed.

## Files inspected and changed

- Inspected Phase 0–4 reports, KPI definitions, product fields, stock fields, SQL product views, and cleaned source files.
- Changed `sql/03_product_analysis.sql`, `scripts/build_product_analytics_notebook.py`, `notebooks/04_product_analytics.ipynb`, `tests/test_phase_5_product.py`, and this report.
- Changed `reports/product_findings.md`.
- Cleaned and raw source files were not modified.

## Validation performed

- Rebuilt and replayed all 20 notebook cells sequentially: **PASS**.
- Delivered-status-proxy product totals reconciled to the scoped sales rows: **PASS**.
- Product snapshot SKUs are unique: **PASS**.
- Amazon SKU mappings are internally consistent for category, style, and size: **PASS**.
- Exact Amazon-to-May/March snapshot match rate remains 0%; no invalid join was introduced: **PASS WITH WARNING**.
- Shared non-null MRP fields between March and May snapshots have no conflicting values: **PASS**.
- Pareto cumulative percentages are monotonic and end at 100%: **PASS**.
- ABC thresholds are explicit: A `<=80%`, B `>80% and <=95%`, C `>95%`: **PASS**.
- Low-volume products are not labelled slow-moving: **PASS**.
- Stock remains a separate undated snapshot with five duplicate SKU keys: **PASS WITH WARNING**.

## Important limitations

- The delivered-status proxy is not an approved completed-sales rule.
- ABC is reported-sales ABC, not inventory, profitability, or demand-planning ABC.
- No product is labelled profitable, unprofitable, slow-moving, discontinued, or a true stockout.
- No Amazon sales-to-price or sales-to-stock join is possible without a governed SKU crosswalk.
- No product lifecycle, cost/margin, dated inventory, or long demand history is available.

## Final status

**PASS WITH WARNINGS**: suitable for controlled within-source product analysis. A governed SKU crosswalk and approved status definition remain required for stronger portfolio decisions.
