# Phase 1 Business Scope

## Scope decision

The Kaggle extracts support controlled, source-local descriptive analysis of
reported e-commerce activity, product mix, reference prices, and a stock
snapshot. They do not support an official completed-sales KPI layer, a
customer-360 model, a reconciled P&L, or predictive modelling.

## Supported business questions

### Sales

- How do Amazon reported amounts, distinct orders, lines, and units vary by
  date and declared source/status scope?
- How do international reported pieces and gross amounts vary by date?
- What is the source-local mix by category, SKU, geography, fulfilment, and B2B
  flag?

### Products

- Which source-local categories, styles, SKUs, sizes, and colours contribute
  reported sales or units?
- What is the match coverage to product snapshots?
- Which stock snapshot rows have zero or low reported stock?

### Pricing

- What are the distributions of reported amount per unit and reference MRP
  fields within their own source/snapshot scope?
- How dispersed are reference prices across marketplace columns within the same
  product snapshot?

### Operations

- What is the Amazon source-status, fulfilment, and courier-status composition?
- What warehouse provider rates are shown by cost head?

### Profitability and prediction

- Which additional data is required for transaction-level cost allocation and
  profit?
- Which data gaps prevent a leakage-controlled predictive target?

## Table grains and relationships

| Dataset | Grain | Key status |
|---|---|---|
| Amazon sales | One source order-line record | `order_id` repeats; no line ID |
| International sales | One retained source sales line | No order ID; no currency; `sku` can be missing |
| May 2022 product prices | One SKU snapshot row | `sku` unique within snapshot |
| March 2021 product prices | One SKU snapshot row | `sku` unique within snapshot |
| Sale Report | One SKU/size/colour stock row | `sku_code` missing/non-unique |
| Warehouse comparison | One cost-head reference row | Not a transaction ledger |
| Expense IIGF | One detail or summary report row | Mixed detail/summary grain |

Candidate SKU links are diagnostics only. Product, stock, warehouse, and
expense tables must not be treated as confirmed foreign-key relationships.
Warehouse and expense records must never be joined directly to sales lines.

## Status handling

- The complete Amazon source is retained for traceability.
- `delivered_status_proxy` and cancellation/return status proxies are
  analytical conventions only.
- Proxy rates must be labelled as source-status composition, not official
  business rates.
- No cancelled or returned amount is silently netted from reported sales.

## Governance boundaries

- Reported amount is not net sales and is never profit.
- International money is not combined with Amazon money because currency is
  absent.
- `customer` text is not a reliable customer identifier.
- `tp`, `tp_1`, and `tp_2` are not treated as cost.
- Stock is an undated snapshot, not a time series.
- Cross-source enrichment is blocked until a governed SKU crosswalk exists.
