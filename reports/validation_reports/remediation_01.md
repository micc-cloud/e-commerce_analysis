# Remediation 1: Data Foundation and KPI Governance

## Scope and rules-file note

The requested `CPROJECT_RULES.md` file is not present in the repository or the
provided project-rules location. The available rules file is
`/Users/user/Desktop/Jobs/e_commerce_project/PROJECT_RULES.md`; it was used for
this remediation. No Phase 2–9 analytical notebooks or calculations were
changed.

## Issue classification before remediation

| Issue | Classification | Evidence | Action | Remaining limitation | Status |
|---|---|---|---|---|---|
| Amazon `amount` missing on 7,792 rows | `DEFINITION_REQUIRED` plus `SOURCE_DATA_LIMITATION` | 121,177 of 128,969 rows have a reported amount; missingness varies by status | Preserve missing values and label coverage; do not impute or drop | Source does not explain whether missing means zero, cancelled, unavailable, or another state | WARNING |
| Zero Amazon quantity on 12,804 rows | `DEFINITION_REQUIRED` | Zero quantity is concentrated in records whose business outcome is not independently documented | Preserve rows and report as a data-quality segment | Cannot determine whether zero means cancellation, a source state, or an error | WARNING |
| Zero Amazon amount on 2,343 rows | `DEFINITION_REQUIRED` | Zero amount exists without a validated accounting interpretation | Preserve rows and exclude only from ratio denominators where the formula requires a positive amount | Cannot infer whether zero represents free/zero-value activity or missing revenue | WARNING |
| Date parsing and month-first date convention | `FIXABLE` | Raw Amazon and international dates use month-day-year strings; international `months` validates month/year | Make month-first parsing explicit and retain the international month-consistency check | Amazon has no independent month field for cross-checking | PASS |
| Duplicate stock `sku_code` values | `DEFINITION_REQUIRED` | Stock table has 68 duplicate `sku_code` rows and 48 missing keys; grain includes size and colour | Do not deduplicate; document the grain as SKU/size/colour snapshot | No snapshot date and no governed product key; SKU-level stock totals require an approved aggregation | WARNING |
| Amazon candidate line-key duplicates | `DEFINITION_REQUIRED` | `order_id+sku+size` has two duplicate rows while `order_id` is intentionally repeated at line grain | Keep rows and flag the candidate key as non-unique | No line ID exists to establish whether duplicates are duplicate extracts or separate lines | WARNING |
| Inconsistent SKU/category/style/size mappings | `SOURCE_DATA_LIMITATION` | Exact Amazon-to-product-snapshot SKU match is zero; taxonomies are source-specific | Use source-local grouping and report unmatched join coverage | No reliable cross-source product crosswalk exists | BLOCKED for cross-source enrichment |
| International currency missing | `SOURCE_DATA_LIMITATION` | International file has no currency field or FX rate | Keep international monetary results separate | Cross-source totals and price comparisons are invalid | BLOCKED |
| International order IDs missing | `SOURCE_DATA_LIMITATION` | International table is line grain without an order identifier | Permit line and piece analysis only | International order count, AOV, and order-level rates are unsupported | BLOCKED |
| Warehouse table grain | `SOURCE_DATA_LIMITATION` | Four cost-head reference rows; no transaction key, date, unit basis, or currency | Keep as reference-rate table; never join directly to sales lines | Cannot allocate fulfilment cost to orders, SKUs, or periods | BLOCKED for cost allocation |
| Expense table grain | `SOURCE_DATA_LIMITATION` | Twenty-one mixed detail/summary report rows; no sales key, period, or currency | Separate detail and summary rows; never aggregate them together | Cannot allocate expenses to sales or calculate profit | BLOCKED for profitability |
| Phase 8 filename references | `FIXABLE` | Phase 8 report used logical names that do not exist in `data/cleaned/` | Correct report references to actual filenames | None after documentation correction | PASS |

## Phase 0 remediation actions

- Raw files remain unchanged.
- Cleaned files are not imputed or automatically filtered for missing
  `amount`, zero quantity, or zero amount.
- Month-first parsing is explicit in the cleaning code. International dates are
  retained only when their parsed month/year agrees with `months`; excluded
  source rows remain available in `data/raw/`.
- Stock rows are retained at their observed SKU/size/colour snapshot grain;
  duplicate `sku_code` values are not silently collapsed.
- Candidate keys and join coverage remain diagnostics, not asserted foreign
  keys.
- Phase 8 documentation now uses the repository's actual cleaned filenames.

## Phase 1 KPI governance

### Supported metrics

- Amazon distinct order count by date and declared source scope, using
  `COUNT(DISTINCT order_id)`.
- Amazon and international line counts and gross units/pieces, kept separate.
- Amazon reported gross amount and international reported gross amount,
  separately, with amount coverage and currency limitations disclosed.
- Source-local category, SKU, size, style, geography, fulfilment, and B2B
  distributions.
- Stock snapshot row counts and reported stock totals, without turnover or
  stockout-over-time claims.
- Warehouse provider reference-rate comparisons by cost head.

### Proxy metrics

- `delivered_status_proxy`: exact Amazon status
  `Shipped - Delivered to Buyer`; it is not completed sales.
- Cancellation and return status proxies: source-status composition using
  distinct Amazon orders; they are not official cancellation or return rates.
- Reported amount per unit: `amount / qty` only where amount is present and
  quantity is positive; it is not a validated realised selling price.
- Reported-sales ABC/Pareto: concentration of a declared sales scope, not
  profitability, demand, or inventory classification.
- Stock zero-row count: a snapshot observation, not a stockout rate.

### Unsupported metrics

- Official net sales after discounts, cancellations, returns, refunds, taxes,
  or shipping adjustments.
- Profit, COGS, gross margin, contribution margin, ROI, or profitability by
  SKU/category/platform.
- True return rate, refund rate, delivery time, on-time delivery, or SLA rate.
- Customer count, repeat rate, retention, lifetime value, or cohort analysis.
- Inventory turnover, days of inventory, stockout-over-time, or demand
  forecasting from the undated stock snapshot.
- Cross-source sales totals, cross-source price indexes, or international
  order-level KPIs.

## Revalidation decision

**PASS WITH WARNINGS.** Phase 0–1 are revalidated for controlled descriptive
analysis. Cross-source enrichment, official operational rates, profitability,
and predictive modelling remain blocked by definitions or source-data gaps.
