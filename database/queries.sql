-- DataPulse SQL Queries
-- Demonstrates various SQL concepts for Business Intelligence

-- ============================================
-- 1. INNER JOIN Example
-- ============================================
-- Join orders with customers and products to get complete order details
SELECT 
    o.order_id,
    o.order_date,
    c.customer_name,
    c.segment,
    p.product_name,
    p.category,
    o.quantity,
    o.sales,
    o.profit
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p ON o.product_id = p.product_id
LIMIT 10;


-- ============================================
-- 2. LEFT JOIN Example
-- ============================================
-- Find all customers and their orders (including customers with no orders)
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(o.order_id) as order_count,
    COALESCE(SUM(o.sales), 0) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY total_spent DESC;


-- ============================================
-- 3. GROUP BY and Aggregations
-- ============================================
-- Total sales and profit by category
SELECT 
    category,
    COUNT(order_id) as total_orders,
    SUM(sales) as total_revenue,
    SUM(profit) as total_profit,
    AVG(sales) as avg_order_value,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) as profit_margin_pct
FROM orders
GROUP BY category
ORDER BY total_revenue DESC;


-- ============================================
-- 4. HAVING Clause
-- ============================================
-- Find categories with profit margin above 20%
SELECT 
    category,
    SUM(sales) as total_revenue,
    SUM(profit) as total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) as profit_margin_pct
FROM orders
GROUP BY category
HAVING (SUM(profit) / SUM(sales)) > 0.20
ORDER BY profit_margin_pct DESC;


-- ============================================
-- 5. Subquery Example
-- ============================================
-- Find orders where sales are above the average order value
SELECT 
    order_id,
    order_date,
    customer_id,
    product_id,
    sales,
    profit
FROM orders
WHERE sales > (SELECT AVG(sales) FROM orders)
ORDER BY sales DESC
LIMIT 10;


-- ============================================
-- 6. CTE (Common Table Expression) Example
-- ============================================
-- Calculate monthly sales growth using CTE
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', order_date) as month,
        SUM(sales) as monthly_revenue
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
),
monthly_growth AS (
    SELECT 
        month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (ORDER BY month) as prev_month_revenue,
        ROUND((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) / 
              LAG(monthly_revenue) OVER (ORDER BY month) * 100, 2) as growth_pct
    FROM monthly_sales
)
SELECT 
    month,
    monthly_revenue,
    prev_month_revenue,
    growth_pct
FROM monthly_growth
WHERE prev_month_revenue IS NOT NULL
ORDER BY month;


-- ============================================
-- 7. Window Functions - RANK
-- ============================================
-- Rank products by sales within each category
WITH product_sales AS (
    SELECT 
        product_id,
        product_name,
        category,
        SUM(sales) as total_sales,
        SUM(profit) as total_profit
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    GROUP BY product_id, product_name, category
)
SELECT 
    category,
    product_name,
    total_sales,
    total_profit,
    RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) as sales_rank
FROM product_sales
ORDER BY category, sales_rank;


-- ============================================
-- 8. Window Functions - ROW_NUMBER
-- ============================================
-- Top 10 customers by revenue with ranking
WITH customer_revenue AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        SUM(o.sales) as total_revenue,
        COUNT(o.order_id) as order_count
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.segment
)
SELECT 
    customer_name,
    segment,
    total_revenue,
    order_count,
    ROW_NUMBER() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM customer_revenue
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================
-- 9. Window Functions - Running Total
-- ============================================
-- Calculate running total of revenue over time
SELECT 
    order_date,
    SUM(sales) OVER (ORDER BY order_date) as running_total_revenue,
    SUM(sales) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total_alt
FROM orders
ORDER BY order_date;


-- ============================================
-- 10. CASE WHEN Statement
-- ============================================
-- Categorize orders based on sales amount
SELECT 
    order_id,
    order_date,
    sales,
    CASE 
        WHEN sales < 100 THEN 'Small Order'
        WHEN sales BETWEEN 100 AND 500 THEN 'Medium Order'
        WHEN sales BETWEEN 500 AND 1000 THEN 'Large Order'
        ELSE 'Very Large Order'
    END as order_size,
    CASE 
        WHEN profit < 0 THEN 'Loss'
        WHEN profit = 0 THEN 'Break-even'
        ELSE 'Profitable'
    END as profitability
FROM orders
ORDER BY sales DESC
LIMIT 20;


-- ============================================
-- 11. Identify Declining Products
-- ============================================
-- Find products with declining sales over time
WITH product_monthly_sales AS (
    SELECT 
        p.product_id,
        p.product_name,
        strftime('%Y-%m', o.order_date) as month,
        SUM(o.sales) as monthly_sales
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, strftime('%Y-%m', o.order_date)
),
product_trend AS (
    SELECT 
        product_id,
        product_name,
        month,
        monthly_sales,
        LAG(monthly_sales) OVER (PARTITION BY product_id ORDER BY month) as prev_month_sales,
        ROUND((monthly_sales - LAG(monthly_sales) OVER (PARTITION BY product_id ORDER BY month)) / 
              LAG(monthly_sales) OVER (PARTITION BY product_id ORDER BY month) * 100, 2) as growth_pct
    FROM product_monthly_sales
)
SELECT 
    product_name,
    month,
    monthly_sales,
    prev_month_sales,
    growth_pct
FROM product_trend
WHERE growth_pct < -10 AND prev_month_sales IS NOT NULL
ORDER BY growth_pct ASC
LIMIT 10;


