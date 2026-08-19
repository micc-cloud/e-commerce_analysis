# Phase 0: Repository and Cleaned Data Audit

**Final status: PASS WITH WARNINGS**

## Scope

- Audited all expected files under `data/cleaned`.
- Used `scripts/clean_ecommerce_data.py` as the reproducibility source.
- Raw source files were preserved; the international cleaned output was regenerated with the confirmed date/month correction.

## File Inventory

| File | Rows | Columns | Memory | Date range |
|---|---:|---:|---:|---|
| `amazon_sale_report_cleaned.csv` | 128,969 | 22 | 185.24 MB | 2022-03-31T00:00:00 to 2022-06-29T00:00:00 |
| `cloud_warehouse_compersion_chart_cleaned.csv` | 4 | 3 | 0.00 MB | No date field |
| `expense_iigf_cleaned.csv` | 21 | 4 | 0.00 MB | No date field |
| `international_sale_report_cleaned.csv` | 12,322 | 9 | 4.90 MB | 2021-06-05T00:00:00 to 2022-05-11T00:00:00 |
| `may_2022_cleaned.csv` | 1,330 | 16 | 0.45 MB | No date field |
| `p_l_march_2021_cleaned.csv` | 1,330 | 17 | 0.46 MB | No date field |
| `sale_report_cleaned.csv` | 9,233 | 6 | 2.86 MB | No date field |

## Schema, Types, and Validation Findings

### `amazon_sale_report_cleaned.csv`

- Columns: `order_id, date, status, fulfilment, sales_channel, ship_service_level, style, sku, category, size, asin, courier_status, qty, currency, amount, ship_city, ship_state, ship_postal_code, ship_country, promotion_ids, b2b, fulfilled_by`
- Dtypes: `{"amount": "float64", "asin": "object", "b2b": "bool", "category": "object", "courier_status": "object", "currency": "object", "date": "object", "fulfilled_by": "object", "fulfilment": "object", "order_id": "object", "promotion_ids": "object", "qty": "int64", "sales_channel": "object", "ship_city": "object", "ship_country": "object", "ship_postal_code": "float64", "ship_service_level": "object", "ship_state": "object", "size": "object", "sku": "object", "status": "object", "style": "object"}`
- Exact duplicate rows: **0**
- Candidate key `order_id`: 15,431 duplicate rows; 0 rows with null key parts.
- Candidate key `order_id+sku+size`: 2 duplicate rows; 0 rows with null key parts.
- Numeric checks: amount: {'nonblank': 121177, 'non_numeric_nonblank': 0, 'negative': 0, 'zero': 2343}; qty: {'nonblank': 128969, 'non_numeric_nonblank': 0, 'negative': 0, 'zero': 12804}
- Leading/trailing whitespace: none detected.

### `cloud_warehouse_compersion_chart_cleaned.csv`

- Columns: `cost_head, shiprocket_price_per_unit, increff_price_per_unit`
- Dtypes: `{"cost_head": "object", "increff_price_per_unit": "float64", "shiprocket_price_per_unit": "float64"}`
- Exact duplicate rows: **0**
- Candidate key `cost_head`: 0 duplicate rows; 0 rows with null key parts.
- Numeric checks: No non-numeric values, negative values, or zero values detected in audited numeric fields.
- Leading/trailing whitespace: none detected.

### `expense_iigf_cleaned.csv`

- Columns: `transaction_type, record_type, particular, amount`
- Dtypes: `{"amount": "int64", "particular": "object", "record_type": "object", "transaction_type": "object"}`
- Exact duplicate rows: **0**
- Candidate key `transaction_type+record_type+particular+amount`: 0 duplicate rows; 0 rows with null key parts.
- Numeric checks: amount: {'nonblank': 21, 'non_numeric_nonblank': 0, 'negative': 1, 'zero': 0}
- Leading/trailing whitespace: none detected.

### `international_sale_report_cleaned.csv`

- Columns: `date, months, customer, style, sku, size, pcs, rate, gross_amt`
- Dtypes: `{"customer": "object", "date": "object", "gross_amt": "float64", "months": "object", "pcs": "float64", "rate": "float64", "size": "object", "sku": "object", "style": "object"}`
- Exact duplicate rows: **0**
- Candidate key `date+customer+sku+size+pcs+rate+gross_amt`: 479 duplicate rows; 1,379 rows with null key parts.
- Numeric checks: No non-numeric values, negative values, or zero values detected in audited numeric fields.
- Leading/trailing whitespace: none detected.

### `may_2022_cleaned.csv`

