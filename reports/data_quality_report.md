# E-Commerce Data Quality & Cleaning Report

## Cleaning Rules Applied

- Preserved raw files under `data/raw` and wrote cleaned files under `data/cleaned`.
- Standardized column names to lowercase snake_case.
- Removed generated index columns and fully empty columns.
- Trimmed whitespace, normalized blank-like values to missing, and removed exact duplicate rows.
- Converted numeric amount, price, quantity, rate, MRP, stock, and weight fields to numeric values where safe.
- Converted date fields to ISO `YYYY-MM-DD` where safe.
- Treated SKU, ASIN, order IDs, codes, and postal codes as text identifiers.
- Reshaped special report-style CSVs into analysis-ready tables.

## File-Level Summary

| File | Raw Rows | Cleaned Rows | Raw Columns | Cleaned Columns | Duplicate Rows Removed | Key Notes |
|---|---:|---:|---:|---:|---:|---|
| Amazon Sale Report.csv | 128,975 | 128,969 | 24 | 22 | 6 | Dropped generated index column. Dropped parser artifact column `unnamed_22`. Removed 6 exact duplicate rows. |
| Cloud Warehouse Compersion Chart.csv | 50 | 4 | 4 | 3 | 0 | Promoted embedded first row to semantic column names. Converted rupee-denominated per-unit prices to numeric values. Removed narrative section headings without comparable price values. |
| Expense IIGF.csv | 17 | 21 | 5 | 4 | 0 | Reshaped two side-by-side receipt and expense sections into one auditable long table. Flagged totals, pending amount, and unlabelled balance rows as summary records. Kept original spelling in source notes; standardized output column names. |
| International sale Report.csv | 37,432 | 24,541 | 10 | 9 | 12,891 | Dropped generated index column. Removed 12,891 exact duplicate rows. |
| May-2022.csv | 1,330 | 1,330 | 17 | 16 | 0 | Dropped generated index column. |
| P  L March 2021.csv | 1,330 | 1,330 | 18 | 17 | 0 | Dropped generated index column. |
| Sale Report.csv | 9,271 | 9,233 | 7 | 6 | 38 | Dropped generated index column. Removed 38 exact duplicate rows. |

## Missing Value Highlights

### Amazon Sale Report.csv
- `fulfilled_by`: 89,692 missing (69.55%).
- `promotion_ids`: 49,150 missing (38.11%).
- `currency`: 7,792 missing (6.04%).
- `amount`: 7,792 missing (6.04%).
- `courier_status`: 6,872 missing (5.33%).
- `ship_country`: 33 missing (0.03%).
- `ship_postal_code`: 33 missing (0.03%).
- `ship_state`: 33 missing (0.03%).
- `ship_city`: 33 missing (0.03%).

### Cloud Warehouse Compersion Chart.csv
- `increff_price_per_unit`: 1 missing (25.0%).

### Expense IIGF.csv
- No missing values after cleaning.
- Negative numeric values detected: `{"amount": 1}`.

### International sale Report.csv
- `sku`: 2,425 missing (9.88%).
- `pcs`: 1,041 missing (4.24%).
- `rate`: 1,041 missing (4.24%).
- `gross_amt`: 1,041 missing (4.24%).
- `customer`: 1,040 missing (4.24%).
- `style`: 1,040 missing (4.24%).
- `size`: 1,040 missing (4.24%).
- `months`: 25 missing (0.1%).
- `date`: 1 missing (0.0%).

### May-2022.csv
- `weight`: 73 missing (5.49%).
- `mrp_old`: 37 missing (2.78%).
- `final_mrp_old`: 37 missing (2.78%).
- `ajio_mrp`: 37 missing (2.78%).
- `amazon_mrp`: 37 missing (2.78%).
- `amazon_fba_mrp`: 37 missing (2.78%).
- `flipkart_mrp`: 37 missing (2.78%).
- `limeroad_mrp`: 37 missing (2.78%).
- `paytm_mrp`: 37 missing (2.78%).
- `snapdeal_mrp`: 37 missing (2.78%).

### P  L March 2021.csv
- `weight`: 73 missing (5.49%).
- `final_mrp_old`: 37 missing (2.78%).
- `ajio_mrp`: 37 missing (2.78%).
- `paytm_mrp`: 37 missing (2.78%).
- `limeroad_mrp`: 37 missing (2.78%).
- `flipkart_mrp`: 37 missing (2.78%).
- `amazon_fba_mrp`: 37 missing (2.78%).
- `amazon_mrp`: 37 missing (2.78%).
- `snapdeal_mrp`: 37 missing (2.78%).
- `mrp_old`: 37 missing (2.78%).

### Sale Report.csv
- `sku_code`: 48 missing (0.52%).
- `category`: 10 missing (0.11%).
- `color`: 10 missing (0.11%).
- `design_no`: 1 missing (0.01%).
- `stock`: 1 missing (0.01%).
- `size`: 1 missing (0.01%).
