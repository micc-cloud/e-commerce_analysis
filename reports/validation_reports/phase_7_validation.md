# Phase 7 Validation: Operations Analytics

## Decision

**PASS WITH WARNINGS**

The operations notebook completed successfully using distinct Amazon order IDs for denominators. It distinguishes line-level status from order-level status, checks mixed-status orders, reports explicit status proxies, and excludes unsupported delivery-speed and warehouse-allocation measures.

## Files inspected and changed

- Inspected `PROJECT_RULES.md`, `docs/kpi_definition.md`, Phase 0–6 validation reports, `sql/04_operations_analysis.sql`, cleaned Amazon operations fields, and the status-scope helper.
- Created `notebooks/06_operations_analytics.ipynb`, `scripts/build_operations_analytics_notebook.py`, `reports/operations_findings.md`, `reports/validation_reports/phase_7_validation.md`, and `tests/test_phase_7_operations.py`.
- No raw or cleaned source file was modified.

## Validation performed

- Rebuilt and replayed all 16 notebook cells sequentially in a fresh Python process: **PASS**.
- Raw line status totals reconciled to `128,969` lines: **PASS**.
- Order-level status totals reconciled to `120,378` distinct orders: **PASS**.
- Mixed-status orders: `0`: **PASS**, while retaining the check for future data.
- Mixed fulfilment and channel orders: `0`: **PASS**.
- Rate denominator explicitly confirmed as `120,378` distinct Amazon orders: **PASS**.
- Status proxy rates are bounded between 0 and 1: **PASS**.
- Fulfilment and platform order totals reconcile to the order denominator: **PASS**.
- Platform/category groups include sample-size flags; Non-Amazon is flagged small-sample review only: **PASS**.
- Warehouse table was inspected and not joined because it has no reliable order-level key: **PASS**.

## Reconciliation

| Measure | Result |
|---|---:|
| Amazon line records | `128,969` |
| Distinct Amazon orders | `120,378` |
| Cancelled orders | `17,185` |
| Return-status-proxy orders | `1,981` |
| Shipped-status-proxy orders | `102,339` |
| Delivered-status-proxy orders | `26,566` |
| Cancellation status proxy rate | `14.28%` |
| Return status proxy rate | `1.65%` |
| Shipped status proxy rate | `85.01%` |
| Delivered status proxy rate | `22.07%` |

## Assumptions and limitations

- Cancellation, return, shipped, and delivered measures are source-status proxies, not approved business rates.
- Every rate denominator is all distinct Amazon order IDs unless a group table explicitly states its group-level distinct-order denominator.
- A `1,000`-order threshold is an analytical sample flag, not a statistical significance test.
- A `100`-order threshold is used only to produce operational review candidates.
- No delivery duration or courier-speed ranking is possible without valid event timestamps.
- Warehouse reference rates cannot be linked to orders or fulfilment methods.

## Final status

**PASS WITH WARNINGS**: suitable for descriptive operational monitoring and status-definition review. Do not present proxy rates as true cancellation, return, fulfilment, delivery, or SLA metrics.
