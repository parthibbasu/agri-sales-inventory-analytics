-- Agri Retail Sales & Inventory Analytics SQL Queries

-- 1. Total revenue, profit, and margin
SELECT
    SUM(units_sold * unit_price) AS total_revenue,
    SUM(units_sold * (unit_price - cost_per_unit)) AS gross_profit,
    ROUND(
        SUM(units_sold * (unit_price - cost_per_unit)) * 100.0 /
        SUM(units_sold * unit_price), 2
    ) AS profit_margin_pct
FROM agri_sales_inventory;

-- 2. Category-wise performance
SELECT
    category,
    SUM(units_sold) AS total_units_sold,
    SUM(units_sold * unit_price) AS revenue,
    SUM(units_sold * (unit_price - cost_per_unit)) AS gross_profit
FROM agri_sales_inventory
GROUP BY category
ORDER BY revenue DESC;

-- 3. District-wise sales performance
SELECT
    state,
    district,
    SUM(units_sold * unit_price) AS revenue,
    COUNT(order_id) AS total_orders
FROM agri_sales_inventory
GROUP BY state, district
ORDER BY revenue DESC;

-- 4. Inventory stockout risk
SELECT
    order_id,
    state,
    district,
    product,
    units_sold,
    inventory_units,
    CASE
        WHEN inventory_units < units_sold THEN 'High Stockout Risk'
        ELSE 'Healthy Inventory'
    END AS inventory_status
FROM agri_sales_inventory;

-- 5. Order mismatch rate by state
SELECT
    state,
    COUNT(*) AS total_orders,
    SUM(order_mismatch) AS mismatch_orders,
    ROUND(SUM(order_mismatch) * 100.0 / COUNT(*), 2) AS mismatch_rate_pct
FROM agri_sales_inventory
GROUP BY state
ORDER BY mismatch_rate_pct DESC;

-- 6. Top 3 products by revenue in each category
WITH product_revenue AS (
    SELECT
        category,
        product,
        SUM(units_sold * unit_price) AS revenue,
        RANK() OVER (
            PARTITION BY category
            ORDER BY SUM(units_sold * unit_price) DESC
        ) AS revenue_rank
    FROM agri_sales_inventory
    GROUP BY category, product
)
SELECT *
FROM product_revenue
WHERE revenue_rank <= 3;
