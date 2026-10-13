# Phase 5 Product Analytics Findings

## Scope and mapping

**Observation** Product contribution and ABC use Amazon's exact
`delivered_status_proxy` scope. Reported-source totals remain separate.

**Evidence** The proxy contains 28,769 lines, 26,566 distinct orders, 28,886
units, and `18,650,815.00` reported gross amount. It contains 4,430 distinct
Amazon SKUs with 99.97% amount coverage. May and March product snapshots each
contain 1,330 unique SKUs; exact Amazon-to-snapshot matches are zero.

**Interpretation** Product metrics are source-local Amazon results. No price,
MRP, or stock enrichment is assumed.

**Business implication** Obtain a governed SKU crosswalk before using product
master or stock data to explain sales performance.

**Limitation** The delivered status is an analytical proxy, not an approved
completed-order rule; source systems may use different SKU definitions.

## Category, SKU, and variant contribution

**Observation** Set, kurta, and Western Dress lead delivered-status-proxy
reported gross amount. The leading SKUs are `JNE3797-KR-L`, `JNE3797-KR-M`,
`SET183-KR-DH-M`, `JNE3797-KR-S`, and `JNE3797-KR-XL`.

**Evidence** Category reported amounts are `8,800,562`, `4,715,208`, and
`3,868,616`. The leading five SKU amounts are `295,061`, `260,255`, `197,316`,
`188,905`, and `174,942`. SKU, category, style, and size calculations use
source-local mappings with distinct order counts and amount coverage.

**Interpretation** These results describe reported commercial contribution in a
status-proxy scope, not profitability or demand.

**Business implication** Review high-contribution variants for availability,
catalogue quality, and status composition.

**Limitation** `amount` is reported gross amount, not net sales; no cost,
lifecycle, dated inventory, or demand history exists.

## Reported Gross Amount ABC and Pareto

**Observation** ABC classifications can be calculated from descending
delivered-status-proxy reported gross amount.

**Evidence** The declared thresholds are A through cumulative share `<=80%`, B
above 80% through `<=95%`, and C above 95%. The SKU classification contains
1,433 A SKUs, 1,453 B SKUs, and 1,544 C SKUs. Cumulative contribution is
monotonic and ends at 100%.

**Interpretation** This is **Reported Gross Amount ABC**, not inventory,
profit, demand, or lifecycle ABC.

**Business implication** Use A-class products for first-pass availability and
data-quality review; treat C-class products as review candidates only.

**Limitation** No automatic rationalisation, discontinuation, or slow-moving
decision is justified by this classification.

## Sales concentration and B2B/B2C mix

**Observation** The top five categories account for approximately 99.18% of
delivered-status-proxy reported gross amount, while the top five SKUs account
for approximately 5.99% of the SKU-attributed scope.

**Evidence** Shares use the same within-scope reported gross amount denominator
and sum to 100% across the full category and SKU tables. B2B/B2C category mix is
also calculated within the Amazon source.

**Interpretation** Category concentration is high, while SKU concentration is
more dispersed. This is a mix signal, not a causal or economic conclusion.

**Business implication** Pair concentration review with status, availability,
and catalogue checks before assortment decisions.

**Limitation** No profitability, margin, inventory, customer, or demand metric
supports a stronger portfolio conclusion.

## High- and low-volume review

**Observation** High- and low-reported-amount SKUs are displayed within the
observed Amazon proxy window.

**Evidence** The review tables include reported gross amount, gross units,
line count, distinct orders, and amount coverage. The window is bounded by the
available extract rather than a lifecycle period.

**Interpretation** Low observed volume is not evidence of slow movement or poor
performance.

**Business implication** Validate launch date, availability, listing quality,
strategic role, and longer history before taking action.

**Limitation** No product is labelled slow-moving, recently introduced,
unprofitable, discontinued, or excess inventory.

## Status-proxy composition

**Observation** Cancellation and return-related labels can be concentrated by
category and SKU.

**Evidence** Cancelled and return-related rows are analysed from the complete
reported Amazon source. The notebook reports line counts, units, reported gross
amount, and amount coverage by category and SKU.

**Interpretation** These are status-composition review signals, not rates.

**Business implication** Prioritise status-definition and data-quality review
for categories or SKUs with high proxy counts.

**Limitation** No approved order-status precedence, returned quantity, refund
value, or event timestamp exists.

## Stock and cross-source exclusions

- Stock remains a separate undated SKU/size/colour snapshot with duplicate and
  missing `sku_code` values.
- No Amazon sales-to-stock, sales-to-MRP, or sales-to-price join is performed.
- Colour analysis is limited to the stock snapshot because Amazon sales has no
  colour field.
- Shared March/May reference-price fields are not treated as realised selling
  price or cost.
- International monetary product analysis is not combined with Amazon because
  currency and order identifiers are absent.
