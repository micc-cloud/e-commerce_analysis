# Phase 1 Data Dictionary

This dictionary describes only fields present in the cleaned CSV files. “Likely business meaning” is an interpretation for analysis planning, not a confirmed source-system definition.

## Governance notes

- The Amazon and international raw date strings are month-day-year (`%m-%d-%y`).
  The cleaned international `date` is displayed as `mm/dd/yyyy` and is
  retained only when its month/year agrees with `months`.
- `amount` and `gross_amt` are reported monetary fields. Missing Amazon
  `amount` is preserved; it is not treated as zero or imputed.
- Zero `qty`, zero `amount`, and negative expense values are observations that
  require source/business interpretation. They are not silently removed.
- Amazon is an order-line table without a line identifier. `order_id` is a
  candidate order key only and repeats by design.
- `sku`, `sku_code`, category, style, and size links across files are candidate
  relationships. Exact Amazon-to-product-snapshot SKU match is currently zero.
- `tp`, `tp_1`, and `tp_2` are reference fields with undefined business
  meaning; they must not be treated as COGS or product cost.
- Warehouse and expense tables are report/reference grains without transaction
  keys, reliable dates, or currency. They cannot be allocated to sales.

## `amazon_sale_report_cleaned.csv`

**Grain:** one Amazon sales/order line record. `order_id` repeats across lines and is not a row key.

| Field | Type | Plain-language meaning | Likely business meaning | Limitations | Permitted analytical use |
|---|---|---|---|---|---|
| `order_id` | text | Order reference | Transaction/order identifier | Repeats across lines; no customer ID | Distinct-order counts within this file; line-to-order grouping |
| `date` | text, ISO date | Order date | Sales order date | No timezone or explicit time | Daily/monthly trends |
| `status` | categorical text | Order status | Lifecycle/outcome status | Multiple line statuses may exist within an order | Status mix; carefully defined order-status proxies |
| `fulfilment` | categorical text | Fulfilment type | Amazon or Merchant fulfilment | Not a delivery-time measure | Fulfilment mix |
| `sales_channel` | categorical text | Sales channel | Amazon.in or Non-Amazon | Channel definitions are source labels | Channel split within this file |
| `ship_service_level` | categorical text | Requested service level | Standard/expedited service | Not actual delivery performance | Service-level mix |
| `style` | text | Product style code | Parent/style identifier | Not guaranteed unique across sources | Product/style grouping |
| `sku` | text | Stock-keeping code | Sellable product variant | Cross-file matches are incomplete | SKU-level sales analysis; candidate joins |
| `category` | categorical text | Product category label | Merchandise category | Labels differ from other files | Category mix within source |
| `size` | categorical text | Variant size | Size dimension | Text standardisation may still be needed | Variant and size mix |
| `asin` | text | Amazon catalogue identifier | Amazon product listing ID | Missing/marketplace-specific | Amazon listing grouping |
| `courier_status` | categorical text | Courier state | Dispatch/courier progress | Not a complete delivery timestamp | Operational status mix |
| `qty` | integer | Quantity on line | Units ordered on line | Zero values and cancelled lines exist | Gross line units; status-filtered units with explicit rule |
| `currency` | categorical text | Currency code | INR for populated values | Missing on some rows; no FX field | Currency validation; INR-only aggregation |
| `amount` | decimal | Monetary amount on line | Reported sales amount | Missing values; treatment of cancellations/returns not defined | Gross amount analysis with coverage disclosure |
| `ship_city` | text | Shipping city | Delivery geography | Missing values and spelling variation | Geographic mix, not customer analysis |
| `ship_state` | text | Shipping state | Delivery geography | Missing values and spelling variation | Geographic mix |
| `ship_postal_code` | decimal-like text | Shipping postal code | Delivery location code | Read as text when used; leading zeros risk | Geography after string normalisation |
| `ship_country` | text | Shipping country | Delivery country | Small missing subset | Country mix |
| `promotion_ids` | text | Promotion references | Applied promotion identifiers | No discount amount or promotion dimension | Promotion presence only |
| `b2b` | boolean | Business-order flag | B2B versus consumer flag | No customer/account identifier | B2B mix within Amazon data |
| `fulfilled_by` | categorical text | Fulfilment provider label | Easy Ship/FBA-type provider | Missing on many rows; definitions not supplied | Provider mix with missingness shown |

## `international_sale_report_cleaned.csv`

**Grain:** one retained international sales line. The source’s malformed/non-transaction rows were excluded by the Phase 0 date/month rule. There is no order identifier.

