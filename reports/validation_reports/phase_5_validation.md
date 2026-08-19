# Phase 5 Validation: Product Analytics

## Final status

**PASS WITH WARNINGS**

Product analytics uses source-local Amazon identifiers and supported reported
gross measures. Cross-source product, price, and stock enrichment remains
excluded because the SKU mapping is not reliable.

## Files inspected and changed

Inspected:

- `PROJECT_RULES.md`
- `docs/kpi_definition.md`
- `docs/business_scope.md`
- `reports/validation_reports/remediation_01.md`
- `reports/validation_reports/remediation_02.md`
- `reports/validation_reports/phase_4_validation.md`
- `notebooks/04_product_analytics.ipynb`
- Amazon, product snapshot, and stock cleaned files

Changed:

- `notebooks/04_product_analytics.ipynb`
- `reports/product_findings.md`
- `reports/validation_reports/phase_5_validation.md`
- `tests/test_phase_5_revalidation.py`

No raw or cleaned dataset was modified. Upstream Phase 0–4 analytical files
were not rebuilt.

## Supported and proxy metrics

Supported source-local metrics:

- SKU reported gross amount, gross units, and distinct Amazon orders.
- Category, style, size, B2B/category, and source-local status composition.
- Sales concentration and Pareto contribution.
- High- and low-observed-volume SKU review.

Proxy metrics:

- Delivered-status-proxy product contribution using exact status
  `Shipped - Delivered to Buyer`.
- Cancellation and return-related status composition from source labels.
- **Reported Gross Amount ABC** using thresholds A `<=80%`, B `>80%` to `<=95%`,
  and C `>95%`.

## Mapping validation

| Mapping/check | Result | Status |
|---|---:|---|
| Amazon distinct SKUs in delivered proxy | 4,430 | PASS |
| May product snapshot unique SKUs | 1,330 | PASS |
| March product snapshot unique SKUs | 1,330 | PASS |
| Amazon-to-May exact SKU match | 0 rows / 0 distinct SKUs | WARNING / blocked enrichment |
| Amazon SKU category/style/size conflicts | 0 | PASS |
| May/March snapshot SKU duplicates | 0 | PASS |
| Stock duplicate non-null SKU keys | 5 keys | WARNING |

No cross-source sales-to-product, sales-to-stock, or sales-to-MRP join was used.

## Reconciliation and independent reproduction

| Result | Product analysis | Independent source / Phase 4 | Status |
|---|---:|---:|---|
| Delivered proxy reported gross amount | 18,650,815.00 | 18,650,815.00 | PASS |
| Delivered proxy gross units | 28,886 | 28,886 | PASS |
| Delivered proxy distinct orders | 26,566 | 26,566 | PASS |
| Top-five category amount share | 99.18% | Direct Pandas group-by | PASS |
| Top-five SKU amount share | 5.99% | Direct Pandas group-by | PASS |
| SKU ABC cumulative endpoint | 100% | Direct cumulative calculation | PASS |
| Category ABC cumulative endpoint | 100% | Direct cumulative calculation | PASS |

Additional checks passed:

- Reported gross amount and units reconcile by SKU and category.
- Distinct-order measures use `nunique(order_id)` and remain separate from line
  counts.
- Amount coverage is shown in product tables; delivered proxy coverage is
  99.97% with 8 missing amounts.
- Cancellation and return tables use source-status labels and retain coverage
  fields; they are not presented as rates.
- B2B/B2C category mix is source-local and does not use an unsafe join.
- Pareto cumulative percentages are monotonic and terminate at 100%.
- No product is labelled slow-moving, unprofitable, discontinued, excess, or a
  true stockout.
- The notebook executed top-to-bottom from a clean `python3` kernel.

## Excluded analyses

- Sales-to-product-price or MRP enrichment.
- Sales-to-stock joins, stockouts, inventory turnover, and demand measures.
- Profitability, margin, cost, lifecycle, and discontinuation conclusions.
- Customer-level product analysis.
- International monetary product comparisons.

## Remaining limitations

- `amount` remains reported gross amount, not net sales or profit.
- The delivered status is an analytical proxy without approved order precedence.
- Exact cross-source SKU match is zero, preventing enrichment.
- Stock is an undated, non-unique variant snapshot.
- The Amazon observed window is short and cannot support lifecycle or
  slow-moving claims.

## Decision

**PASS WITH WARNINGS.** Phase 5 is suitable for controlled within-source
product contribution and concentration analysis. Stop here and wait before
starting Phase 6.
