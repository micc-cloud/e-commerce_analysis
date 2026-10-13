# Phase 8: Profitability Feasibility Recheck

## Decision

**PASS WITH WARNINGS — PROFITABILITY BLOCKED**

The Phase 0–7 evidence still does not support defensible transaction-level
profitability analysis. No profitability notebook or profitability findings
report is created. The phase stops at feasibility.

## Required-data assessment

| Requirement | Observed evidence | Feasibility |
|---|---|---|
| Validated realised selling price | Amazon has line-level `amount` and `currency` on 121,177 of 128,969 rows; `amount` is reported gross amount, not validated net revenue. | Partial |
| COGS / product cost | May has `tp`; March has `tp_1` and `tp_2`. Their meanings and cost basis are undefined, and exact Amazon-to-snapshot SKU matching is 0. | No |
| Platform fees | No transaction-, line-, platform-, or period-linked fee fields exist. | No |
| Fulfilment cost | Warehouse file has 4 reference-rate rows only; no order/SKU/date/unit-basis/currency key. | No |
| Shipping cost | No transaction-linked shipping-cost field exists. | No |
| Taxes | No tax field or tax ledger exists. | No |
| Refund amounts | No refund amount field or refund ledger exists. | No |
| Return quantities | Status labels only; no returned quantity or return-event ledger exists. | No |
| Currency | Amazon populated currency is INR; international currency is absent; snapshot and expense currency are not defined. | No for consolidated profitability |
| Reliable transaction/SKU/date keys | Amazon has `order_id`, `sku`, and `date`; warehouse and expense sources have no reliable sales key/date, and product SKU formats do not match Amazon. | No |

## Warehouse and expense linkage

### Warehouse reference rates

`cloud_warehouse_compersion_chart_cleaned.csv` contains four cost-head rows and
provider reference prices. It has no transaction ID, order ID, SKU, effective
date, currency, or confirmed allocation unit. These rates cannot be allocated
to orders, SKUs, categories, platforms, or periods.

### Expense report

`expense_iigf_cleaned.csv` contains 21 rows with `detail` and `summary`
`record_type` values. Detail and summary/balance rows are different grains and
must not be added together. The report has no sales key, period key that links
to orders, currency, or approved allocation basis. It cannot be used to assign
expenses to transactions.

## Controls against misinterpretation

- `tp`, `tp_1`, and `tp_2` remain undefined reference fields; they are not
  treated as COGS, cost, or margin inputs.
- MRP and marketplace reference-price fields are not costs.
- Amazon `amount` is not treated as net revenue, profit, or margin.
- Warehouse reference rates are not joined or allocated to sales.
- Expense detail and summary rows are not combined or double-counted.
- Status proxies are not used as validated returns, refunds, or completed-sales
  adjustments.
- No cross-source currency aggregation is performed.

## Unsupported metrics

The following remain blocked:

- profit and gross profit;
- gross margin and contribution margin;
- ROI;
- profitability by SKU, category, or platform;
- high-revenue/low-margin and low-revenue/high-margin segments;
- expense-driver attribution and profitability concentration;
- net revenue after discounts, cancellations, returns, refunds, taxes, and
  fees.

## Minimum additional data to unlock analysis

1. A transaction/line ledger with `order_id`, `line_id`, governed SKU, date,
   currency, quantity, gross amount, discount, tax, refund, return, and
   shipping fields.
2. A validated COGS or landed-cost ledger with line/SKU key, effective date,
   currency, unit-cost basis, and documented costing method.
3. A platform-fee ledger keyed to order/line, platform, date, currency, and fee
   component.
4. A fulfilment/shipping ledger keyed to order/line or shipment, with dates,
   provider, currency, and cost basis.
5. A returns/refunds ledger with order/line key, returned quantity, refund
   value, date, and reason.
6. Tax definitions and tax-inclusive/tax-exclusive treatment.
7. An approved expense-allocation basis by period, currency, channel,
   warehouse, or another documented dimension.
8. A governed SKU crosswalk across sales, product, inventory, and cost data.

## Stop decision

Do not create a profitability notebook until the required data and definitions
are supplied, validated, and approved. No source or cleaned file was changed.
