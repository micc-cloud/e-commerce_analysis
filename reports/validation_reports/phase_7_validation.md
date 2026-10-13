# Phase 7 Validation: Operations Analytics

## Final status

**PASS WITH WARNINGS**

Phase 7 uses Amazon status fields as descriptive analytical proxies only. The
notebook distinguishes line grain from distinct-order grain, explicitly
investigates mixed-status orders, uses order-plus-dimension tables to avoid
many-to-many duplication, and excludes unsupported timing and rate claims.

## Files inspected and changed

Inspected:

- `PROJECT_RULES.md`
- `docs/kpi_definition.md`
- `docs/business_scope.md`
- Phase 0–6 validation reports
- `src/status_scope.py`
- Cleaned Amazon operations fields and warehouse reference data

Changed:

- `notebooks/06_operations_analytics.ipynb`
- `reports/operations_findings.md`
- `reports/validation_reports/phase_7_validation.md`
- `tests/test_phase_7_operations.py`

No raw or cleaned source dataset was modified. No Phase 8 file was changed.

## Supported and proxy metrics

- Amazon line-level status composition.
- Distinct-order status presence proxies using `nunique(order_id)`.
- Status composition by observed month, category, SKU, ship state, and B2B
  flag, with group denominators and sample flags.
- Fulfilment, provider, and courier source-label mix only.

All cancellation, return, shipped, and delivered measures are labelled status
proxies, not validated operational rates.

## Mixed-status validation

- The order table retains the complete tuple of statuses per `order_id`.
- `status_count > 1` is labelled `MIXED_STATUS_REQUIRES_RULE`.
- Current extract mixed-status orders: **0**.
- No first-status assignment or precedence rule is used.
- A future Shipped + Cancelled order would remain unresolved in the status
  label and be reported in the mixed-status detail table.

## Reconciliation and independent checks

| Check | Result | Status |
|---|---:|---|
| Amazon line records | 128,969 | PASS |
| Distinct Amazon orders | 120,378 | PASS |
| Cancelled status-proxy orders | 17,185 | PASS |
| Return-related status-proxy orders | 1,981 | PASS |
| Shipped status-proxy orders | 102,339 | PASS |
| Delivered status-proxy orders | 26,566 | PASS |
| Mixed-status orders | 0 | PASS WITH WARNING |

Additional checks passed:

- Line-level status counts sum to all Amazon rows.
- Order-level status labels sum to all distinct Amazon orders.
- Proxy denominators are explicit and rates are bounded between 0 and 1.
- Monthly order totals reconcile to the distinct-order denominator.
- Category, SKU, geography, and B2B/B2C tables are built at
  `order_id + dimension` grain; overlapping group denominators are not summed
  as a source-wide total.
- Small groups receive `small_sample_review_only` flags.
- Fulfilment is not ranked when only one meaningful category exists.
- Warehouse data is not joined because it lacks a transaction-level key.
- No timestamp-based metric or unsupported operational-rate terminology was
  introduced.
- Notebook executed top-to-bottom from a clean `python3` kernel.

## Excluded analyses

- Official cancellation, return, fulfilment, delivery, or SLA rates.
- Delivery/processing duration, on-time performance, and courier speed.
- Invented order-status precedence or forced mixed-order assignment.
- Warehouse/expense attribution, causal operational explanations, and
  predictive use of status/courier fields.

## Remaining limitations

- Status fields are source labels without event history or transition times.
- The extract has no mixed-status orders, so precedence governance remains
  unresolved rather than validated.
- `amount` and cost fields are not needed for this phase and are not used to
  infer operational impact.
- Group comparisons may reflect product mix and sample size.
- The fulfilment dimension has no meaningful comparison group.

## Decision

**PASS WITH WARNINGS.** Suitable for descriptive status and operational data
governance review. Obtain event-level status history and an approved
precedence rule before official operational KPIs. Stop before Phase 8.
