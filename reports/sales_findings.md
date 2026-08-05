# Phase 4 Sales Analytics Findings

## Scope and data quality

**Observation**  Amazon sales are reported in two explicit scopes: `reported_source` and `delivered_status_proxy`.

**Evidence**  The delivered proxy is the exact status `Shipped - Delivered to Buyer` and contains `28,769` lines, `26,566` distinct orders, `28,886` units, and `18,650,815.00` reported amount. The complete source contains `128,969` lines and `120,378` distinct orders.

**Interpretation**  The delivered scope is a status proxy, not a confirmed completed-sales definition. It is provided to show status sensitivity without silently deleting source rows.

**Business implication**  Use the source scope for traceability and the delivered proxy for controlled sensitivity analysis until a business-approved status rule exists.

**Limitation**  Cancelled and returned records remain in the reported source scope; no net-sales fields exist.

## Amount coverage

**Observation**  Amount completeness varies materially by status and period.

**Evidence**  Amazon amount coverage is approximately `94%` overall, approximately `59%` for cancelled rows, and approximately `100%` for delivered-status-proxy rows. Coverage is also reported by month and category in the notebook.

**Interpretation**  Amount-based comparisons may be status-sensitive and are not necessarily missing at random.

**Business implication**  Include coverage beside every amount-based KPI and investigate missing cancelled amounts before executive reporting.

**Limitation**  Missing amount values cannot be recovered from the available files.

## Orders, units, and price measures

**Observation**  Amazon reported-source totals are `120,378` distinct orders and `116,646` units. The delivered-status proxy contains `26,566` distinct orders and `28,886` units.

**Evidence**  SQL and pandas reconcile both scopes. Amount-per-unit and amount-per-distinct-order are explicitly labelled reported measures; true AOV is not calculated.

**Interpretation**  Order-level and line-level measures remain distinct, and status scope materially changes the result.

**Business implication**  Present reported-source and status-proxy measures side by side rather than calling either one net sales or confirmed AOV.

**Limitation**  `amount` is line-level and discounts, refunds, returns, taxes, and shipping adjustments are unavailable.

## Time trends and growth

**Observation**  Reported-source Amazon amount is `28,838,708.32` in April and `26,225,004.75` in May; comparable May versus April growth is `-9.06%`.

**Evidence**  March and June are partial extract months. Growth is suppressed whenever the current or previous month is partial.

**Interpretation**  The data supports short-window monitoring, not seasonality conclusions.

**Business implication**  Use complete-month comparisons and obtain longer, consistently bounded history.

**Limitation**  The Amazon extract covers only March 31 through June 29, 2022.

## Explicit exclusions

- Net sales, true AOV, profit, margin, customer metrics, true return rate, fulfilment rate, and inventory turnover are not calculated.
- No causal conclusion is drawn from time or dimension comparisons.
- International sales remain separate because currency and order identifiers are unavailable.
