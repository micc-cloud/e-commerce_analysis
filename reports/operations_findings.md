# Phase 7 Operations Analytics Findings

## Scope and denominator

**Observation**  Amazon operations analysis contains 128,969 line records and
120,378 distinct order IDs.

**Evidence**  Line-level status composition is reported separately from
order-level presence flags. Order-level proxy denominators use distinct
`order_id`.

**Interpretation**  The data supports descriptive status composition, not an
official operational-rate layer.

**Business implication**  Use the outputs to identify status-definition,
event-history, and process-data priorities.

**Limitation**  Status labels have no event timestamps or approved lifecycle
precedence rule.

## Mixed-status orders: governance finding

**Observation**  The analysis explicitly checks whether one order contains
multiple line statuses and never assigns a mixed order to a single status.

**Evidence**  The order table stores all status values, a `status_count`, and
the label `MIXED_STATUS_REQUIRES_RULE` whenever `status_count > 1`. The current
cleaned Amazon extract contains 0 mixed-status orders, but the check and detail
table are retained for future extracts. A future order such as Shipped +
Cancelled would remain unresolved rather than being labelled Cancelled or
Shipped.

**Interpretation**  The absence of mixed statuses is an observed property of
this extract, not evidence that a business precedence rule exists.

**Business implication**  Obtain an approved order-status precedence rule and
event-level status history before producing official cancellation, return, or
delivery outcomes.

**Limitation**  No line-status event history, transition timestamp, or
returned/refunded quantity is available.

## Status composition proxies

**Observation**  Source-status proxies are calculated over all 120,378 distinct
Amazon orders: cancelled 17,185 (14.28%), return-related 1,981 (1.65%),
shipped 102,339 (85.01%), and delivered-status proxy 26,566 (22.07%).

**Evidence**  Cancellation is exact `Cancelled`; return-related contains
`Return`; shipped begins with `Shipped`; delivered is exact
`Shipped - Delivered to Buyer`. Each is an order-level presence flag.

**Interpretation**  These figures describe source-status composition only.

**Business implication**  Use them to prioritise status taxonomy and event-data
quality review.

**Limitation**  They are not validated cancellation, return, fulfilment, or
delivery rates and must not be presented as such.

## Time, category, SKU, geography, and B2B/B2C

**Observation**  Status composition can be compared across time, categories,
SKUs, shipping states, and B2B/B2C groups using explicit group denominators.

**Evidence**  Time tables use distinct orders by observed month. Category,
SKU, geography, and B2B tables are built at `order_id + dimension` grain,
avoiding an unsafe order-to-category or order-to-SKU merge. Each table reports
distinct orders, line counts, proxy counts, proxy rates, and sample flags.

**Interpretation**  Group differences may reflect product mix, sample size, or
status capture rather than an operational cause.

**Business implication**  Investigate sufficiently observed groups with process
owners and collect event-level timestamps, status transition reasons, and
product-mix controls.

**Limitation**  Small groups are directional only. Multi-category and
multi-SKU orders mean group distinct-order totals can legitimately overlap and
must not be summed as a source-wide order total.

## Fulfilment and courier fields

**Observation**  Fulfilment, provider, and courier labels are available as
source mix indicators, but fulfilment comparison is skipped when only one
meaningful value is present.

**Evidence**  The notebook reports line and distinct-order counts by
`fulfilment`, `fulfilled_by`, and `courier_status`, without ranking speed.

**Interpretation**  Labels do not establish delivery duration or service level.

**Business implication**  Collect order-created, shipped, delivered, and
return-event timestamps before evaluating operational speed.

**Limitation**  No delivery time, processing time, SLA, on-time delivery, or
courier-speed metric is supported.

## Explicit exclusions

- Official cancellation, return, fulfilment, delivery, or SLA rates.
- Any invented order-status precedence rule.
- Delivery or processing duration and courier-speed ranking.
- Warehouse or expense attribution to orders; no safe transaction key exists.
- Predictive use of status or courier fields.
- Causal operational explanations or performance rankings.