-- ============================================
-- 12. Customer Lifetime Value (CLV)
-- ============================================
-- Calculate customer lifetime value
WITH customer_stats AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        COUNT(o.order_id) as total_orders,
        MIN(o.order_date) as first_purchase,
        MAX(o.order_date) as last_purchase,
        SUM(o.sales) as total_spent,
        SUM(o.profit) as total_profit
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.segment
),
customer_ltv AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        total_orders,
        total_spent,
        total_profit,
        JULIANDAY(last_purchase) - JULIANDAY(first_purchase) as days_active,
        total_spent / NULLIF(total_orders, 0) as avg_order_value,
        total_spent / NULLIF((JULIANDAY(last_purchase) - JULIANDAY(first_purchase)), 0) * 365 as annual_value
    FROM customer_stats
)
SELECT 
    customer_name,
    segment,
    total_orders,
    ROUND(total_spent, 2) as total_spent,
    ROUND(total_profit, 2) as total_profit,
    ROUND(avg_order_value, 2) as avg_order_value,
    ROUND(annual_value, 2) as estimated_annual_value
FROM customer_ltv
ORDER BY total_spent DESC
LIMIT 10;


-- ============================================
-- 13. Regional Performance Analysis
-- ============================================
-- Analyze sales performance by region
SELECT 
    region,
    COUNT(DISTINCT order_id) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(sales) as total_revenue,
    SUM(profit) as total_profit,
    ROUND(AVG(sales), 2) as avg_order_value,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) as profit_margin_pct
FROM orders
GROUP BY region
ORDER BY total_revenue DESC;


-- ============================================
-- 14. Discount vs Profit Analysis
-- ============================================
-- Analyze the relationship between discount and profit
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.10 THEN 'Low Discount (0-10%)'
        WHEN discount <= 0.20 THEN 'Medium Discount (10-20%)'
        ELSE 'High Discount (>20%)'
    END as discount_category,
    COUNT(order_id) as order_count,
    SUM(sales) as total_revenue,
    SUM(profit) as total_profit,
    ROUND(AVG(profit), 2) as avg_profit_per_order,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) as profit_margin_pct
FROM orders
GROUP BY discount_category
ORDER BY profit_margin_pct DESC;


-- ============================================
-- 15. Repeat Customer Analysis
-- ============================================
-- Identify repeat customers and their behavior
WITH customer_order_count AS (
    SELECT 
        customer_id,
        COUNT(order_id) as order_count
    FROM orders
    GROUP BY customer_id
),
customer_classification AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        COALESCE(oc.order_count, 0) as order_count,
        CASE 
            WHEN COALESCE(oc.order_count, 0) = 0 THEN 'No Orders'
            WHEN COALESCE(oc.order_count, 0) = 1 THEN 'One-time Customer'
            WHEN COALESCE(oc.order_count, 0) BETWEEN 2 AND 5 THEN 'Occasional Customer'
            ELSE 'Loyal Customer'
        END as customer_type
    FROM customers c
    LEFT JOIN customer_order_count oc ON c.customer_id = oc.customer_id
)
SELECT 
    customer_type,
    COUNT(customer_id) as customer_count,
    ROUND(COUNT(customer_id) * 100.0 / SUM(COUNT(customer_id)) OVER (), 2) as percentage
FROM customer_classification
GROUP BY customer_type
ORDER BY customer_count DESC;


-- ============================================
-- 16. Seasonal Sales Pattern
-- ============================================
-- Analyze seasonal sales patterns by quarter
SELECT 
    strftime('%Y', order_date) as year,
    CASE 
        WHEN CAST(strftime('%m', order_date) AS INTEGER) IN (1, 2, 3) THEN 'Q1'
        WHEN CAST(strftime('%m', order_date) AS INTEGER) IN (4, 5, 6) THEN 'Q2'
        WHEN CAST(strftime('%m', order_date) AS INTEGER) IN (7, 8, 9) THEN 'Q3'
        ELSE 'Q4'
    END as quarter,
    COUNT(order_id) as order_count,
    SUM(sales) as total_revenue,
    SUM(profit) as total_profit
FROM orders
GROUP BY year, quarter
ORDER BY year, quarter;


-- ============================================
-- 17. High Revenue Low Profit Products
-- ============================================
-- Identify products that generate high revenue but low profit
WITH product_performance AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        SUM(o.sales) as total_revenue,
        SUM(o.profit) as total_profit,
        ROUND((SUM(o.profit) / SUM(o.sales)) * 100, 2) as profit_margin
    FROM products p
    INNER JOIN orders o ON p.product_id = o.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    product_name,
    category,
    ROUND(total_revenue, 2) as total_revenue,
    ROUND(total_profit, 2) as total_profit,
    profit_margin
FROM product_performance
WHERE total_revenue > 1000 AND profit_margin < 15
ORDER BY total_revenue DESC;


-- ============================================
-- 18. Cross-Selling Opportunity
-- ============================================
-- Find products frequently bought together (simplified version)
WITH product_pairs AS (
    SELECT 
        o1.product_id as product_1,
        o2.product_id as product_2,
        COUNT(*) as purchase_count
    FROM orders o1
    INNER JOIN orders o2 ON o1.order_id = o2.order_id
    WHERE o1.product_id < o2.product_id
    GROUP BY o1.product_id, o2.product_id
    HAVING COUNT(*) > 5
)
SELECT 
    p1.product_name as product_1,
    p2.product_name as product_2,
    pp.purchase_count as times_bought_together
FROM product_pairs pp
INNER JOIN products p1 ON pp.product_1 = p1.product_id
INNER JOIN products p2 ON pp.product_2 = p2.product_id
ORDER BY pp.purchase_count DESC
LIMIT 10;
