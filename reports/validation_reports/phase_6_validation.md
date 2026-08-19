# Phase 6 Validation: Pricing Analytics

## Decision

**PASS WITH WARNINGS**

The pricing notebook completed successfully and calculates only supported within-source price measures. Actual discounts, realised price-versus-MRP, elasticity, and profit-margin analysis remain excluded.

## Files inspected and changed

- Inspected `PROJECT_RULES.md`, `docs/data_dictionary.md`, Phase 0–5 validation reports, cleaned sales files, product snapshots, and the status-scope helper.
- Created `notebooks/05_pricing_analytics.ipynb`, `scripts/build_pricing_analytics_notebook.py`, `reports/pricing_findings.md`, `reports/validation_reports/phase_6_validation.md`, and `tests/test_phase_6_pricing.py`.
- No raw or cleaned source file was modified.

## Validation performed

- Rebuilt and replayed all 17 notebook cells sequentially in a fresh Python process: **PASS**.
- Confirmed populated Amazon currencies are INR; international currency is unavailable: **PASS WITH WARNING**.
- Calculated unit price only with populated amount and positive quantity: **PASS**.
- Zero unit-price rows: `716`; negative unit-price rows: `0`: **PASS WITH WARNING**.
- Snapshot MRP fields have no negative values or zero values: **PASS**.
- Confirmed zero exact Amazon-to-May SKU matches; discount calculations were correctly excluded: **PASS WITH WARNING**.
- Manually reconciled unit-price arithmetic for a ten-row sample: **PASS**.
- Price bands `[0,500)`, `[500,1000)`, `[1000,2000)`, `[2000,inf)` are unique, exhaustive, and mutually exclusive: **PASS**.
- IQR anomaly rows were flagged and retained; no rows were removed: **PASS**.

## Reconciliation

| Measure | Result |
|---|---:|
| Valid delivered-status-proxy pricing rows | `28,761` |
| Median reported amount per unit | `629 INR` |
| Mean reported amount per unit | `645.82 INR` |
| Amazon-to-May exact SKU matches | `0` |
| May rows with at least two platform reference prices | `1,293` |
| May rows with non-zero platform reference-price range | `266` |
| Largest May platform reference-price range | `800 INR` |

## Assumptions and limitations

- `amount / qty` is a line-level reported amount-per-unit proxy, not confirmed net realised price.
- `Shipped - Delivered to Buyer` is a status proxy, not an approved completed-sales rule.
- MRP fields are reference/listed prices and are not treated as cost.
- Discount amount, discount percentage, and realised price-versus-MRP are unsupported without a SKU crosswalk and discount fields.
- Platform reference prices are compared within the same snapshot rows, but their business definitions and currency/unit basis are not confirmed.
- No price elasticity, causal claim, or specific price recommendation is produced.

## Final status

**PASS WITH WARNINGS**: suitable for descriptive price monitoring and reference-price consistency review. Obtain a governed SKU crosswalk and validated discount/currency definitions before discount or realised-price analysis.
