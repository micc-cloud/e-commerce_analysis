# Phase 4 Sales Analytics Findings

## Reported sales scope

**Observation**  Amazon and international sales provide separate reported gross-value scopes.

**Evidence**  Amazon reported amount is INR-coded and totals `78,590,043.30`; international reported gross amount totals `10,834,927.19` but has no currency field.

**Interpretation**  The sources must not be added to one company-wide sales total without currency and scope controls.

**Business implication**  Use source-specific reporting packs and reconcile currencies before cross-source comparisons.

**Limitation**  Net sales is unavailable because discount, refund, and return-value fields are not present.

## Orders, units, and selling-price measures

**Observation**  Amazon contains `120,378` distinct orders and `116,646` reported units. The reported amount per distinct order is `652.86`, and the amount-per-unit measure is `673.75`.

**Evidence**  These figures reconcile to the DuckDB monthly sales output and use distinct `order_id` for order counts. International has `16,294` pieces and an amount-per-piece measure of `664.96`, but no order identifier.

**Interpretation**  Order counts and line-item units answer different questions. The order-value figure is a reported-value-per-distinct-order measure, not a fully validated AOV.

**Business implication**  Keep distinct orders, units, and amount-per-unit measures separate in management reporting.

**Limitation**  Amount is line-grain, status treatment is not an approved completed-order rule, and net adjustments are unavailable.

## Time trends and growth

**Observation**  Amazon reported amount is `28,838,708.32` in April, `26,225,004.75` in May, and `23,424,646.38` in June. May is down `9.06%` against April on a comparable complete-month basis.

**Evidence**  March 31 and June 29 are extract boundaries. March and June are labelled partial; MoM is suppressed whenever the current or prior month is partial. The first period has no prior denominator.

**Interpretation**  The data supports period monitoring, but not a reliable seasonal pattern claim.

**Business implication**  Use complete-month comparisons for growth decisions and obtain a longer, consistently bounded history for seasonal planning.

**Limitation**  Only four Amazon calendar months are available, and raw boundary-month changes are not decision-grade growth rates.

## Category and SKU contribution

**Observation**  The top five categories contribute `99.1%` of reported Amazon amount. The top five attributed SKUs contribute `3.0%` of the attributed-SKU amount scope.

**Evidence**  The leading categories are Set, kurta, Western Dress, Top, and Ethnic Dress. The leading SKUs are J0230-SKD-M, JNE3797-KR-L, J0230-SKD-S, JNE3797-KR-M, and JNE3797-KR-S. Both concentration denominators sum to 100%, and the top-five results were independently reproduced by direct group-bys.

**Interpretation**  Category mix is highly concentrated while SKU-level amount is more distributed across the available attributed-SKU scope.

**Business implication**  Prioritise availability, status, and catalogue-quality checks for high-contribution categories and products.

**Limitation**  Concentration is not profitability, and missing or unmatched SKU values limit SKU coverage.

## Channel, B2B, and geography

**Observation**  B2B reported amount is `591,220.79`, approximately `0.75%` of Amazon reported amount. The largest shipping-state amounts are Maharashtra, Karnataka, and Telangana.

**Evidence**  The notebook groups reported amount, units, and distinct orders by `sales_channel`, `b2b`, and `ship_state`.

**Interpretation**  These are descriptive Amazon segment views, not evidence that a channel or geography caused performance differences.

**Business implication**  Use these dimensions to frame operational and data-quality questions.

**Limitation**  International data lacks comparable channel, B2B, and currency fields; shipping state is not a customer identifier.

## Explicit exclusions

- Net sales, profit, gross margin, customer metrics, true return rate, fulfilment rate, and inventory turnover are not calculated.
- No causal conclusion is drawn from time or dimension comparisons.
- Partial months are not compared as complete months.
