"""
Product Analytics Page for DataPulse
Product performance and profitability analysis
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
import pandas as pd
from common_ui import run_page
from analytics.product_analysis import (
    get_best_selling_products,
    get_most_profitable_products,
    get_low_performing_products,
    get_category_analysis,
    get_subcategory_analysis,
    get_product_ranking_by_category,
    get_high_revenue_low_profit_products,
    plot_best_selling_products,
    plot_most_profitable_products,
    plot_category_performance,
    plot_subcategory_analysis,
    plot_product_profitability_scatter,
    plot_low_performing_products
)


def render(db, filters):
    """Render Product Analytics page"""
    st.title("📦 Product Analytics")
    st.markdown("---")
    
    # Get filtered data
    with st.spinner("Loading data..."):
        df = db.get_orders_data(
            start_date=filters.get('start_date'),
            end_date=filters.get('end_date'),
            region=filters.get('region'),
            category=filters.get('category'),
            segment=filters.get('segment')
        )
        
        if df.empty:
            st.warning("No data available for the selected filters.")
            return
    
    # Best-Selling Products
    st.subheader("Best-Selling Products")
    
    best_selling = get_best_selling_products(df, n=10)
    if not best_selling.empty:
        fig = plot_best_selling_products(best_selling)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Best-Selling Products Data"):
            st.dataframe(
                best_selling.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Most Profitable Products
    st.subheader("Most Profitable Products")
    
    most_profitable = get_most_profitable_products(df, n=10)
    if not most_profitable.empty:
        fig = plot_most_profitable_products(most_profitable)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Most Profitable Products Data"):
            st.dataframe(
                most_profitable.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Category Performance
    st.subheader("Category Performance")
    
    category_data = get_category_analysis(df)
    if not category_data.empty:
        fig = plot_category_performance(category_data)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Category Performance Data"):
            st.dataframe(
                category_data.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%',
                    'avg_revenue_per_product': '${:,.2f}'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Sub-Category Analysis
    st.subheader("Sub-Category Analysis")
    
    subcategory_data = get_subcategory_analysis(df)
    if not subcategory_data.empty:
        fig = plot_subcategory_analysis(subcategory_data)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Sub-Category Data"):
            st.dataframe(
                subcategory_data.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Product Profitability Analysis
    st.subheader("Product Profitability Analysis")
    
    product_ranking = get_product_ranking_by_category(df)
    if not product_ranking.empty:
        fig = plot_product_profitability_scatter(product_ranking)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Product Ranking Data"):
            st.dataframe(
                product_ranking.head(30).style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Low Performing Products
    st.subheader("Low Performing Products")
    
    low_performing = get_low_performing_products(df, n=10)
    if not low_performing.empty:
        fig = plot_low_performing_products(low_performing)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Low Performing Products Data"):
            st.dataframe(
                low_performing.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # High Revenue Low Profit Products
    st.subheader("High Revenue, Low Profit Products")
    
    high_rev_low_profit = get_high_revenue_low_profit_products(df)
    if not high_rev_low_profit.empty:
        st.warning(f"Found {len(high_rev_low_profit)} products with high revenue but low profit margin (<15%)")
        st.dataframe(
            high_rev_low_profit.style.format({
                'total_revenue': '${:,.2f}',
                'total_profit': '${:,.2f}',
                'profit_margin': '{:.2f}%'
            }),
            use_container_width=True
        )
    else:
        st.success("No products found with high revenue and low profit margin")


if __name__ == "__main__":
    run_page(render, title="Product Analytics", icon="📦")

