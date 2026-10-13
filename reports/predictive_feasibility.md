# Phase 9: Predictive Analytics Feasibility

## Decision

**PASS WITH WARNINGS — no predictive model is recommended at this stage.**

The available datasets support descriptive analysis and baseline monitoring,
but none of the proposed use cases has a target, predictor timing, validation
design, and business actionability combination strong enough for a defensible
model. The phase therefore stops without creating a predictive notebook.

## Dataset evidence

- Amazon contains 128,969 line records, 120,378 distinct orders, and 91
  observed dates from 2022-03-31 through 2022-06-29.
- International sales contain 12,322 retained lines and 162 observed dates from
  2021-06-05 through 2022-05-11, but no order identifier and no currency.
- Amazon status outcomes are recorded as final/status fields, with no event
  timestamps for order, dispatch, delivery, cancellation, or return events.
- Amazon has 7,195 SKUs and 12,804 zero-quantity lines; international sales
  have 4,590 non-null SKUs, but cross-source SKU matching is not reliable.
- The data has no reliable customer identifier, no dated inventory history,
  no validated cost ledger, and no transaction-linked profit fields.

## Use-case assessment

| Use case | Target definition | Data volume / date coverage | Class balance | Leakage risk | Available predictors | Business actionability | Baseline and validation | Decision |
|---|---|---|---|---|---|---|---|---|
| Sales forecasting | Future reported sales amount or units at a defined source/date grain | Amazon has only 91 dates and partial boundary periods; international has no order ID, currency, or common scope | Not a class problem; daily values are affected by status and missing amounts | Status and amount completeness can reflect post-order outcomes; partial periods and source definitions are unresolved | Date, quantity, category, SKU, fulfilment, channel, B2B, and status are present, but predictor timing is not defined | A forecast could support planning, but no approved planning horizon, inventory linkage, or decision threshold exists | Seasonal-naive/last-value baseline and time split would be possible, but the short, status-mixed series is not sufficient for reliable business value | No |
| Demand forecasting | Future demand/units by SKU or category before fulfilment outcome | 91 Amazon dates with sparse SKU-date observations; no dated inventory or stockout history | Not a class problem; many SKU-date cells are zero or unobserved | Using status, amount, courier, or fulfilment fields would use information unavailable at prediction time | SKU, category, size, quantity, date, and B2B exist; no lagged demand history of sufficient duration or inventory context | Could inform replenishment, but stock decisions cannot be evaluated without dated inventory and stockout context | Seasonal-naive or moving-average baseline with rolling-origin validation would be required; coverage is too short and sparse | No |
| Order cancellation prediction | Cancellation flag known before fulfilment, at order creation | 120,378 distinct Amazon orders; observed cancellation status proxy is 17,185 orders (14.28%), but there are no order-event timestamps | Supervised class balance is approximately 14.28% positive using the status proxy | `status`, `courier_status`, `fulfilment`, and potentially amount are outcome or post-order fields; no as-of cutoff can be enforced | SKU/category, date, service level, channel, B2B, and location fields exist, but their availability at order creation is undocumented | Potentially actionable for intervention, but the intervention workflow, decision lead time, and approved target are missing | Stratified baseline plus time-based split is possible in principle, but leakage cannot be ruled out with current timestamps and field lineage | No |
| Return prediction | True return/refund event or quantity attributable to an order/line | 120,378 orders; 1,981 return-status-proxy orders (1.65%), but no return quantity, refund amount, or return event date | Approximately 1.65% positive by status proxy; this is not a validated return label | Status and courier fields can encode the outcome; no pre-return observation cutoff exists | Product and fulfilment fields exist, but no validated customer, delivery-event, reason, or refund predictors | Could support prevention or service intervention, but a true return target and intervention timing are absent | Rare-event baseline and time split would be needed; proxy target and leakage make model performance uninterpretable | No |
| Profit forecasting | Future validated net profit or margin | No validated net revenue, COGS, platform fees, fulfilment/shipping costs, taxes, refunds, or allocation keys | Not applicable | Any constructed target from amount, `tp*`, warehouse rates, or expense totals would encode unsupported assumptions | Reported amount, quantity, status, and reference prices exist, but no cost predictors or valid target | Not actionable because the target itself cannot be calculated | No meaningful baseline or temporal validation can be defined until a costed ledger exists | No |

## Why modelling is not recommended

1. The available time history is short for forecasting and does not establish
   stable seasonality. Boundary periods are partial and the Amazon and
   international sources cannot be combined safely.
2. Cancellation and return labels are status proxies, not approved event
   targets. The files do not say when each predictor became available, so a
   time-based split alone would not remove target leakage.
3. The strongest operational fields, including status and courier status, are
   likely downstream of the decision a model would need to support.
4. Demand modelling lacks dated inventory and stockout observations, making
   observed quantity a potentially censored measure of demand.
5. Profit forecasting is blocked by the Phase 8 feasibility decision: no valid
   costed profit target exists.
6. No business owner, intervention, forecast horizon, service-level target, or
   cost of false positives/false negatives is documented.

## Minimum additional data required

- At least 12–24 months of consistently defined daily or weekly history,
  including complete periods and a governed calendar.
- A point-in-time order-event ledger with order creation, payment, fulfilment,
  dispatch, delivery, cancellation, return, and refund timestamps.
- A governed pre-outcome feature set with field availability timestamps.
- A stable customer/account identifier only if customer history is approved for
  the use case.
- Dated inventory snapshots, stockout flags, replenishment events, and lead
  times for demand forecasting.
- A transaction-linked cost and fee ledger before any profit target can be
  created.
- An approved SKU crosswalk and consistent currency definitions across sources.
- A business decision specification: prediction horizon, action, threshold,
  owner, and cost of errors.

## Recommended next action

Do not create `notebooks/08_predictive_analysis.ipynb` yet. First obtain the
event-level history and business decision definition above. Reassess sales or
demand forecasting only after the data supports a leakage-controlled,
time-based backtest against a naive baseline.
