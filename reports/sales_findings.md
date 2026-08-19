# Phase 4 Sales Analytics Findings

## Scope and data quality

**Observation** Amazon reported sales are presented in a complete source scope and a delivered-status proxy scope. International sales remain separate.

**Evidence** Amazon has 128,969 lines, 120,378 distinct orders, 116,646 reported units, and `78,590,043.30` reported gross amount. Amount coverage is 93.96% (121,177 populated rows). The delivered-status proxy has 28,769 lines, 26,566 distinct orders, 28,886 units, `18,650,815.00` reported gross amount, and 99.97% amount coverage.

**Interpretation** The delivered scope is an analytical status convention, not a completed-sales definition. The reported-source scope is retained for source traceability.

**Business implication** Use both scopes for sensitivity review and show amount coverage alongside every monetary result.

**Limitation** `amount` is not validated revenue or net sales. Missing values, cancellations, returns, discounts, refunds, taxes, and shipping adjustments are not resolved.

## Amount coverage

**Observation** Amount completeness varies by status and period.

**Evidence** Overall Amazon coverage is 93.96%; cancelled-line coverage is approximately 59%, while delivered-status-proxy coverage is approximately 99.97%. The notebook reports coverage by status, date grain, month, category, SKU, channel, B2B flag, geography, and fulfilment.

**Interpretation** Amount-based comparisons may be status-sensitive and missingness cannot be assumed random.

**Business implication** Investigate missing amount records before using reported gross amount for operational decisions.

**Limitation** The source provides no rule for interpreting missing amount as zero, cancelled, unavailable, or another business state.

## Time trends and month-over-month change

**Observation** Reported Amazon amount was `28,838,708.32` in April 2022 and `26,225,004.75` in May 2022, a comparable change of `-9.06%`.

**Evidence** March 31 is a partial opening period and June 1–June 29 is a partial closing period. The notebook suppresses comparisons where either the current or previous month is partial.

**Interpretation** The extract supports short-window monitoring only.

**Business implication** Use complete-month comparisons for reporting and obtain longer consistently bounded history for planning.

**Limitation** The 91 observed Amazon dates cover only 2022-03-31 to 2022-06-29. No seasonality or forecasting claim is made.

## Category contribution

**Observation** Within the delivered-status proxy, Set, kurta, and Western Dress are the largest reported gross amount categories.

**Evidence** Their reported amounts are `8,800,562`, `4,715,208`, and `3,868,616`, respectively. The top five categories account for approximately 99.18% of the delivered-status-proxy amount scope.

**Interpretation** The result describes concentration within an analytical status scope, not completed sales or profitability.

**Business implication** Review availability and status composition for leading categories before making assortment or planning decisions.

**Limitation** Cross-source category mappings are not governed and amount is not net sales.

## SKU contribution and concentration

**Observation** The leading delivered-status-proxy SKUs are `JNE3797-KR-L`, `JNE3797-KR-M`, `SET183-KR-DH-M`, `JNE3797-KR-S`, and `JNE3797-KR-XL`.

**Evidence** Their reported amounts are `295,061`, `260,255`, `197,316`, `188,905`, and `174,942`. Together they represent approximately 5.99% of the SKU-attributed delivered-status-proxy amount scope.

**Interpretation** This is a reported sales concentration signal, not a profitability or demand ranking.

**Business implication** These variants merit stock and fulfilment review; low contribution alone is not evidence for rationalisation.

**Limitation** Product snapshot SKU matches remain unavailable, and no cost, lifecycle, or dated inventory data exists.

## B2B and source-local dimensions

**Observation** The Amazon extract contains B2C (`b2b=False`) and B2B (`b2b=True`) flags, plus channel, fulfilment, and shipping-state fields.

**Evidence** In the reported-source scope, B2C has `77,998,822.51` reported amount across 119,584 distinct orders, while B2B has `591,220.79` across 794 distinct orders. Amazon fulfilment labels show `54,319,516.00` for Amazon and `24,270,527.30` for Merchant reported amount. The leading shipping states are Maharashtra, Karnataka, Telangana, Uttar Pradesh, and Tamil Nadu.

**Interpretation** These are source-local mix comparisons, not full platform, customer, or causal performance analyses.

**Business implication** Use the dimensions for descriptive segmentation and data-quality follow-up.

**Limitation** International data has no comparable B2B, platform, order, or currency fields. Geography is shipping geography, not a customer identifier.

## Status composition

**Observation** Amazon contains cancellation-, return-, delivery-, and other status labels.

**Evidence** Distinct-order status proxies include 17,185 orders with a cancelled label, 1,981 with a return-related label, and 26,566 with the exact delivered-status proxy.

**Interpretation** These figures describe source-status composition only.

**Business implication** Use them to prioritise lifecycle-definition and operational data-quality review.

**Limitation** They are not official cancellation, return, or fulfilment rates. No approved status precedence, return quantity, refund value, or event timestamp exists.

## Explicit exclusions

- Validated net sales, refund-adjusted sales, profit, margin, and customer KPIs.
- Official cancellation, return, fulfilment, delivery, or SLA rates.
- Inventory or stockout KPIs.
- Cross-currency aggregation of Amazon and international amounts.
- Seasonality, forecasting, causal, or price-elasticity claims.
