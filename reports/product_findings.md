# Phase 5 Product Analytics Findings

## Product scope and mapping

**Observation**  Amazon product performance can be analysed within the sales source, but product-price and stock enrichment cannot be safely joined to Amazon sales.

**Evidence**  Amazon contains 7,195 distinct SKUs. The May and March product snapshots each contain 1,330 unique SKUs, but no Amazon SKU matches either snapshot. The stock report has 9,170 non-null `sku_code` values and five duplicate SKU keys.

**Interpretation**  The source systems use different SKU formats or populations. Product-price and stock results must remain separate source views.

**Business implication**  Establish a governed SKU crosswalk before using price or inventory data to explain sales performance.

**Limitation**  No cross-source product enrichment, inventory coverage, or price linkage is claimed.

## Category performance

**Observation**  Reported Amazon amount is concentrated in a small number of categories.

**Evidence**  Set contributes `49.9%` and kurta `27.1%` of reported amount. Together they contribute `76.98%`; the top three categories contribute `91.25%`.

**Interpretation**  The observed sales portfolio is category-concentrated within the Amazon window.

**Business implication**  Prioritise availability, catalogue quality, and status review for Set and kurta before making assortment decisions.

**Limitation**  Reported amount is not profit, and cancelled/returned rows were not removed because no approved order-level status precedence rule exists.

## SKU, style, and size performance

**Observation**  The highest reported-amount SKUs are J0230-SKD-M, JNE3797-KR-L, J0230-SKD-S, JNE3797-KR-M, and JNE3797-KR-S. The highest style is JNE3797, while M, L, and XL are the leading sizes by reported amount.

**Evidence**  SKU, style, and size tables use direct Amazon group-bys with reported amount, units, line count, and distinct orders.

**Interpretation**  The results describe commercial contribution and variant mix within the 91-day observed window.

**Business implication**  Use the leading variants for availability and catalogue checks, then test whether the pattern persists over a longer history.

**Limitation**  Amazon has no colour field, and no product lifecycle or launch-date field is available.

## Pareto and ABC classification

**Observation**  ABC classification identifies 1,973 A-class SKUs, 2,143 B-class SKUs, and 3,079 C-class SKUs using explicit reported-amount thresholds.

**Evidence**  Class A is cumulative contribution through 80%, B is greater than 80% through 95%, and C is greater than 95%. Cumulative contribution ends at 100% for both SKU and category tables.

**Interpretation**  ABC is a reported-sales concentration tool, not a profitability or inventory-service classification.

**Business implication**  Begin portfolio review with A-class availability and data quality, and investigate C-class products for lifecycle, stock, strategic-role, and demand evidence.

**Limitation**  No cost, margin, demand forecast, lifecycle, or service-level data exists to support automatic rationalisation.

## Low-volume and rationalisation candidates

**Observation**  Some SKUs have zero reported amount or very low observed contribution.

**Evidence**  The notebook presents the lowest reported-amount SKUs within the same 91-day window and retains their units and line counts.

**Interpretation**  These are low-volume review candidates, not slow-moving products.

**Business implication**  Check launch date, stock availability, listing quality, returns, margin, and strategic role before any product removal decision.

**Limitation**  The dataset does not provide a defensible lifecycle or longer demand window, so no product is labelled slow-moving, unprofitable, or discontinued.

## Status and stock indicators

**Observation**  Cancellation and return-related records can be concentrated by category, while the stock snapshot contains zero-stock rows by category.

**Evidence**  Status concentration is shown using descriptive line counts, units, and reported amounts. The stock snapshot reports `242,386` stock units and zero-stock rows by stock category, including `205` for KURTA and `114` for KURTA SET.

**Interpretation**  These are investigation signals, not cancellation/return rates or stockout rates.

**Business implication**  Review status rules and create a dated, governed stock-to-sales key before making availability or rationalisation decisions.

**Limitation**  Stock has no snapshot date and `sku_code` is non-unique; mixed line statuses require order-level precedence.

## Explicit exclusions

- No product is labelled unprofitable, slow-moving, discontinued, or a true stockout.
- No Amazon sales-to-price or sales-to-stock join is used.
- No colour-sales analysis is performed because Amazon has no colour field.