- Columns: `sku, style_id, catalog, category, weight, tp, mrp_old, final_mrp_old, ajio_mrp, amazon_mrp, amazon_fba_mrp, flipkart_mrp, limeroad_mrp, myntra_mrp, paytm_mrp, snapdeal_mrp`
- Dtypes: `{"ajio_mrp": "float64", "amazon_fba_mrp": "float64", "amazon_mrp": "float64", "catalog": "object", "category": "object", "final_mrp_old": "float64", "flipkart_mrp": "float64", "limeroad_mrp": "float64", "mrp_old": "float64", "myntra_mrp": "float64", "paytm_mrp": "float64", "sku": "object", "snapdeal_mrp": "float64", "style_id": "object", "tp": "float64", "weight": "float64"}`
- Exact duplicate rows: **0**
- Candidate key `sku`: 0 duplicate rows; 0 rows with null key parts.
- Numeric checks: No non-numeric values, negative values, or zero values detected in audited numeric fields.
- Leading/trailing whitespace: none detected.

### `p_l_march_2021_cleaned.csv`

- Columns: `sku, style_id, catalog, category, weight, tp_1, tp_2, mrp_old, final_mrp_old, ajio_mrp, amazon_mrp, amazon_fba_mrp, flipkart_mrp, limeroad_mrp, myntra_mrp, paytm_mrp, snapdeal_mrp`
- Dtypes: `{"ajio_mrp": "float64", "amazon_fba_mrp": "float64", "amazon_mrp": "float64", "catalog": "object", "category": "object", "final_mrp_old": "float64", "flipkart_mrp": "float64", "limeroad_mrp": "float64", "mrp_old": "float64", "myntra_mrp": "float64", "paytm_mrp": "float64", "sku": "object", "snapdeal_mrp": "float64", "style_id": "object", "tp_1": "float64", "tp_2": "float64", "weight": "float64"}`
- Exact duplicate rows: **0**
- Candidate key `sku`: 0 duplicate rows; 0 rows with null key parts.
- Numeric checks: No non-numeric values, negative values, or zero values detected in audited numeric fields.
- Leading/trailing whitespace: none detected.

### `sale_report_cleaned.csv`

- Columns: `sku_code, design_no, stock, category, size, color`
- Dtypes: `{"category": "object", "color": "object", "design_no": "object", "size": "object", "sku_code": "object", "stock": "float64"}`
- Exact duplicate rows: **0**
- Candidate key `sku_code`: 68 duplicate rows; 48 rows with null key parts.
- Numeric checks: stock: {'nonblank': 9232, 'non_numeric_nonblank': 0, 'negative': 0, 'zero': 581}
- Leading/trailing whitespace: none detected.

## Reproducibility

| Cleaned file | Result | Detail |
|---|---|---|
| `amazon_sale_report_cleaned.csv` | PASS | Serialized output matches the cleaner output. |
| `cloud_warehouse_compersion_chart_cleaned.csv` | PASS | Serialized output matches the cleaner output. |
| `expense_iigf_cleaned.csv` | PASS | Serialized output matches the cleaner output. |
| `international_sale_report_cleaned.csv` | PASS | Serialized output matches the cleaner output. |
| `may_2022_cleaned.csv` | PASS | Serialized output matches the cleaner output. |
| `p_l_march_2021_cleaned.csv` | PASS | Serialized output matches the cleaner output. |
| `sale_report_cleaned.csv` | PASS | Serialized output matches the cleaner output. |

## Candidate Relationships and Merge Risk

The product tables expose `sku` and the sales tables expose `sku`/`sku_code`; these are plausible SKU links, not confirmed foreign keys. Parent uniqueness must be validated before treating any merge as many-to-one.

| Child | Parent | Unmatched child values |
|---|---|---:|
| `amazon_sale_report_cleaned.csv.sku` | `may_2022_cleaned.csv.sku` | 7,195 |
| `amazon_sale_report_cleaned.csv.sku` | `p_l_march_2021_cleaned.csv.sku` | 7,195 |
| `international_sale_report_cleaned.csv.sku` | `may_2022_cleaned.csv.sku` | 4,590 |
| `international_sale_report_cleaned.csv.sku` | `p_l_march_2021_cleaned.csv.sku` | 4,590 |
| `sale_report_cleaned.csv.sku_code` | `may_2022_cleaned.csv.sku` | 9,170 |
| `sale_report_cleaned.csv.sku_code` | `p_l_march_2021_cleaned.csv.sku` | 9,170 |

## Decision

**PASS WITH WARNINGS.** The datasets are suitable for exploratory analysis with documented caveats. The main risks are missing identifiers/amounts, non-unique transaction-level keys, and SKU values that do not match the product tables. Revenue and expense amounts must not be interpreted as profit without validated cost and scope definitions.

## Limitations and Unresolved Issues

- The source files do not provide a confirmed data dictionary or business-approved primary keys.
- `international_sale_report_cleaned.csv` now has 0 invalid nonblank dates. Rows with parseable month-day-year dates whose month/year agreed with `months` were formatted as `mm/dd/yyyy`; 25,110 source rows were excluded from the cleaned transaction table and remain traceable to the raw source.
- Date fields in some source reports use ambiguous day-month formatting; date ranges are parseability checks, not business-date certification.
- The expense and warehouse files are report extracts with summary rows and should not be joined to order lines without explicit grain rules.
- The date correction was applied with a reproducible rule; future corrections require business-owner confirmation and before/after row-count reconciliation.
