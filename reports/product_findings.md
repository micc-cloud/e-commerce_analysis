# Phase 5 Product Analytics Findings

## Scope and mapping

**Observation**  Product contribution and ABC use the explicit `delivered_status_proxy` scope; reported-source status totals remain separate.

**Evidence**  The proxy uses exact status `Shipped - Delivered to Buyer` and contains `28,769` lines. Amazon has `4,430` distinct SKUs in this scope, while the May and March product snapshots each have `1,330` unique SKUs. Exact Amazon-to-snapshot matches remain `0`.

**Interpretation**  Product results are within-source Amazon results and are not enriched with price or stock snapshots.

**Business implication**  Create a governed SKU crosswalk before using price or inventory data to explain sales performance.

**Limitation**  The delivered status is a proxy, not an approved completed-order definition.

## Category and SKU performance

**Observation**  Within the delivered-status proxy, Set contributes `47.2%`, kurta `25.3%`, and Western Dress `20.7%` of reported amount.

**Evidence**  Category and SKU totals reconcile directly to the delivered-status-proxy sales scope. The leading proxy SKUs are JNE3797-KR-L, JNE3797-KR-M, SET183-KR-DH-M, JNE3797-KR-S, and JNE3797-KR-XL.

**Interpretation**  The results describe status-scoped commercial contribution, not profitability.

**Business implication**  Prioritise status, catalogue, and availability review for high-contribution variants.

**Limitation**  Amount is not net sales, and no cost or margin data exists.

## Pareto and reported-sales ABC

**Observation**  ABC is explicitly a reported-sales classification, not inventory or profitability ABC.

**Evidence**  Class A is cumulative contribution through 80%, B is greater than 80% through 95%, and C is greater than 95%. The delivered proxy produces `1,433` A-class SKUs, `1,453` B-class SKUs, and `1,544` C-class SKUs; cumulative shares end at 100%.

**Interpretation**  The classification identifies status-scoped sales concentration only.

**Business implication**  Use A products for availability and data-quality review; treat C products as investigation candidates.

**Limitation**  No cost, lifecycle, demand forecast, dated inventory, or service-level fields support automatic rationalisation.

## Low-volume and status concentration

**Observation**  Low-amount SKUs and cancellation/return concentrations are displayed as review signals.

**Evidence**  Low-volume review is limited to the observed March 31 to June 26 proxy window. Cancelled and return-related records are calculated from the full reported source for status investigation.

**Interpretation**  Low volume is not evidence of slow movement, and status concentration is not a true rate.

**Business implication**  Check lifecycle, availability, listing quality, returns, margin, and strategic role before any rationalisation decision.

**Limitation**  No product is labelled slow-moving, unprofitable, discontinued, or a true stockout.

## Stock and mapping limitations

- Stock is a separate undated snapshot with five duplicate non-null `sku_code` keys.
- No sales-to-stock join or stockout rate is calculated.
- Amazon has no colour field; colour analysis is limited to the separate stock snapshot.
- Shared non-null MRP fields between March and May had no conflicting values, but their business definitions are unconfirmed.
