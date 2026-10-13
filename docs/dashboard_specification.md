# Power BI Dashboard Specification

## Design principles

Build a recruiter-facing portfolio dashboard with four pages, a white
background, restrained blue/teal accents, compact KPI cards, and clear source
labels. Use the exact terms **Reported Gross Amount**, **Reported Unit-Price
Proxy**, and **Status Composition Proxy** in titles and subtitles. Every
monetary visual must show an Amount Coverage % tooltip or nearby card.

Global Amazon slicers: date, month, category, SKU, sales channel, fulfilment,
ship state, and B2B. Keep international visuals on their own page section and
do not apply Amazon slicers to them.

## Page 1: Executive Overview

| Visual type / title | Source and fields | Slicers / filters | Sorting / tooltip / drill-through | Required measure | Business question |
|---|---|---|---|---|---|
| Card: `Reported Gross Amount (INR)` | `fact_amazon_sales`; no axis | Global Amazon slicers; `amount` is blank-safe | Tooltip: Amount Coverage % and date range | Reported Gross Amount; Amount Coverage % | What reported monetary scale is visible, and how complete is it? |
| Card: `Distinct Amazon Orders` | `fact_amazon_sales[order_id]` | Global Amazon slicers | Tooltip: Gross Units | Distinct Orders | How many distinct orders are represented? |
| Card: `Gross Units` | `fact_amazon_sales[qty]` | Global Amazon slicers | Tooltip: zero-quantity row count if added as a column summary | Gross Units | How many source-reported units are present? |
| Card: `Amount Coverage %` | `fact_amazon_sales[amount_present]` | Global Amazon slicers | Conditional colour below 95%; tooltip: row count | Amount Coverage % | Can the displayed amount be interpreted with adequate coverage? |
| Line chart: `Reported Gross Amount by Observed Date` | X: `dim_date[date]`; Y: Reported Gross Amount | Global Amazon slicers | Ascending date; tooltip: Amount Coverage %, Is Partial Period | Reported Gross Amount | How does reported amount vary across observed dates? |
| Bar chart: `Category Contribution of Reported Gross Amount` | Y: `dim_category[category]`; X: Reported Gross Amount | Global Amazon slicers | Descending amount; tooltip: Category Contribution %, Amount Coverage %; drill-through to Product page | Reported Gross Amount; Category Contribution % | Which source-local categories contribute reported amount? |
| 100% stacked bar: `Status Composition Proxy` | Y: `dim_order_status[status_label]`; X: Distinct Orders | Date/category slicers; exclude blank labels | Descending orders; tooltip: Status Composition %; no official rate label | Distinct Orders; Status Composition % | What source-status composition is observed? |

Page warning text: `Reported Gross Amount is not net sales. Status values are
analytical composition proxies. March and June are partial observed periods.`

## Page 2: Sales Performance

| Visual type / title | Source and fields | Slicers / filters | Sorting / tooltip / drill-through | Required measure | Business question |
|---|---|---|---|---|---|
| Line and clustered column chart: `Reported Gross Amount and Gross Units by Month` | X: `dim_date[month_start]`; column Y: Gross Units; line Y: Reported Gross Amount | Global Amazon slicers; show `is_partial_period` in tooltip | Ascending month; March and June labelled partial; tooltip: Amount Coverage % | Reported Gross Amount; Gross Units; Amount Coverage % | How do reported amount and units change by observed month? |
| Bar chart: `Distinct Orders by Sales Channel` | Y: `fact_amazon_sales[sales_channel]`; X: Distinct Orders | Date/category slicers | Descending orders; flag Non-Amazon as small sample in tooltip | Distinct Orders | What source channel mix is observed? |
| Treemap: `B2B/B2C Reported Gross Amount Mix` | Group: `fact_amazon_sales[b2b]`; Values: Reported Gross Amount | Global Amazon slicers | Descending amount; tooltip: B2B Mix %, Amount Coverage % | Reported Gross Amount; B2B Mix % | How is reported amount split by the source B2B flag? |
| Filled map or bar chart: `Reported Gross Amount by Ship State` | Location: `fact_amazon_sales[ship_state]`; Values: Reported Gross Amount | Global Amazon slicers; exclude blank state | Descending amount for bar fallback; tooltip: Distinct Orders, Amount Coverage % | Reported Gross Amount; Distinct Orders | Which source-local shipping states contribute reported amount? |
| Table: `International Reported Gross Amount and Pieces` | `fact_international_sales[months]`, `reported_gross_amount`, `pieces` | International date/month slicer only | Sort by month; title must include `Currency Unspecified`; no drill-through to Amazon | International Reported Gross Amount (Currency Unspecified); International Reported Pieces | What separate international reported activity is present? |

Page warning text: `Amazon and international monetary values are not combined.
International currency is unspecified. March and June Amazon periods are
partial and should not be compared as complete months.`

## Page 3: Product & Pricing

