# Power BI Desktop Build Guide

This guide creates the dashboard manually from the prepared CSV package. It
does not require or create a `.pbix` file in this repository.

## 1. Prepare the files

1. Open Power BI Desktop.
2. Select **Get data > Text/CSV**.
3. Import each CSV in `data/processed/dashboard/`:
   `fact_amazon_sales.csv`, `dim_date.csv`, `dim_category.csv`, `dim_sku.csv`,
   `dim_order_status.csv`, and `fact_international_sales.csv`.
4. In Power Query, set dates to Date, keys/IDs to Text or Whole number as
   documented in `docs/power_bi_model.md`, and numeric fields to Decimal number
   or Whole number.
5. Do not merge the Amazon and international queries. Do not import product
   snapshots, stock, warehouse, or expense tables into this dashboard model.
6. Apply **Close & Apply**.

## 2. Create the model

In Model view, create exactly these four one-to-many, single-direction
relationships:

- `dim_date[date_key]` -> `fact_amazon_sales[date_key]`
- `dim_category[category_key]` -> `fact_amazon_sales[category]`
- `dim_sku[sku_key]` -> `fact_amazon_sales[sku]`
- `dim_order_status[order_id]` -> `fact_amazon_sales[order_id]`

Confirm the dimension-side key icon appears and no relationship is
many-to-many or bidirectional. Keep `fact_international_sales` disconnected.

## 3. Add measures

Create the measures in `docs/dax_measures.md` under the relevant table. At
minimum add Reported Gross Amount, Amount Coverage %, Distinct Orders, Gross
Units, B2B/B2C measures, Category Contribution %, SKU Contribution %, Reported
Unit-Price Proxy, Status Composition %, and the three status-proxy order
measures.

Format amount measures as INR with two decimals, counts as whole numbers,
coverage/mix/contribution measures as percentages, and the unit-price proxy as
INR with two decimals. Do not use the word revenue for Reported Gross Amount.

## 4. Create report pages

Create four pages in this order:

1. **Executive Overview**: four KPI cards across the top, date trend in the
   middle, category contribution and status composition below.
2. **Sales Performance**: monthly amount/units trend, channel mix, B2B/B2C
   mix, state contribution, and a separate international table.
3. **Product & Pricing**: top SKU, category proxy comparison, price bands,
   SKU proxy variation, product matrix, and B2B mix.
4. **Operations**: status composition, monthly status matrix, state status
   review, B2B/B2C status mix, mixed-status governance table, and a static
   fulfilment limitation note.

Use the complete visual-by-visual field specification in
`docs/dashboard_specification.md`.

## 5. Add slicers and warnings

For Amazon pages, add slicers for date, month, category, SKU, sales channel,
ship state, and B2B. Keep slicers compact in a left rail or top strip. Add a
partial-period warning on any visual using March or June 2022:

`March and June are partial observed periods; do not compare them as complete
months.`

Add these persistent labels:

- `Reported Gross Amount: not net sales`
- `Reported Unit-Price Proxy: delivered-status proxy rows where amount / qty is valid (amount is present and qty > 0)`
- `Status Composition Proxy: not an official cancellation, return, fulfilment, delivery, or SLA rate`
- `International currency unspecified; do not combine with Amazon INR`

## 6. Configure interactions

1. Use **Format > Edit interactions** so category selections filter the Amazon
   product and status visuals on the same page.
2. Prevent Amazon selections from filtering the international table.
3. Keep status selections descriptive; do not turn them into lifecycle or rate
   interpretations.
4. Add drill-through fields `sku` and `category` to a Product Detail page or
   use the Product & Pricing matrix as the drill-through target.
5. Add page navigator buttons to the top-right of all four pages.

## 7. Recruiter-facing presentation checklist

- Use no more than four pages.
- Keep titles business-readable and include `Proxy` when a measure is a proxy.
- Show Amount Coverage % beside every monetary visual.
- Use consistent number formats and avoid excessive decimals.
- Keep legends short and sort bars by the displayed measure.
- Do not show profit, margin, net sales, customer KPIs, inventory turnover,
  forecasts, predictive outputs, official cancellation/return rates, SLA, or
  delivery time.
- Do not claim that a price difference caused a volume difference.

## 8. Final manual checks

Before presenting the report, verify:

- Amazon Reported Gross Amount equals the validated source total when no
  slicers are active: 78,590,043.30.
- Amazon Distinct Orders equals 120,378.
- Amazon Gross Units equals 116,646.
- Amount Coverage % equals 93.96%.
- Delivered-status proxy sensitivity, if shown, reconciles to 26,566 orders
  and is labelled as a proxy.
- No international amount is included in Amazon cards or contribution charts.
- The relationship diagram contains no cross-source SKU or cost relationship.
- Mixed-status orders show `MIXED_STATUS_REQUIRES_RULE` if any future data
  contains them.
