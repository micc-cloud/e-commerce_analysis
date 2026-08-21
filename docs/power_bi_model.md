# Power BI Model

## Model design

Use a small source-local star schema for Amazon analysis. `fact_amazon_sales`
is the central fact table. The international fact is intentionally standalone.
The product snapshots, stock snapshot, warehouse reference rates, and expense
report are not loaded into this dashboard model because their keys, dates, or
currency definitions do not support safe relationships.

## Tables and grain

| Table | Grain | Key |
|---|---|---|
| `fact_amazon_sales` | One Amazon source order-line record | No reliable line-level primary key; `order_id` repeats by design |
| `dim_date` | One observed Amazon calendar date | `date_key` |
| `dim_category` | One Amazon source-local category | `category_key` |
| `dim_sku` | One Amazon source-local SKU | `sku_key` |
| `dim_order_status` | One distinct Amazon order | `order_id` |
| `fact_international_sales` | One retained international sales line | No order key; no dashboard relationship |

## Relationships

Create these relationships in Model view:

| From (one) | To (many) | Cardinality | Cross-filter direction |
|---|---|---|---|
| `dim_date[date_key]` | `fact_amazon_sales[date_key]` | 1 : * | Single, dimension to fact |
| `dim_category[category_key]` | `fact_amazon_sales[category]` | 1 : * | Single, dimension to fact |
| `dim_sku[sku_key]` | `fact_amazon_sales[sku]` | 1 : * | Single, dimension to fact |
| `dim_order_status[order_id]` | `fact_amazon_sales[order_id]` | 1 : * | Single, dimension to fact |

Do not create relationships from `fact_international_sales` to any Amazon
table. It has no currency, order ID, or validated cross-source SKU key. Do not
relate Amazon sales to May/March product snapshots, stock, warehouse rates, or
expenses.

## Key and cardinality checks

- `dim_date[date_key]` is unique.
- `dim_category[category_key]` is unique.
- `dim_sku[sku_key]` is unique within the Amazon source.
- `dim_order_status[order_id]` is unique.
- `fact_amazon_sales[order_id]` is intentionally repeated.
- `fact_international_sales` remains line grain with no order-level measures.

## Filter behavior

Use single-direction dimension-to-fact filtering. Avoid bidirectional filters,
many-to-many relationships, and calculated bridge tables. Slicers from the
Amazon dimensions should affect Amazon visuals only. International visuals
must use fields and measures from `fact_international_sales` alone.

## Status governance

`dim_order_status[status_label]` is a source-status label. If an order ever
contains multiple line statuses, it is labelled
`MIXED_STATUS_REQUIRES_RULE`; it must not be assigned to Cancelled, Shipped, or
Delivered without an approved precedence rule.

## Recommended Power BI data types

- Date columns: Date.
- `date_key`: Whole number.
- `qty`, `amount`, `reported_unit_price_proxy`, `pieces`, `rate`, and
  `reported_gross_amount`: Decimal number.
- Boolean flags: True/False.
- IDs, SKU, category, status, and geography: Text.
