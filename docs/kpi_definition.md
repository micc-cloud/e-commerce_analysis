# Phase 1 KPI Governance

This document separates metrics supported by the Kaggle extracts from
mathematically valid proxies and unsupported business KPIs. No missing value,
cost, currency, customer, or status rule is invented.

## Analytical conventions

- Amazon rows are treated as line grain. Order counts use
  `COUNT(DISTINCT order_id)`.
- International rows are line grain and have no order identifier or currency.
- Amazon and international monetary results remain separate.
- The raw sales date convention is month-day-year (`%m-%d-%y`). Cleaned
  international dates are displayed as `mm/dd/yyyy` and validated against
  `months`.
- Cancelled, returned, pending, shipped, and delivered labels are source
  statuses. No official order-level precedence rule is available.
- Any status-based scope below is an **analytical convention**, not an approved
  business rule.
- Missing `amount`, zero quantity, and zero amount are retained. They are not
  imputed or silently dropped.
- `tp`, `tp_1`, and `tp_2` are undefined reference fields until the business
  confirms whether they represent a price, transfer value, or cost.

## Supported metrics

| Metric | Formula / scope | Supported use | Limitation |
|---|---|---|---|
| Amazon distinct order count | `COUNT(DISTINCT order_id)` | Amazon date/status/source-local reporting | Not available for international sales |
| Amazon line count | `COUNT(*)` | Line-grain volume and QA | Not an order count |
| Amazon reported units | `SUM(qty)` within a declared scope | Gross unit reporting | Zero quantities and status treatment require disclosure |
| International reported pieces | `SUM(pcs)` | Source-local piece reporting | No order ID, return data, or currency |
| Amazon reported gross amount | `SUM(amount)` on rows with reported amount | INR-only source-local reporting | Amount is not validated net revenue; 7,792 rows are missing amount |
| International reported gross amount | `SUM(gross_amt)` | International source-local reporting | Currency is absent; do not combine with Amazon |
| Source-local category/SKU/style/size mix | Group-by counts, units, or reported amount | Descriptive product analysis | Cross-source mappings are not reliable |
| Stock snapshot total | `SUM(stock)` at observed snapshot grain | Current-file stock description | Date absent; duplicate `sku_code` values prevent simple SKU-level joins |
| Warehouse reference-rate comparison | Compare provider fields by `cost_head` | Standalone reference comparison | Not an allocated fulfilment cost |

## Proxy metrics

These calculations are permitted only when labelled as proxies.

| Proxy | Analytical convention | Limitation |
|---|---|---|
| Delivered status proxy | `status = 'Shipped - Delivered to Buyer'` | Not confirmed completed sales; no event timestamp |
| Cancellation status proxy | An Amazon order has a line with exact status `Cancelled` | Not a true cancellation rate without lifecycle precedence |
| Return status proxy | An Amazon order has a status containing `Return` | Not a true return/refund rate; no returned quantity or refund value |
| Reported amount per unit | `amount / qty` only where amount exists and `qty > 0` | Not validated realised selling price; amount may be status-sensitive |
| Reported-sales Pareto/ABC | Cumulative contribution of a declared sales scope | Not profitability, demand, or inventory ABC |
| Zero-stock row count | Count of rows where `stock = 0` | Snapshot observation, not stockout rate |

## Partially supported metrics

- Average selling price is a reported amount-per-unit proxy only.
- Average order value is possible for Amazon reported amounts, but its
  interpretation is limited by line-level amount coverage and status scope.
- Gross sales are possible separately by source, but currency and amount
  coverage prevent a consolidated total.
- Units are possible under a declared source/status scope, but not as net units
  after returns or refunds.

## Unsupported metrics

- Official net sales after discounts, cancellations, returns, refunds, taxes,
  or shipping adjustments.
- Profit, COGS, gross profit, gross margin, contribution margin, ROI, and
  profitability by SKU/category/platform.
- True cancellation rate, return rate, refund rate, delivery time, on-time
  delivery, and SLA compliance.
- Customer count, repeat purchase rate, retention, lifetime value, and cohort
  analysis. `customer` text is not a governed customer identifier.
- Inventory turnover, days of inventory, stockout-over-time, and demand
  forecasting from the undated stock snapshot.
- Cross-source sales totals or price indexes without common currency, dates,
  grain, and a governed SKU crosswalk.

## Required future definitions/data

- Business-approved order-status precedence and completed-sales scope.
- Definition of Amazon `amount` and the treatment of missing/zero values.
- Definitions of `tp`, `tp_1`, and `tp_2`.
- International currency and FX basis plus an order identifier if order KPIs
  are required.
- A governed SKU crosswalk and confirmed category/style/size taxonomy.
- Dated inventory snapshots and a stockout definition.
- Transaction-linked costs, fees, taxes, returns, refunds, and shipping data.
