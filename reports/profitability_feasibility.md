# Phase 8: Profitability Feasibility

## Decision

**PASS WITH WARNINGS — profitability analysis stopped.**

The repository does not contain enough transaction-linked revenue and cost data
to calculate defensible profit, gross profit, gross margin, or contribution
margin. No profitability notebook or profitability findings report is created.

## Feasibility assessment

| Requirement | Evidence in the repository | Feasibility |
|---|---|---|
| Realised selling price | Amazon has a line-level `amount` and `currency` for 121,177 of 128,969 rows. The amount is a reported sales amount, not a validated net-of-refund revenue field. International `gross_amt` has no confirmed currency basis. | Partial |
| Product cost / COGS | Product snapshots contain `tp`, `tp_1`, and `tp_2`, but their business meaning and cost basis are not confirmed. No COGS ledger exists. | No |
| Platform fees | No order-, line-, platform-, or period-linked fee field exists. | No |
| Fulfilment costs | The warehouse file contains four reference-rate rows, with no order/SKU key, date, unit basis, currency, or transaction linkage. | No |
| Shipping costs | No transaction-linked shipping-cost field exists. | No |
| Returns / refunds | Status values provide operational proxies only. No return quantity, refund amount, or refund ledger exists. | No |
| Taxes | No tax fields or tax ledger exists. | No |
| Other expenses | The expense file is a small report containing detail and summary/balance rows, with no reliable sales key, period, or currency. Detail rows total 8,095, but cannot be allocated to transactions. | Partial for reporting only; no for profitability |
| Matching keys and dates | Amazon has `order_id`, `sku`, and `date`; the warehouse and expense sources lack transaction keys and dates. Product snapshot SKUs do not exactly match Amazon SKUs in the available crosswalk checks. | No |

## Quantified evidence

- The Amazon cleaned dataset contains 128,969 line rows and 120,378 distinct
  orders. `amount` and `currency` are populated on 121,177 rows; 7,792 rows
  have no reported amount/currency.
- Amazon `amount` is a line-level reported sales measure. It cannot be treated
  as realised net revenue without validated discount, refund, return, tax, and
  cancellation treatment.
- The May and March product snapshots each contain 1,330 unique SKUs, but the
  available exact-match checks found no Amazon-to-snapshot SKU matches.
- The warehouse comparison contains only four rate-reference rows and no
  transaction key or effective date.
- The expense report includes detail and summary/balance records. Expense
  detail rows total 8,095, while summary rows total 10,000; these rows must not
  be added together and neither total can be allocated to sales.

## Unsupported metrics

The following metrics must remain unsupported:

- profit and gross profit;
- gross margin and contribution margin;
- profit by SKU, category, platform, or other dimension;
- high-revenue/low-margin and low-revenue/high-margin product segments;
- expense-driver attribution;
- profitability concentration;
- validated net revenue after returns, refunds, taxes, and fees.

Reported gross sales may continue to be used within the limitations already
documented in the sales KPI and data dictionary documents. It must not be
described as profit, margin, or net revenue.

## Minimum additional data required

1. An order/line sales ledger with `order_id`, `line_id`, SKU, transaction date,
   currency, quantity, gross amount, discounts, refunds, returns, taxes, and
   shipping charges.
2. A COGS or landed-cost ledger with a governed SKU/line key, effective date,
   currency, unit cost, quantity basis, and a documented cost method.
3. A platform-fee ledger keyed to order/line, platform, date, currency, and fee
   component.
4. A fulfilment and shipping ledger keyed to order/line or shipment, with
   provider, dates, currency, and cost basis.
5. A returns/refunds ledger containing order/line keys, returned quantity,
   refund value, date, and reason.
6. Tax data and a documented treatment for tax-inclusive versus tax-exclusive
   sales.
7. Expense allocation dimensions for period, currency, channel, warehouse,
   or another approved allocation basis.
8. A governed SKU crosswalk linking sales, product, inventory, and cost data.

## Recommended action

Stop Phase 8 at feasibility. Obtain the minimum data above and confirm the
business definitions of `tp`, `tp_1`, and `tp_2` before any profitability
calculation is designed. No cleaned data was changed and no business rule was
silently altered.
