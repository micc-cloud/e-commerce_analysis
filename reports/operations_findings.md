# Phase 7 Operations Analytics Findings

## Order-level denominator and status distribution

**Observation**  Amazon contains `128,969` line records and `120,378` distinct orders. No order contains multiple status values in the cleaned file.

**Evidence**  The notebook reconciles line counts and distinct-order counts by raw status and builds all rates from the distinct-order table.

**Interpretation**  Order-level deduplication is currently stable, but the absence of mixed statuses is a source observation rather than a business definition.

**Business implication**  Operational reporting can use distinct order IDs for denominators while retaining line-level status distributions.

**Limitation**  Status labels are not a validated lifecycle model.

## Status proxy rates

**Observation**  Using all `120,378` distinct Amazon orders as the denominator, the cancellation status proxy is `14.28%`, return status proxy is `1.65%`, shipped status proxy is `85.01%`, and delivered status proxy is `22.07%`.

**Evidence**  Cancellation means exact `Cancelled`; return means any status containing `Return`; shipped means any status beginning `Shipped`; delivered means exact `Shipped - Delivered to Buyer`.

**Interpretation**  These measures describe source status composition, not true cancellation, return, fulfilment, or delivery rates.

**Business implication**  Use them to prioritise status-definition and operational-process review.

**Limitation**  No approved status precedence, return quantity, refund value, delivery timestamp, or SLA denominator exists.

## Fulfilment and courier mix

**Observation**  Amazon fulfilment labels show `84,002` distinct orders for Amazon fulfilment and `36,376` for Merchant fulfilment. Courier labels are also reported at line and distinct-order grain.

**Evidence**  The notebook reports `fulfilment`, `fulfilled_by`, and `courier_status` distributions without converting labels into speed or service-level measures.

**Interpretation**  These are operational mix indicators only.

**Business implication**  Use them to identify data-quality and process-review areas, especially missing courier or provider labels.

**Limitation**  No valid delivery-date or timestamp field exists, so delivery duration, on-time delivery, and courier-speed ranking are excluded.

## Platform and category differences

**Observation**  Amazon.in represents `120,254` distinct orders, while Non-Amazon represents `124`; category populations also vary substantially.

**Evidence**  Platform and category tables include distinct-order denominators and a `1,000`-order analytical sample flag. Non-Amazon and smaller categories are labelled `small_sample_review_only`.

**Interpretation**  Differences may be driven by product mix, status mix, or sample size; no causal platform or category ranking is made.

**Business implication**  Focus comparisons on sufficiently observed groups and treat small groups as directional review candidates.

**Limitation**  Channel definitions are source labels, not independently verified operational systems.

## High-risk review candidates

**Observation**  Some categories and SKUs have higher status-proxy rates than the overall source population.

**Evidence**  The notebook flags groups with at least `100` distinct orders and above-overall cancellation or return status-proxy rates.

**Interpretation**  These are operational review candidates, not confirmed high-risk failures.

**Business implication**  Validate product mix, listing conditions, status capture, and fulfilment processes with business owners before action.

**Limitation**  No financial impact, root cause, service-level target, or causal evidence is available.

## Warehouse comparison exclusion

- Warehouse provider rates are standalone reference rows with no order ID, SKU, date, or transaction key.
- They are not linked to fulfilment performance or ranked as operational outcomes.
- Delivery duration, SLA compliance, true cancellation rate, true return rate, and courier speed are not calculated.
