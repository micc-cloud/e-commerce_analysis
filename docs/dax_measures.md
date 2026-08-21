# DAX Measures

Create these measures in the model. Table and column names match the prepared
CSV package. Amount measures intentionally preserve blank `amount` values;
coverage is always shown beside monetary visuals.

## Amazon sales measures

### Reported Gross Amount

```DAX
Reported Gross Amount =
SUM ( fact_amazon_sales[amount] )
```

Classification: `SUPPORTED` within the Amazon source. Definition: sum of
reported `amount` values. Limitation: not validated net sales, profit, or
refund-adjusted revenue; currency is INR where populated.

### Amount Coverage %

```DAX
Amount Coverage % =
DIVIDE (
    COUNTROWS ( FILTER ( fact_amazon_sales, NOT ISBLANK ( fact_amazon_sales[amount] ) ) ),
    COUNTROWS ( fact_amazon_sales )
)
```

Classification: `SUPPORTED` data-quality measure. Definition: rows with a
reported amount divided by all fact rows in the current filter context.
Limitation: coverage does not explain why an amount is missing.

### Distinct Orders

```DAX
Distinct Orders =
DISTINCTCOUNT ( fact_amazon_sales[order_id] )
```

Classification: `SUPPORTED`. Definition: distinct Amazon `order_id` values.
Limitation: not available for international sales and not a line count.

### Gross Units

```DAX
Gross Units =
SUM ( fact_amazon_sales[qty] )
```

Classification: `SUPPORTED` source-local units measure. Limitation: not net
units after returns/refunds and retains source zero or negative quantity
states.

### B2B Orders

```DAX
B2B Orders =
CALCULATE ( [Distinct Orders], fact_amazon_sales[b2b] = TRUE () )
```

Classification: `SUPPORTED` source-local mix measure. Limitation: the source
B2B flag is used descriptively and does not define customer type beyond the
source field.

### B2C Orders

```DAX
B2C Orders =
CALCULATE ( [Distinct Orders], fact_amazon_sales[b2b] = FALSE () )
```

Classification: `SUPPORTED` source-local mix measure. Limitation: same source
flag limitation as B2B Orders.

### B2B Mix %

```DAX
B2B Mix % =
DIVIDE ( [B2B Orders], [Distinct Orders] )
```

Classification: `SUPPORTED` source-local mix. Limitation: denominator is
distinct Amazon orders in the current context.

### B2C Mix %

```DAX
B2C Mix % =
DIVIDE ( [B2C Orders], [Distinct Orders] )
```

Classification: `SUPPORTED` source-local mix. Limitation: denominator is
distinct Amazon orders in the current context and the source B2B flag is not a
governed customer identifier.

### Category Contribution %

```DAX
Category Contribution % =
DIVIDE (
    [Reported Gross Amount],
    CALCULATE (
        [Reported Gross Amount],
        ALLSELECTED ( dim_category[category] )
    )
)
```

Classification: `SUPPORTED` source-local concentration measure. Limitation:
the denominator respects other slicers and current report selections.

### SKU Contribution %

```DAX
SKU Contribution % =
DIVIDE (
    [Reported Gross Amount],
    CALCULATE (
        [Reported Gross Amount],
        ALLSELECTED ( dim_sku[sku] )
    )
)
```

Classification: `SUPPORTED` source-local concentration measure. Limitation:
Amazon SKU mappings are not cross-source product mappings.

## Pricing proxy measures

### Reported Unit-Price Proxy (Delivered Status Proxy)

```DAX
Reported Unit-Price Proxy =
VAR ValidRows =
    FILTER (
        fact_amazon_sales,
        NOT ISBLANK ( fact_amazon_sales[amount] )
            && fact_amazon_sales[qty] > 0
            && fact_amazon_sales[is_delivered_status_proxy] = TRUE ()
    )
RETURN
    DIVIDE (
        SUMX ( ValidRows, fact_amazon_sales[amount] ),
        SUMX ( ValidRows, fact_amazon_sales[qty] )
    )
```

Classification: `PROXY`. Definition: reported amount divided by positive
quantity where amount is populated within the exact delivered-status proxy.
Limitation: not realised selling price, discount, elasticity, profit, or
margin; delivered status is an analytical convention, not completed sales.

## Status composition proxy measures

### Status Composition %

```DAX
Status Composition % =
DIVIDE (
    [Distinct Orders],
    CALCULATE (
        [Distinct Orders],
        ALLSELECTED ( dim_order_status[status_label] )
    )
)
```

Classification: `PROXY`. Definition: distinct orders in a displayed source
status label divided by the selected status-label denominator. Limitation:
source-status composition is not an official cancellation, return,
fulfilment, delivery, or SLA rate.

### Cancelled Status Proxy Orders

```DAX
Cancelled Status Proxy Orders =
CALCULATE (
    DISTINCTCOUNT ( dim_order_status[order_id] ),
    dim_order_status[has_cancelled_status_proxy] = TRUE ()
)
```

Classification: `PROXY`. Limitation: no approved order-status precedence rule.

### Return-Related Status Proxy Orders

```DAX
Return-Related Status Proxy Orders =
CALCULATE (
    DISTINCTCOUNT ( dim_order_status[order_id] ),
    dim_order_status[has_return_status_proxy] = TRUE ()
)
```

Classification: `PROXY`. Limitation: not a return or refund rate; no returned
quantity or refund amount exists.

### Delivered Status Proxy Orders

```DAX
Delivered Status Proxy Orders =
CALCULATE (
    DISTINCTCOUNT ( dim_order_status[order_id] ),
    dim_order_status[has_delivered_status_proxy] = TRUE ()
)
```

Classification: `PROXY`. Limitation: exact source status is not confirmed
completed delivery and has no event timestamp.

## Separate international measures

### International Reported Gross Amount (Currency Unspecified)

```DAX
International Reported Gross Amount (Currency Unspecified) =
SUM ( fact_international_sales[reported_gross_amount] )
```

Classification: `SUPPORTED` source-local reported field. Limitation: currency
is absent and this measure must never be combined with Amazon amount.

### International Reported Pieces

```DAX
International Reported Pieces =
SUM ( fact_international_sales[pieces] )
```

Classification: `SUPPORTED` source-local pieces measure. Limitation: no order
ID, currency, or cross-source relationship.

## Explicitly do not create

Do not create measures named Profit, Gross Profit, Margin, Net Sales, Refund
Rate, Return Rate, Cancellation Rate, Fulfilment Rate, Delivery Time, SLA,
Customer Count, Inventory Turnover, Forecast, or Predicted Value.