| Visual type / title | Source and fields | Slicers / filters | Sorting / tooltip / drill-through | Required measure | Business question |
|---|---|---|---|---|---|
| Bar chart: `Top 10 Source-Local SKUs by Reported Gross Amount` | Y: `dim_sku[sku]`; X: Reported Gross Amount | Global Amazon slicers; Top N = 10 | Descending amount; tooltip: SKU Contribution %, Gross Units, Amount Coverage %; drill-through to SKU detail | Reported Gross Amount; SKU Contribution %; Gross Units | Which source-local SKUs contribute the most reported amount? |
| Bar chart: `Category Reported Unit-Price Proxy (Delivered Status Proxy)` | Y: `dim_category[category]`; X: Reported Unit-Price Proxy | Delivered status proxy, amount populated, and qty > 0 | Descending proxy; tooltip: Gross Units, Amount Coverage %; no causal annotation | Reported Unit-Price Proxy (Delivered Status Proxy) | How does the validated-scope reported unit-price proxy vary by category? |
| Column chart: `Reported Unit-Price Proxy Bands` | X: `fact_amazon_sales[reported_unit_price_band]`; Y: Reported Gross Amount | Delivered status proxy, amount populated, and qty > 0 | Fixed order `[0,500)`, `[500,1000)`, `[1000,2000)`, `[2000,inf)`; tooltip: Amount Coverage % | Reported Gross Amount; Gross Units | Where does validated-scope proxy volume fall across analytical bands? |
| Scatter chart: `SKU Proxy Variation Review` | X: Gross Units; Y: Reported Unit-Price Proxy; Details: `dim_sku[sku]` | Delivered status proxy and valid proxy rows; require at least 5 valid lines in tooltip/filter | Descending by Y; tooltip: SKU, Amount Coverage %, line count; drill-through to SKU detail | Reported Unit-Price Proxy; Gross Units | Which SKUs merit review for observed proxy variation? |
| Matrix: `SKU Product Detail` | Rows: SKU, style, category, size; Values: Reported Gross Amount, Gross Units, Distinct Orders, SKU Contribution % | SKU/category/date slicers | Sort amount descending; drill-through target from category/SKU charts | Reported Gross Amount; Gross Units; Distinct Orders; SKU Contribution % | What source-local product detail supports the contribution view? |
| Card: `B2B Mix %` | `fact_amazon_sales[b2b]` | Global Amazon slicers | Tooltip: B2B Orders and B2C Orders | B2B Mix % | What share of selected distinct orders carries the B2B flag? |

Page warning text: `Reported Unit-Price Proxy = amount / qty only where amount is
present and qty > 0. It is not realised selling price. No MRP, discount,
elasticity, profit, or margin analysis is supported.`

## Page 4: Operations

| Visual type / title | Source and fields | Slicers / filters | Sorting / tooltip / drill-through | Required measure | Business question |
|---|---|---|---|---|---|
| Bar chart: `Status Composition Proxy by Source Label` | Y: `dim_order_status[status_label]`; X: Distinct Orders | Date/category/SKU slicers; show mixed label if present | Descending orders; tooltip: Status Composition %; title must include Proxy | Distinct Orders; Status Composition % | What order-status composition is recorded? |
| Matrix: `Status Composition Proxy by Month` | Rows: `dim_date[month_label]`; columns: `dim_order_status[status_label]`; values: Distinct Orders | Date slicer; show partial-period flag in tooltip | Month ascending; no rate wording | Distinct Orders | Does status composition differ across observed months? |
| Bar chart: `Status Composition Proxy by Ship State` | Y: `fact_amazon_sales[ship_state]`; X: Distinct Orders | Minimum 100 distinct orders; exclude blank state | Descending orders; tooltip: Status Composition % and sample size | Distinct Orders; Status Composition % | Which geographic groups need operational data review? |
| Stacked bar: `B2B/B2C Status Composition Proxy` | Y: `fact_amazon_sales[b2b]`; Legend: `dim_order_status[status_label]`; X: Distinct Orders | Global Amazon slicers | Sort B2C then B2B; tooltip: distinct orders | Distinct Orders | Does source-status composition differ by B2B flag? |
| Table: `Mixed-Status Order Governance Check` | Rows: `dim_order_status[order_id]`, `status_values`; values: status_count, mixed_status_flag | Filter `mixed_status_flag = TRUE` when present | Sort by order ID; drill-through to line facts | No rate measure; use status metadata | Are any orders unresolved because line statuses conflict? |
| Card: `Fulfilment Comparison Not Available` | `fact_amazon_sales[fulfilment]` distinct count | None | Static note; do not create a ranking | None | Is a fulfilment comparison supported? |

Page warning text: `These are source-status composition proxies, not official
cancellation, return, fulfilment, delivery, or SLA rates. No delivery-time,
courier-speed, warehouse, or expense attribution is supported. Mixed-status
orders require an approved precedence rule.`

## Interactions and navigation

- Add page navigation buttons for the four pages in the same top-right location.
- Sync only Amazon slicers across Pages 1–4; do not sync them to the separate
  international table visual.
- Selecting a category filters SKU, pricing, and status visuals on the current
  page through the documented dimensions.
- Selecting a status label filters the status-focused visuals; do not interpret
  the selection as a lifecycle outcome.
- Configure drill-through on `sku` and `category` to the Product Detail matrix;
  include SKU, category, date, Amount Coverage %, and the proxy warning in the
  drill-through filter pane.
- Turn off bidirectional relationships and unnecessary visual interactions
  that could make a visual appear to filter the international fact.
- Add a persistent footer on every page: `Source-local descriptive analysis;
  proxy labels and limitations apply.`
