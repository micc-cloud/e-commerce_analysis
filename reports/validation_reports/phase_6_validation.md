# Phase 6 Validation: Pricing Analytics

## Final status

**PASS WITH WARNINGS**

Phase 6 uses only source-local Amazon pricing proxies and separate catalogue
reference-price diagnostics. No discount, realised price, elasticity, causal,
profit, or margin analysis was introduced.

## Files inspected and changed

Inspected:

- `PROJECT_RULES.md`
- `docs/kpi_definition.md`
- `docs/business_scope.md`
- Phase 0–5 remediation and validation reports
- Cleaned Amazon sales and March/May product snapshots
- `src/status_scope.py`

Changed:

- `notebooks/05_pricing_analytics.ipynb`
- `reports/pricing_findings.md`
- `reports/validation_reports/phase_6_validation.md`
- `tests/test_phase_6_pricing.py`

No raw or cleaned source dataset was modified. No cross-source sales-to-MRP
join was performed.

## Supported and proxy metrics

- Reported unit-price proxy: `amount / qty` only where amount is present,
  currency is INR, and `qty > 0`.
- Proxy distribution and variation by source-local SKU, category, month, B2B
  flag, and shipping state.
- Descriptive price bands with reported gross amount and gross units.
- Catalogue reference-price variation within March/May snapshot rows only.

The reported unit-price proxy is not a validated realised selling price.

## Validation and independent reproduction

| Check | Result | Status |
|---|---:|---|
| Valid delivered-proxy pricing lines | 28,761 | PASS |
| Valid delivered-proxy units | 28,886 | PASS |
| Median reported unit-price proxy | 629 INR | PASS |
| Mean reported unit-price proxy | 645.82 INR | PASS |
| Delivered-proxy missing amount rows | 8 | WARNING |
| Delivered-proxy non-positive quantity rows | 8 | WARNING |
| Zero-price valid rows | 716 | WARNING |
| Negative valid unit-price rows | 0 | PASS |
| Exact Amazon-to-May SKU matches | 0 | WARNING / blocked enrichment |
| May rows with >=2 reference prices | 1,293 | PASS |
| May rows with non-zero reference range | 266 | PASS |
| Largest May reference-price range | 800 INR | PASS |

Independent checks passed:

- Manual `amount / qty` calculation reproduced for a ten-row sample.
- Zero and non-positive quantity rows were excluded from proxy denominators but
  retained in the source data.
- Price-band counts reconcile to all valid proxy rows: 10,053, 15,831, 2,870,
  and 7 lines across the four bands.
- Price-band boundaries are unique, mutually exclusive, and exhaustive.
- SKU and category summary tables use the same valid-price population and
  retain sample-size columns.
- Monthly, B2B/B2C, geographic, and fulfilment comparisons report line counts;
  fulfilment has one observed value and is not ranked.
- Extreme values were flagged using IQR and retained; no outlier was removed.
- Amount coverage is disclosed; the full Amazon source has 7,792 missing
  amounts.
- No MRP, discount, profit, margin, elasticity, or cross-currency calculation
  was introduced.
- The notebook executed top-to-bottom from a clean `python3` kernel.

## Excluded pricing analyses

- Discount amount and discount percentage.
- Amazon reported unit-price proxy versus MRP, because exact SKU match is zero.
- High-discount products from `promotion_ids` alone.
- Optimal price, price elasticity, causal price-volume effects, profit, and
  margin.
- International monetary price aggregation.

## Important limitations

- `amount` is a reported field, not validated net revenue or realised price.
- `Shipped - Delivered to Buyer` is an analytical status convention, not an
  approved completed-sales definition.
- The Amazon window covers only 91 observed dates; March and June are partial
  boundary periods, so seasonality is unsupported.
- Fulfilment has only one observed category (`Merchant`), preventing comparison.
- Amazon SKU mappings to product snapshots are source-incompatible; MRP fields
  remain standalone reference data and are not costs.
- International currency is unavailable, preventing cross-source aggregation.

## Decision

**PASS WITH WARNINGS.** Phase 6 is suitable for controlled descriptive pricing
monitoring and reference-price consistency review. Stop before Phase 7.
