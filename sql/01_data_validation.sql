-- Phase 3 foundation: source-specific DuckDB views over cleaned CSV files.
-- Run from the repository root. No file under data/cleaned is modified.

CREATE OR REPLACE VIEW amazon_sales AS
SELECT * FROM read_csv_auto('data/cleaned/amazon_sale_report_cleaned.csv', HEADER = TRUE, SAMPLE_SIZE = -1);

CREATE OR REPLACE VIEW international_sales AS
SELECT * FROM read_csv_auto('data/cleaned/international_sale_report_cleaned.csv', HEADER = TRUE, SAMPLE_SIZE = -1);

CREATE OR REPLACE VIEW may_product_prices AS
SELECT * FROM read_csv_auto('data/cleaned/may_2022_cleaned.csv', HEADER = TRUE, SAMPLE_SIZE = -1);

CREATE OR REPLACE VIEW march_product_prices AS
SELECT * FROM read_csv_auto('data/cleaned/p_l_march_2021_cleaned.csv', HEADER = TRUE, SAMPLE_SIZE = -1);

CREATE OR REPLACE VIEW stock_snapshot AS
SELECT * FROM read_csv_auto('data/cleaned/sale_report_cleaned.csv', HEADER = TRUE, SAMPLE_SIZE = -1);

CREATE OR REPLACE VIEW warehouse_rates AS
SELECT * FROM read_csv_auto('data/cleaned/cloud_warehouse_compersion_chart_cleaned.csv', HEADER = TRUE, SAMPLE_SIZE = -1);

CREATE OR REPLACE VIEW expense_report AS
SELECT * FROM read_csv_auto('data/cleaned/expense_iigf_cleaned.csv', HEADER = TRUE, SAMPLE_SIZE = -1);

CREATE OR REPLACE VIEW phase_3_validation AS
SELECT 'amazon_sales' AS table_name, COUNT(*) AS row_count, COUNT(DISTINCT order_id) AS distinct_orders, COUNT(*) - COUNT(DISTINCT order_id) AS line_order_difference FROM amazon_sales
UNION ALL
SELECT 'international_sales', COUNT(*), NULL, NULL FROM international_sales
UNION ALL
SELECT 'may_product_prices', COUNT(*), COUNT(DISTINCT sku), COUNT(*) - COUNT(DISTINCT sku) FROM may_product_prices
UNION ALL
SELECT 'march_product_prices', COUNT(*), COUNT(DISTINCT sku), COUNT(*) - COUNT(DISTINCT sku) FROM march_product_prices
UNION ALL
SELECT 'stock_snapshot', COUNT(*), COUNT(DISTINCT sku_code), COUNT(*) - COUNT(DISTINCT sku_code) FROM stock_snapshot
UNION ALL
SELECT 'warehouse_rates', COUNT(*), COUNT(DISTINCT cost_head), COUNT(*) - COUNT(DISTINCT cost_head) FROM warehouse_rates
UNION ALL
SELECT 'expense_report', COUNT(*), NULL, NULL FROM expense_report;

SELECT * FROM phase_3_validation ORDER BY table_name;
