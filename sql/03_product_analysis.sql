-- Product analysis is based on within-source fact tables and candidate SKU joins.

CREATE OR REPLACE VIEW amazon_category_performance AS
WITH category_totals AS (
    SELECT
        category,
        COUNT(*) AS line_count,
        COUNT(DISTINCT order_id) AS distinct_orders,
        SUM(CAST(qty AS DOUBLE)) AS reported_units,
        SUM(CAST(amount AS DOUBLE)) AS reported_amount
    FROM amazon_sales
    GROUP BY category
)
SELECT
    *,
    RANK() OVER (ORDER BY reported_amount DESC NULLS LAST) AS amount_rank
FROM category_totals;

CREATE OR REPLACE VIEW amazon_sku_performance AS
WITH sku_totals AS (
    SELECT
        sku,
        COUNT(*) AS line_count,
        COUNT(DISTINCT order_id) AS distinct_orders,
        SUM(CAST(qty AS DOUBLE)) AS reported_units,
        SUM(CAST(amount AS DOUBLE)) AS reported_amount
    FROM amazon_sales
    WHERE sku IS NOT NULL
    GROUP BY sku
)
SELECT
    *,
    RANK() OVER (ORDER BY reported_amount DESC NULLS LAST) AS amount_rank_desc,
    RANK() OVER (ORDER BY reported_amount ASC NULLS LAST) AS amount_rank_asc
FROM sku_totals;

CREATE OR REPLACE VIEW amazon_product_match_summary AS
SELECT
    COUNT(*) AS amazon_lines,
    COUNT(*) FILTER (WHERE a.sku IS NOT NULL) AS lines_with_sku,
    COUNT(*) FILTER (WHERE a.sku IS NOT NULL AND p.sku IS NOT NULL) AS lines_with_matched_may_product,
    COUNT(DISTINCT a.sku) FILTER (WHERE a.sku IS NOT NULL) AS distinct_amazon_skus,
    COUNT(DISTINCT a.sku) FILTER (WHERE a.sku IS NOT NULL AND p.sku IS NOT NULL) AS distinct_matched_skus
FROM amazon_sales a
LEFT JOIN may_product_prices p ON a.sku = p.sku;

SELECT * FROM amazon_category_performance ORDER BY amount_rank;
