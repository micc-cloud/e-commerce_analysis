# Phase 4 Validation: Sales Analytics

## Decision

**PASS WITH WARNINGS**

Phase 4 now reports both the complete `reported_source` scope and an explicit `delivered_status_proxy` sensitivity scope. The latter is not labelled completed sales because no business-approved status rule exists.

## Files inspected and changed

- Inspected Phase 0–3 reports, KPI definitions, cleaned sales files, SQL layer, and existing Phase 4 code.
- Changed `sql/02_sales_analysis.sql`, `scripts/build_sales_analytics_notebook.py`, `notebooks/03_sales_analytics.ipynb`, `src/status_scope.py`, `tests/test_phase_3_sql.py`, `tests/test_phase_4_sales.py`, and this report.
- Changed `reports/sales_findings.md`.
- Cleaned and raw source files were not modified.

## Validation performed

- Rebuilt and replayed all 32 notebook cells sequentially in a fresh Python process: **PASS**.
- Reported-source SQL reconciliation: amount `78,590,043.30`, orders `120,378`, units `116,646`: **PASS**.
- Delivered-status-proxy reconciliation: amount `18,650,815.00`, orders `26,566`, units `28,886`: **PASS**.
- Amount coverage was reported by status, month, category, and scope: **PASS**.
- Distinct-order logic and line counts remain separate: **PASS**.
- Partial-month MoM suppression remains active: **PASS**.
- Net sales and formal AOV remain excluded: **PASS**.

## Important limitations

- `delivered_status_proxy` is the exact `Shipped - Delivered to Buyer` status, not a confirmed completed-sales definition.
- Reported-source figures include cancelled and return-related rows by design for traceability.
- Amount coverage is approximately 94% overall and materially lower for cancelled rows.
- International data remains separate because currency and order IDs are unavailable.
- The Amazon period is short and has partial boundary months.

## Final status

**PASS WITH WARNINGS**: suitable for scoped descriptive sales analysis. Business approval is still required before selecting an executive completed-sales rule.
