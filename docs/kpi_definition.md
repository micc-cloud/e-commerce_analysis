# Phase 1 KPI Feasibility

## Rules

- Calculate Amazon KPIs and international-sales KPIs separately unless a common currency, scope, and grain are established.
- Treat Amazon rows as line grain and use `COUNT(DISTINCT order_id)` for order-level denominators.
- Do not treat `tp`, `tp_1`, or `tp_2` as cost until their business definition is confirmed.
- Exclude or separately label cancelled/returned statuses; do not silently mix them with completed sales.

## Feasibility matrix

| Proposed KPI | Business definition | Formula | Required fields | Available fields | Feasible | Limitations |
|---|---|---|---|---|---|---|
| Gross sales | Reported gross sales value before validated returns/refunds | Amazon: `SUM(amount)`; International: `SUM(gross_amt)` | Amount, scope, currency | `amount`, `currency`, `gross_amt` | Partial | Amount coverage differs; international currency absent; do not combine files |
| Net sales | Sales after discounts, cancellations, returns, and refunds | Gross sales - discounts - returns/refunds | Gross amount, discounts, returns/refunds | Gross amount, `promotion_ids`, status only | Partial | No discount amount, refund value, or return amount |
| Order count | Distinct orders in a defined period/scope | `COUNT(DISTINCT order_id)` | Order ID, date | Amazon `order_id`, `date` | Yes, Amazon-only | International has no order ID; order status needs line-to-order rule |
| Units sold | Quantity/pieces sold under a defined status scope | Amazon: `SUM(qty)`; International: `SUM(pcs)` | Quantity, status scope | `qty`, `pcs`, `status` | Partial | Gross units possible; net units/returns not supported |
| Average selling price | Reported sales value per unit | `SUM(amount) / SUM(qty)` or `SUM(gross_amt) / SUM(pcs)` | Amount, quantity | `amount`, `qty`, `gross_amt`, `pcs` | Partial | Currency/scope and cancellation treatment; zero quantities exist |
| Average order value | Reported order value per distinct order | `SUM(order_value) / COUNT(DISTINCT order_id)` | Order ID, order-level value | `order_id`, `amount` | Partial | `amount` grain/treatment must be confirmed; international lacks order ID |
| Cancellation rate | Share of orders classified cancelled | `COUNT(DISTINCT cancelled order_id) / COUNT(DISTINCT order_id)` | Order ID, status | `order_id`, `status` | Partial | Multiple line statuses require an order-level precedence rule |
| Return rate | Share of orders/units returned | Returned orders or units / total orders or units | Return flag/quantity, order or line key | Status includes returned-to-seller labels | Partial | Status proxy only; no return quantity or refund value |
| Fulfilment rate | Share delivered/fulfilled under a declared definition | `COUNT(DISTINCT delivered order_id) / COUNT(DISTINCT order_id)` | Order ID, fulfilment outcome | `order_id`, `status`, `courier_status`, `fulfilment` | Partial | No approved delivered definition or SLA denominator |
| Profit | Sales less validated product, logistics, platform, and other costs | `net sales - attributable costs` | Net sales and attributable cost ledger | Warehouse rates and expense report lack transaction linkage | No | No reliable cost allocation or common period/currency |
| Gross margin | Gross profit as a percentage of net sales | `(net sales - COGS) / net sales` | Net sales, COGS | No confirmed COGS field; `tp*` undefined | No | TP fields cannot be assumed to be COGS |
| Customer metrics | Customer count, repeat rate, frequency, or customer value | E.g. distinct customer IDs; repeat customers / customers | Stable customer ID, order ID, date | International `customer` text only | No | No reliable customer identifier across datasets; do not propose customer-360 analysis |
| Inventory metrics | Stock on hand, stockout rate, turnover, or days of inventory | E.g. `SUM(stock)`; turnover = COGS / average inventory | Stock, dates, sales/cost, snapshots | `stock`, `sku_code`, sales quantities | Partial | Stock date absent; no average inventory or COGS; turnover/DOI not feasible |

## Explicitly excluded from Phase 1

- Profit, gross margin, contribution margin, and ROI.
- True return rate, refund rate, and net sales after refunds.
- Customer lifetime value, retention, repeat purchase rate, and customer cohort metrics.
- Inventory turnover, days inventory outstanding, and stockout rate over time.
- Delivery time, on-time delivery, and SLA compliance.
- Cross-channel total sales or price index without common currency, dates, and product-match coverage.

These exclusions are scope controls, not statements that the business does not need the KPIs.
