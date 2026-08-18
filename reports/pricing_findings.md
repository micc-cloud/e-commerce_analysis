# Phase 6 Pricing Analytics Findings

## Observed selling-price proxy

**Observation**  A line-level unit-price proxy is available for delivered-status-proxy Amazon rows with INR currency, populated amount, and positive quantity.

**Evidence**  The valid population contains `28,761` rows. Median reported amount per unit is `629 INR`; the mean is approximately `645.82 INR`. Zero unit-price rows total `716`; no negative unit prices were observed.

**Interpretation**  The distribution describes reported amount per unit within the exact `Shipped - Delivered to Buyer` status proxy.

**Business implication**  Use the measure for price-quality monitoring and investigation, not as a confirmed net realised price.

**Limitation**  Amount is line-level, status is a proxy, and promotion/discount values are unavailable.

## Platform reference-price differences

**Observation**  Platform-labelled MRP/reference prices vary for some product snapshot rows.

**Evidence**  In the May snapshot, `1,293` rows have at least two platform values and `266` rows have a non-zero range across the eight platform-labelled MRP fields. The largest observed row range is `800 INR`.

**Interpretation**  These are catalogue reference-price differences within a product snapshot, not realised marketplace price differences.

**Business implication**  Review catalogue governance and platform-price maintenance for rows with large reference-price ranges.

**Limitation**  Platform field definitions, timing, and commercial comparability are not confirmed. MRP is not cost.

## Price variation by SKU and category

**Observation**  SKU and category unit-price distributions differ within the delivered-status proxy.

**Evidence**  The notebook reports median, mean, minimum, maximum, range, line count, and units by SKU and category.

**Interpretation**  Variation may reflect product mix, size, promotions, status, or data quality; it does not establish elasticity or an optimal price.

**Business implication**  Use high-variation groups as candidates for source and catalogue review.

**Limitation**  No causal design or repeated controlled price experiment exists.

## Price bands and anomalies

**Observation**  Most valid-price rows fall in the `[500,1000)` INR analytical band.

**Evidence**  The mutually exclusive bands contain: `[0,500)` `10,053` lines, `[500,1000)` `15,831`, `[1000,2000)` `2,870`, and `[2000,inf)` `7`.

**Interpretation**  The bands describe observed volume distribution only.

**Business implication**  Use bands for monitoring and sample review rather than price recommendations.

**Limitation**  Band boundaries are analytical thresholds, not business-approved pricing tiers.

## Discount and listed-price exclusions

- Discount amount and discount percentage are not calculated.
- Selling price versus MRP is not calculated because Amazon-to-May product SKU matches are `0`.
- High-discount products cannot be identified from `promotion_ids` alone.
- No price increase or elasticity recommendation is made.
- Amazon and international price fields are not combined because international currency is unavailable.
- No profit or margin conclusion is made from price alone.
