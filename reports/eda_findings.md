# E-commerce EDA Findings

## Key findings

- Amazon contains 128,969 order lines and 120,378 distinct orders from 2022-03-31 to 2022-06-29.
- Amazon reported amount totals 78,590,043.30; 94.0% of lines have amount populated and INR is the only populated currency.
- International sales contain 12,322 retained lines and reported gross amount of 10,834,927.19; currency is not supplied, so this remains a separate scope.
- Amazon has 116,646 reported units, including 12,804 zero-quantity lines needing status/business review.
- SKU coverage is 100.0% for Amazon and 88.8% for international sales; cross-source matches are incomplete.
- The stock snapshot contains 581 zero-stock rows, but no snapshot date, so turnover and stockout-over-time KPIs remain unsupported.

## Limitations

- Amazon and international scopes remain separate because currency and order-grain definitions differ.
- Status labels are descriptive proxies; true cancellation/return rates require an approved order-level rule.
- Profit, gross margin, customer-360, true net sales, and inventory turnover are not calculated.
- Outliers are retained and flagged for follow-up; no causal conclusion is made.
