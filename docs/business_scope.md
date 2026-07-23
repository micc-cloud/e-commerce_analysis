# Phase 1 Business Scope

## Realistic business scenario

The available files support a portfolio analysis of an apparel e-commerce business selling through Amazon and an international/wholesale sales process, with separate product-price snapshots, a stock snapshot, warehouse provider rates, and a small expense report. The analysis can assess reported sales activity, order/status mix, product and variant mix, reference pricing, and current stock patterns.

The evidence does not support a fully reconciled P&L, customer-360 model, or inventory-turnover model. This scope therefore focuses on commercial and operational decision support while clearly separating reported sales from profit.

## Decision scope

### Sales

- How do reported Amazon sales and international gross amounts trend by date/month?
- What is the order, line, and unit mix by status, fulfilment type, category, SKU, geography, and B2B flag?
- Which sales records are cancelled, returned-to-seller, pending, or delivered under explicit status rules?

### Products

- Which categories, styles, SKUs, sizes, and colours contribute reported sales or units?
- Which product reference SKUs can be matched safely to product-price snapshots?
- Where are missing SKU and category values limiting product attribution?

### Pricing

- How do reported selling rates compare with available MRP/reference-price fields within matched SKU populations?
- Which marketplace reference prices differ across channels?
- What price coverage and currency limitations prevent a realised-price or discount conclusion?

### Operations

- What is the fulfilment and courier-status mix in Amazon data?
- Which stock snapshot variants have zero or low reported stock?
- How do the two warehouse provider reference rates differ by cost head?

### Profitability

- Which expense and warehouse records are available as standalone reference information?
- What additional cost, discount, refund, currency, and allocation fields are required before profit or margin can be calculated?

## Table grains and relationship map

| Dataset | Grain | Key status |
|---|---|---|
| Amazon sales | One order line | `order_id` repeats; line-level duplicate candidate remains |
| International sales | One retained sales line | No order ID; `sku` missing in 1,379 rows |
| May 2022 product prices | One SKU/size snapshot row | `sku` unique in snapshot |
| March 2021 product prices | One SKU/size snapshot row | `sku` unique in snapshot |
| Sale Report | One SKU/size/colour stock row | `sku_code` missing/non-unique |
| Warehouse comparison | One cost-head reference row | Not a transaction ledger |
| Expense IIGF | One detail or summary report row | Mixed detail/summary grain |

Candidate SKU relationships must be treated as left joins with match-rate reporting. Never join the report-level expense or warehouse tables directly to sales lines.

## Business-question tree

```text
Business performance
├── Sales
│   ├── Reported gross sales by date/month and source
│   ├── Distinct Amazon orders and line/unit mix
│   └── Status, fulfilment, geography, and B2B composition
├── Products
│   ├── Category/style/SKU contribution
│   ├── Size and colour mix
│   └── SKU match coverage to product snapshots
├── Pricing
│   ├── Reported rate and selling-price distributions
│   ├── MRP/reference-price comparisons
│   └── Marketplace reference-price dispersion
├── Operations
│   ├── Amazon fulfilment and courier-status mix
│   ├── Stock snapshot and zero-stock exposure
│   └── Warehouse provider rate comparison
└── Profitability
    ├── Expense and receipt report structure
    ├── Standalone logistics-rate references
    └── Data required for cost allocation and margin
```

## Governance boundaries

- Reported amount is not profit.
- `customer` text is not a reliable customer identifier.
- `tp`, `tp_1`, and `tp_2` are not treated as cost without confirmation.
- Cancelled and returned statuses must be explicitly filtered or reported; no silent netting is allowed.
- Cross-source currency aggregation is excluded because only Amazon rows carry a populated currency code.
