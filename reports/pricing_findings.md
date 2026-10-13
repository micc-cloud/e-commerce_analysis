# Phase 6 Pricing Analytics Findings

## Scope and definition

**Observation**  Pricing analysis is restricted to Amazon rows in the exact
`Shipped - Delivered to Buyer` `delivered_status_proxy` scope.

**Evidence**  A reported unit-price proxy is calculated only where `amount` is
present, `qty > 0`, and `currency == INR`, using `amount / qty` at line grain.
The valid population contains 28,761 lines and 28,886 units.

**Interpretation**  The proxy describes reported amount per unit within one
source and status convention.

**Business implication**  Use the results for price-quality monitoring and
follow-up investigation, not as confirmed realised selling-price guidance.

**Limitation**  `amount` is not validated net revenue or realised selling
price; 8 delivered-proxy rows have missing amount and 8 have non-positive
quantity. The full Amazon source has 7,792 missing amounts.

## Unit-price distribution

**Observation**  The typical reported unit-price proxy is 629 INR at the
median and 645.82 INR at the mean.

**Evidence**  Valid unit-price rows contain 716 zero-price observations and no
negative unit-price observations. Zero-amount rows are retained as anomalies,
not removed.

**Interpretation**  The mean being above the median indicates a higher-priced
tail in this observed population, but does not establish customer response.

**Business implication**  Investigate zero-amount lines and high-price lines
with the source owner before using this proxy in pricing decisions.

**Limitation**  No approved anomaly threshold, discount value, promotion value,
or causal design is available.

## Time variation

**Observation**  The median proxy rises across the observed interior months:
568 INR in April, 648 INR in May, and 725 INR in June.

**Evidence**  Valid-price lines by month are March 16, April 12,075, May
10,399, and June 6,271. March and June are partial boundary periods; the
notebook labels them and does not treat this as seasonality.

**Interpretation**  Monthly differences may reflect product mix, status
composition, or incomplete coverage rather than price effects.

**Business implication**  Use month-level changes as a monitoring signal for
catalogue and source-quality review.

**Limitation**  The Amazon data covers only 91 observed dates, so no
seasonality, elasticity, or causal price-volume conclusion is supported.

## SKU and category variation

**Observation**  Reported unit-price distributions vary by source-local SKU
and category.

**Evidence**  The notebook reports median, mean, minimum, maximum, range,
valid line count, and units for each SKU and category. High-variation SKU
review is restricted to groups with at least 5 valid lines; for example,
`J0280-SKD-M` has a 1,556 INR observed range across 21 lines.

**Interpretation**  Within-SKU variation can reflect zero amounts, product
mix, size, status, promotions, or data-quality issues.

**Business implication**  Prioritise high-variation SKUs for catalogue,
promotion, and transaction-quality investigation.

**Limitation**  Amazon SKUs have zero exact matches to the May/March product
snapshots, so no MRP or listed-price enrichment is valid.

## Price bands and volume

**Observation**  Most valid-price lines fall in the `[500,1000)` INR band.

**Evidence**  Mutually exclusive bands contain: `[0,500)` 10,053 lines and
10,104 units; `[500,1000)` 15,831 lines and 15,895 units; `[1000,2000)` 2,870
lines and 2,880 units; `[2000,inf)` 7 lines and 7 units. Reported gross amount
is shown separately by band.

**Interpretation**  These bands describe observed volume distribution only.

**Business implication**  Use bands for monitoring and sample review, not for
optimal-price or demand recommendations.

**Limitation**  Band boundaries are analytical thresholds, not approved
commercial price tiers.

## B2B/B2C, geography, and fulfilment

**Observation**  B2B lines have a higher median proxy than B2C lines, while
fulfilment cannot be compared across groups.

**Evidence**  B2B has 249 valid lines, 685 INR median, and 705.48 INR mean;
B2C has 28,512 lines, 629 INR median, and 645.29 INR mean. The valid population
contains one fulfilment value, `Merchant`, so no fulfilment comparison is
reported. Geographic tables report sample sizes; small states must be treated
cautiously.

**Interpretation**  These are descriptive source-local differences and may be
driven by product mix or sample size.

**Business implication**  Use adequately sized B2B/B2C and state groups as
areas for further investigation, not as pricing recommendations.

**Limitation**  No causal, elasticity, or optimal-price claim is made; the
fulfilment dimension has no comparison group and international currency is
unavailable.

## Explicit exclusions

- Discount amount and discount percentage.
- Amazon selling-price versus MRP, because exact Amazon-to-snapshot SKU match
  is zero.
- High-discount product identification from `promotion_ids` alone.
- Profit, margin, cost, price elasticity, causal price-volume analysis, and
  specific price recommendations.
- Cross-currency or international monetary price aggregation.

All extreme values were investigated with an IQR flag and retained. No source
or cleaned dataset was modified.
