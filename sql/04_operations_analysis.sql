-- Operations analysis uses explicit status proxies and snapshot-safe measures.

CREATE OR REPLACE VIEW amazon_fulfilment_performance AS
SELECT
    fulfilment,
    courier_status,
    COUNT(*) AS line_count,
    COUNT(DISTINCT order_id) AS distinct_orders,
    SUM(CAST(qty AS DOUBLE)) AS reported_units
FROM amazon_sales
GROUP BY fulfilment, courier_status;

CREATE OR REPLACE VIEW warehouse_provider_comparison AS
SELECT
    cost_head,
    shiprocket_price_per_unit,
    increff_price_per_unit,
    increff_price_per_unit - shiprocket_price_per_unit AS increff_minus_shiprocket
FROM warehouse_rates;

CREATE OR REPLACE VIEW stock_snapshot_summary AS
SELECT
    COUNT(*) AS stock_rows,
    COUNT(DISTINCT sku_code) AS distinct_sku_codes,
    SUM(CAST(stock AS DOUBLE)) AS reported_stock_units,
    COUNT(*) FILTER (WHERE CAST(stock AS DOUBLE) = 0) AS zero_stock_rows,
    COUNT(*) FILTER (WHERE sku_code IS NULL) AS missing_sku_code_rows
FROM stock_snapshot;

CREATE OR REPLACE VIEW stock_category_summary AS
SELECT
    category,
    COUNT(*) AS snapshot_rows,
    COUNT(DISTINCT sku_code) AS distinct_sku_codes,
    SUM(CAST(stock AS DOUBLE)) AS reported_stock_units,
    COUNT(*) FILTER (WHERE CAST(stock AS DOUBLE) = 0) AS zero_stock_rows
FROM stock_snapshot
GROUP BY category;

SELECT * FROM amazon_fulfilment_performance ORDER BY distinct_orders DESC;