| Field | Type | Plain-language meaning | Likely business meaning | Limitations | Permitted analytical use |
|---|---|---|---|---|---|
| `date` | text, `mm/dd/yyyy` | Sales date | International sales date | No time, currency, or order ID | Date trends |
| `months` | categorical text | Month label | Reporting month | Redundant with date; used to validate month/year | Month grouping and QA |
| `customer` | text | Customer name text | Wholesale/customer label | Not a governed customer ID; spelling/identity risk | Descriptive customer-name grouping only, not customer-360 claims |
| `style` | text | Style code | Product/style identifier | Cross-file meaning not confirmed | Style grouping |
| `sku` | text | SKU code | Product variant identifier | Missing on 11.19%; cross-file matches incomplete | SKU-level sales where populated |
| `size` | categorical text | Size | Variant size | Missing/format variation possible | Size mix |
| `pcs` | decimal | Pieces sold | Units on sales line | Missing values and no return status | Gross pieces with coverage disclosure |
| `rate` | decimal | Unit or line rate as reported | Selling rate | Source definition not provided; currency absent | Rate distribution, not cross-source currency comparison |
| `gross_amt` | decimal | Gross amount | Reported gross sales amount | Currency absent; no discount/return fields | Gross sales within this file only |

## `may_2022_cleaned.csv`

**Grain:** one SKU snapshot row, apparently from May 2022. `sku` is unique in this file. This is not a transaction table and `tp` is not assumed to be cost.

| Field | Type | Plain-language meaning | Likely business meaning | Limitations | Permitted analytical use |
|---|---|---|---|---|---|
| `sku` | text | SKU code | Product variant key | Snapshot-specific; join coverage is incomplete | Product reference join after match QA |
| `style_id` | text | Style identifier | Parent style | Definition not supplied | Style grouping |
| `catalog` | text | Catalogue label | Merchandise catalogue | Source taxonomy | Product segmentation |
| `category` | text | Product category | Merchandise category | Taxonomy differs from Amazon/Sale Report | Product mix |
| `weight` | decimal | Product weight | Unit weight | Missing values; unit not stated | Weight distribution only |
| `tp` | decimal | TP value | Possible trade/transfer price | Definition and cost basis not confirmed | Price reference scenario only; not profit cost |
| `mrp_old` | decimal | Previous MRP | Reference/list price | Snapshot and definition not confirmed | Price comparison |
| `final_mrp_old` | decimal | Final previous MRP | Reference price | Snapshot and definition not confirmed | Price comparison |
| `ajio_mrp` | decimal | AJIO MRP | Channel reference price | Not observed realised sales price | Channel price comparison |
| `amazon_mrp` | decimal | Amazon MRP | Channel reference price | Not observed realised sales price | Channel price comparison |
| `amazon_fba_mrp` | decimal | Amazon FBA MRP | Fulfilment-specific reference price | Not linked to FBA order outcomes | Reference comparison |
| `flipkart_mrp` | decimal | Flipkart MRP | Channel reference price | Not observed realised sales price | Channel price comparison |
| `limeroad_mrp` | decimal | Limeroad MRP | Channel reference price | Not observed realised sales price | Channel price comparison |
| `myntra_mrp` | decimal | Myntra MRP | Channel reference price | Not observed realised sales price | Channel price comparison |
| `paytm_mrp` | decimal | Paytm MRP | Channel reference price | Not observed realised sales price | Channel price comparison |
| `snapdeal_mrp` | decimal | Snapdeal MRP | Channel reference price | Not observed realised sales price | Channel price comparison |

## `p_l_march_2021_cleaned.csv`

**Grain:** one SKU snapshot row, apparently from March 2021. `sku` is unique in this file. This is not a transaction table and `tp_1`/`tp_2` are not assumed to be cost.

