"""
SQL Insights Page for DataPulse
Demonstrates SQL queries and their business insights
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
import pandas as pd
from common_ui import run_page


def render(db, filters):
    """Render SQL Insights page"""
    st.title("💻 SQL Insights")
    st.markdown("---")
    st.markdown("""
    This page demonstrates important SQL queries used in the DataPulse platform, 
    showcasing various SQL concepts including JOINs, aggregations, window functions, CTEs, and more.
    """)
    
    # SQL Query Examples
    sql_examples = [
        {
            "title": "Top 10 Customers by Revenue",
            "query": """
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    SUM(o.sales) as total_revenue,
    COUNT(o.order_id) as order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY total_revenue DESC
LIMIT 10;
            """,
            "explanation": "This query uses INNER JOIN to combine customer and orders data, then uses GROUP BY and aggregation to calculate total revenue per customer. It identifies the most valuable customers.",
            "insight": "Identifies top revenue-generating customers for targeted marketing and retention strategies."
        },
        {
            "title": "Monthly Sales Growth Using Window Functions",
            "query": """
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', order_date) as month,
        SUM(sales) as monthly_revenue
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) as prev_month_revenue,
    ROUND((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) / 
          LAG(monthly_revenue) OVER (ORDER BY month) * 100, 2) as growth_pct
FROM monthly_sales;
            """,
            "explanation": "This query uses a CTE (Common Table Expression) to calculate monthly sales, then uses the LAG window function to compare each month with the previous month and calculate growth percentage.",
            "insight": "Tracks month-over-month sales growth to identify trends and seasonal patterns."
        },
        {
            "title": "Running Total of Revenue",
            "query": """
SELECT 
    order_date,
    sales,
    SUM(sales) OVER (ORDER BY order_date) as running_total
FROM orders
ORDER BY order_date;
            """,
            "explanation": "This query uses a window function with SUM() OVER() to calculate a running total of revenue over time. The ORDER BY clause ensures the calculation follows the chronological order.",
            "insight": "Shows cumulative revenue over time, useful for tracking progress toward sales targets."
        },
        {
            "title": "Rank Products by Sales Within Each Category",
            "query": """
WITH product_sales AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        SUM(o.sales) as total_sales
    FROM products p
    INNER JOIN orders o ON p.product_id = o.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    category,
    product_name,
    total_sales,
    RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) as sales_rank
FROM product_sales
ORDER BY category, sales_rank;
            """,
            "explanation": "This query uses a CTE to aggregate sales by product, then uses RANK() with PARTITION BY to rank products within each category separately.",
            "insight": "Identifies top-performing products within each category for inventory and marketing decisions."
        },
        {
            "title": "Identify Declining Products",
            "query": """
WITH product_monthly_sales AS (
    SELECT 
        p.product_id,
        p.product_name,
        strftime('%Y-%m', o.order_date) as month,
        SUM(o.sales) as monthly_sales
    FROM orders o
    INNER JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, strftime('%Y-%m', o.order_date)
)
SELECT 
    product_name,
    month,
    monthly_sales,
    LAG(monthly_sales) OVER (PARTITION BY product_id ORDER BY month) as prev_month_sales,
    ROUND((monthly_sales - LAG(monthly_sales) OVER (PARTITION BY product_id ORDER BY month)) / 
          LAG(monthly_sales) OVER (PARTITION BY product_id ORDER BY month) * 100, 2) as growth_pct
FROM product_monthly_sales
WHERE growth_pct < -10 AND prev_month_sales IS NOT NULL
ORDER BY growth_pct ASC;
            """,
            "explanation": "This query uses a CTE to calculate monthly sales per product, then uses LAG window function to calculate month-over-month growth. It filters for products with declining sales (>10% drop).",
            "insight": "Identifies products with declining performance for investigation and potential action."
        },
        {
            "title": "Customer Lifetime Value (CLV)",
            "query": """
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(o.order_id) as total_orders,
    SUM(o.sales) as total_spent,
    SUM(o.profit) as total_profit,
    MIN(o.order_date) as first_purchase,
    MAX(o.order_date) as last_purchase,
    ROUND(SUM(o.sales) / COUNT(o.order_id), 2) as avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY total_spent DESC;
            """,
            "explanation": "This query uses INNER JOIN and multiple aggregations to calculate customer lifetime value metrics including total spent, order count, and average order value.",
            "insight": "Calculates customer lifetime value to identify high-value customers and tailor retention strategies."
        },
        {
            "title": "Discount vs Profit Analysis",
            "query": """
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
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) as profit_margin_pct
FROM orders
GROUP BY discount_category
ORDER BY profit_margin_pct DESC;
            """,
            "explanation": "This query uses CASE WHEN to categorize discounts, then aggregates to analyze the relationship between discount levels and profitability.",
            "insight": "Analyzes how different discount levels affect profit margins to optimize pricing strategy."
        },
        {
            "title": "Regional Performance with HAVING Clause",
            "query": """
SELECT 
    region,
    SUM(sales) as total_revenue,
    SUM(profit) as total_profit,
    COUNT(DISTINCT customer_id) as unique_customers,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) as profit_margin_pct
FROM orders
GROUP BY region
HAVING SUM(sales) > 10000
ORDER BY total_revenue DESC;
            """,
            "explanation": "This query uses GROUP BY to aggregate by region, and HAVING to filter only regions with total revenue above $10,000.",
            "insight": "Identifies high-performing regions and their profit margins for resource allocation."
        }
    ]
    
    # Display SQL examples
    for i, example in enumerate(sql_examples, 1):
        with st.expander(f"{i}. {example['title']}"):
            st.markdown("### SQL Query")
            st.code(example['query'], language='sql')
            
            st.markdown("### Explanation")
            st.markdown(example['explanation'])
            
            st.markdown("### Business Insight")
            st.info(example['insight'])
            
            # Execute query and show results
            try:
                with st.spinner("Executing query..."):
                    result_df = db.execute_query(example['query'])
                    if not result_df.empty:
                        st.markdown("### Query Results")
                        st.dataframe(result_df, use_container_width=True)
                    else:
                        st.info("No results returned for this query")
            except Exception as e:
                st.error(f"Error executing query: {e}")
        
        st.markdown("---")
    
    # SQL Concepts Summary
    st.subheader("SQL Concepts Demonstrated")
    
    concepts = {
        "INNER JOIN": "Combines rows from two tables based on a related column",
        "LEFT JOIN": "Returns all rows from the left table and matching rows from the right table",
        "GROUP BY": "Groups rows that have the same values into summary rows",
        "HAVING": "Filters groups after aggregation (unlike WHERE which filters before aggregation)",
        "Subqueries": "A query nested inside another query",
        "CTE (Common Table Expression)": "Temporary result set defined within the execution scope of a single statement",
        "Window Functions": "Performs calculations across a set of table rows related to the current row (RANK, LAG, SUM OVER)",
        "Aggregations": "Functions that perform calculations on multiple values (SUM, COUNT, AVG, MAX, MIN)",
        "CASE WHEN": "Conditional logic in SQL queries"
    }
    
    col1, col2, col3 = st.columns(3)
    
    for i, (concept, description) in enumerate(concepts.items()):
        if i % 3 == 0:
            with col1:
                st.markdown(f"**{concept}**")
                st.caption(description)
        elif i % 3 == 1:
            with col2:
                st.markdown(f"**{concept}**")
                st.caption(description)
        else:
            with col3:
                st.markdown(f"**{concept}**")
                st.caption(description)


if __name__ == "__main__":
    run_page(render, title="SQL Insights", icon="💻")

