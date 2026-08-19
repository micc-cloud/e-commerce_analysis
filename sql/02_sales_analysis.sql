-- Sales analysis stays within source and currency boundaries.
-- `reported_amount` is a source-reported field; NULL amounts are not imputed.

CREATE OR REPLACE VIEW amazon_monthly_sales AS
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', CAST(date AS DATE)) AS sales_month,
        SUM(CAST(amount AS DOUBLE)) AS reported_amount,
        COUNT(amount) AS amount_lines,
        COUNT(*) FILTER (WHERE CAST(amount AS DOUBLE) = 0) AS zero_amount_lines,
        COUNT(*) FILTER (WHERE CAST(qty AS DOUBLE) = 0) AS zero_quantity_lines,
        SUM(CAST(qty AS DOUBLE)) AS reported_units,
        COUNT(DISTINCT order_id) AS distinct_orders,
        COUNT(*) AS line_count
    FROM amazon_sales
    GROUP BY 1
)
SELECT
    'reported_source' AS analysis_scope,
    sales_month,
    reported_amount,
    amount_lines,
    line_count,
    100.0 * amount_lines / NULLIF(line_count, 0) AS amount_coverage_pct,
    zero_amount_lines,
    zero_quantity_lines,
    reported_units,
    distinct_orders,
    reported_amount / NULLIF(distinct_orders, 0) AS reported_value_per_distinct_order,
    reported_amount - LAG(reported_amount) OVER (ORDER BY sales_month) AS amount_change_mom,
    100.0 * (reported_amount - LAG(reported_amount) OVER (ORDER BY sales_month))
        / NULLIF(LAG(reported_amount) OVER (ORDER BY sales_month), 0) AS amount_change_mom_pct
FROM monthly;

CREATE OR REPLACE VIEW amazon_status_scoped_sales AS
SELECT
    *,
    CASE
        WHEN LOWER(status) = 'cancelled' THEN 'cancelled'
        WHEN LOWER(status) LIKE '%return%' THEN 'return_related'
        WHEN status = 'Shipped - Delivered to Buyer' THEN 'delivered_status_proxy'
        ELSE 'other_status'
    END AS status_group,
    status = 'Shipped - Delivered to Buyer' AS is_delivered_status_proxy
FROM amazon_sales;

CREATE OR REPLACE VIEW amazon_monthly_sales_scoped AS
WITH scoped AS (
    SELECT
        'reported_source' AS analysis_scope,
        DATE_TRUNC('month', CAST(date AS DATE)) AS sales_month,
        SUM(CAST(amount AS DOUBLE)) AS reported_amount,
        COUNT(amount) AS amount_lines,
        COUNT(*) FILTER (WHERE CAST(amount AS DOUBLE) = 0) AS zero_amount_lines,
        COUNT(*) FILTER (WHERE CAST(qty AS DOUBLE) = 0) AS zero_quantity_lines,
        SUM(CAST(qty AS DOUBLE)) AS reported_units,
        COUNT(DISTINCT order_id) AS distinct_orders,
        COUNT(*) AS line_count
    FROM amazon_status_scoped_sales
    GROUP BY 1, 2
    UNION ALL
    SELECT
        'delivered_status_proxy' AS analysis_scope,
        DATE_TRUNC('month', CAST(date AS DATE)) AS sales_month,
        SUM(CAST(amount AS DOUBLE)) AS reported_amount,
        COUNT(amount) AS amount_lines,
        COUNT(*) FILTER (WHERE CAST(amount AS DOUBLE) = 0) AS zero_amount_lines,
        COUNT(*) FILTER (WHERE CAST(qty AS DOUBLE) = 0) AS zero_quantity_lines,
        SUM(CAST(qty AS DOUBLE)) AS reported_units,
        COUNT(DISTINCT order_id) AS distinct_orders,
        COUNT(*) AS line_count
    FROM amazon_status_scoped_sales
    WHERE is_delivered_status_proxy
    GROUP BY 1, 2
)
SELECT
    analysis_scope,
    sales_month,
    reported_amount,
    amount_lines,
    line_count,
    100.0 * amount_lines / NULLIF(line_count, 0) AS amount_coverage_pct,
    zero_amount_lines,
    zero_quantity_lines,
    reported_units,
    distinct_orders,
    reported_amount / NULLIF(distinct_orders, 0) AS reported_value_per_distinct_order,
    reported_amount - LAG(reported_amount) OVER (PARTITION BY analysis_scope ORDER BY sales_month) AS amount_change_mom,
    100.0 * (reported_amount - LAG(reported_amount) OVER (PARTITION BY analysis_scope ORDER BY sales_month))
        / NULLIF(LAG(reported_amount) OVER (PARTITION BY analysis_scope ORDER BY sales_month), 0) AS amount_change_mom_pct
FROM scoped;

CREATE OR REPLACE VIEW international_monthly_sales AS
SELECT
    DATE_TRUNC('month', CAST(date AS DATE)) AS sales_month,
    SUM(CAST(gross_amt AS DOUBLE)) AS reported_gross_amount,
    SUM(CAST(pcs AS DOUBLE)) AS reported_pieces,
    COUNT(*) AS line_count
FROM international_sales
GROUP BY 1;

CREATE OR REPLACE VIEW amazon_status_analysis AS
WITH labelled AS (
    SELECT
        order_id,
        CASE
            WHEN LOWER(status) LIKE '%cancel%' THEN 'cancelled_status'
            WHEN LOWER(status) LIKE '%return%' THEN 'returned_status'
            WHEN LOWER(status) LIKE '%deliver%' THEN 'delivered_status'
            ELSE 'other_status'
        END AS status_group
    FROM amazon_sales
), order_status AS (
    SELECT order_id, MAX(status_group = 'cancelled_status') AS has_cancelled,
        MAX(status_group = 'returned_status') AS has_returned,
        MAX(status_group = 'delivered_status') AS has_delivered
    FROM labelled
    GROUP BY order_id
)
SELECT
    COUNT(*) AS distinct_orders,
    COUNT(*) FILTER (WHERE has_cancelled) AS orders_with_cancelled_status,
    COUNT(*) FILTER (WHERE has_returned) AS orders_with_returned_status,
    COUNT(*) FILTER (WHERE has_delivered) AS orders_with_delivered_status,
    COUNT(*) FILTER (WHERE has_cancelled) * 1.0 / NULLIF(COUNT(*), 0) AS cancelled_status_proxy_rate,
    COUNT(*) FILTER (WHERE has_returned) * 1.0 / NULLIF(COUNT(*), 0) AS returned_status_proxy_rate,
    COUNT(*) FILTER (WHERE has_delivered) * 1.0 / NULLIF(COUNT(*), 0) AS delivered_status_proxy_rate
FROM order_status;

CREATE OR REPLACE VIEW amazon_platform_performance AS
SELECT
    'reported_source' AS analysis_scope,
    'source_local_channel_mix' AS metric_type,
    sales_channel,
    fulfilment,
    COUNT(*) AS line_count,
    COUNT(DISTINCT order_id) AS distinct_orders,
    SUM(CAST(amount AS DOUBLE)) AS reported_amount,
    SUM(CAST(qty AS DOUBLE)) AS reported_units
FROM amazon_sales
GROUP BY sales_channel, fulfilment;

SELECT * FROM amazon_monthly_sales ORDER BY sales_month;