| Field | Type | Plain-language meaning | Likely business meaning | Limitations | Permitted analytical use |
|---|---|---|---|---|---|
| `sku` | text | SKU code | Product variant key | Snapshot-specific; join coverage is incomplete | Product reference join after match QA |
| `style_id` | text | Style identifier | Parent style | Definition not supplied | Style grouping |
| `catalog` | text | Catalogue label | Merchandise catalogue | Source taxonomy | Product segmentation |
| `category` | text | Product category | Merchandise category | Taxonomy differs from other files | Product mix |
| `weight` | decimal | Product weight | Unit weight | Missing values; unit not stated | Weight distribution |
| `tp_1` | decimal | First TP field | Possible trade/transfer price | Definition not confirmed | Reference comparison only |
| `tp_2` | decimal | Second TP field | Possible alternate cost/price | Definition not confirmed | Reference comparison only |
| `mrp_old` | decimal | Previous MRP | Reference/list price | Snapshot and definition not confirmed | Price comparison |
| `final_mrp_old` | decimal | Final previous MRP | Reference price | Snapshot and definition not confirmed | Price comparison |
| `ajio_mrp` | decimal | AJIO MRP | Channel reference price | Not realised sales price | Channel price comparison |
| `amazon_mrp` | decimal | Amazon MRP | Channel reference price | Not realised sales price | Channel price comparison |
| `amazon_fba_mrp` | decimal | Amazon FBA MRP | Fulfilment-specific reference price | Not linked to FBA outcomes | Reference comparison |
| `flipkart_mrp` | decimal | Flipkart MRP | Channel reference price | Not realised sales price | Channel price comparison |
| `limeroad_mrp` | decimal | Limeroad MRP | Channel reference price | Not realised sales price | Reference comparison |
| `myntra_mrp` | decimal | Myntra MRP | Channel reference price | Not realised sales price | Reference comparison |
| `paytm_mrp` | decimal | Paytm MRP | Channel reference price | Not realised sales price | Reference comparison |
| `snapdeal_mrp` | decimal | Snapdeal MRP | Channel reference price | Not realised sales price | Reference comparison |

## `sale_report_cleaned.csv`

**Grain:** one inventory SKU/size/colour row, likely an undated stock snapshot. `sku_code` is not unique and is not a reliable one-row-per-SKU key.

| Field | Type | Plain-language meaning | Likely business meaning | Limitations | Permitted analytical use |
|---|---|---|---|---|---|
| `sku_code` | text | Inventory SKU code | Stock item identifier | 48 missing and 68 duplicate rows; not a confirmed key | Inventory grouping with duplicate review |
| `design_no` | text | Design number | Parent design/style | One missing value | Design grouping |
| `stock` | decimal | Stock quantity | Available or reported stock | Snapshot date absent; zero values exist; definition not supplied | Stock snapshot and zero-stock counts |
| `category` | text | Inventory category | Merchandise category | Taxonomy differs from other files | Inventory mix |
| `size` | text | Size | Variant size | Text variation possible | Variant mix |
| `color` | text | Colour | Variant colour | Text variation possible | Colour mix |

## `cloud_warehouse_compersion_chart_cleaned.csv`

**Grain:** one warehouse cost-head row. It is a reference table, not a transaction table.

| Field | Type | Plain-language meaning | Likely business meaning | Limitations | Permitted analytical use |
|---|---|---|---|---|---|
| `cost_head` | text | Warehouse cost category | Inbound/outbound/RTO-related cost head | Small report extract; one provider value may be missing | Reference cost comparison |
| `shiprocket_price_per_unit` | decimal | Shiprocket per-unit price | Provider rate | Unit and period not stated | Provider-rate comparison |
| `increff_price_per_unit` | decimal | Increff per-unit price | Provider rate | One missing value; unit and period not stated | Provider-rate comparison |

## `expense_iigf_cleaned.csv`

**Grain:** one receipt/expense report record, including detail and summary rows. It is not an order-cost ledger.

| Field | Type | Plain-language meaning | Likely business meaning | Limitations | Permitted analytical use |
|---|---|---|---|---|---|
| `transaction_type` | text | Receipt or expense side | Cash-flow direction/report section | Source spelling and scope are report-level | Expense/receipt listing |
| `record_type` | text | Detail or summary flag | Whether row is a detail or total/balance | Summary rows must not be added to detail rows | Detail versus summary separation |
| `particular` | text | Description or date-like label | Expense description or receipt date | Mixed semantic content | Controlled listing after filtering |
| `amount` | integer | Reported amount | Receipt/expense amount | One negative amount; currency, period, and accounting basis absent | Expense totals only after excluding summary rows and defining scope |

## Cross-file relationship summary

- `amazon_sale_report_cleaned.sku` -> product `sku` is a candidate many-to-one relationship, but 7,195 Amazon SKU values do not match the product snapshots.
- `international_sale_report_cleaned.sku` -> product `sku` is a candidate many-to-one relationship, but 4,590 values do not match the product snapshots and 1,379 international rows have missing SKU.
- `sale_report_cleaned.sku_code` -> product `sku` is not currently a reliable join: 9,170 values do not match and `sku_code` itself is non-unique/missing.
- There is no confirmed relationship from warehouse costs or the expense report to sales lines.
