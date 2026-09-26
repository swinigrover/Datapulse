"""
Executive Overview Page for DataPulse
Displays key performance indicators and high-level metrics
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
import pandas as pd
from common_ui import run_page
import plotly.express as px
import plotly.graph_objects as go
from analytics.sales_analysis import (
    get_monthly_revenue_trend,
    get_sales_by_region,
    get_sales_by_category,
    get_top_products,
    plot_monthly_revenue_trend,
    plot_sales_by_region,
    plot_sales_by_category,
    plot_profit_by_category,
    plot_top_products
)


def render(db, filters):
    """Render Executive Overview page"""
    st.title("🏠 Executive Overview")
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
        
        # Get KPIs
        kpis = db.get_kpis(
            start_date=filters.get('start_date'),
            end_date=filters.get('end_date'),
            region=filters.get('region'),
            category=filters.get('category'),
            segment=filters.get('segment')
        )
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"${kpis['total_revenue']:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Total Orders",
            value=f"{kpis['total_orders']:,}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Total Profit",
            value=f"${kpis['total_profit']:,.2f}",
            delta=None
        )
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.metric(
            label="Profit Margin",
            value=f"{kpis['profit_margin']:.2f}%",
            delta=None
        )
    
    with col5:
        st.metric(
            label="Average Order Value",
            value=f"${kpis['avg_order_value']:,.2f}",
            delta=None
        )
    
    with col6:
        st.metric(
            label="Total Customers",
            value=f"{kpis['total_customers']:,}",
            delta=None
        )
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Revenue Trend")
        monthly_data = get_monthly_revenue_trend(df)
        if not monthly_data.empty:
            fig = plot_monthly_revenue_trend(monthly_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No monthly data available")
    
    with col2:
        st.subheader("Sales by Region")
        regional_data = get_sales_by_region(df)
        if not regional_data.empty:
            fig = plot_sales_by_region(regional_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No regional data available")
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Category")
        category_data = get_sales_by_category(df)
        if not category_data.empty:
            fig = plot_sales_by_category(category_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")
    
    with col2:
        st.subheader("Profit by Category")
        if not category_data.empty:
            fig = plot_profit_by_category(category_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")
    
    # Charts Row 3
    st.subheader("Top 10 Products by Revenue")
    top_products = get_top_products(df, n=10)
    if not top_products.empty:
        fig = plot_top_products(top_products)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No product data available")
    
    # Detailed Data Tables
    st.markdown("---")
    st.subheader("Detailed Data")
    
    with st.expander("View Regional Performance Details"):
        if not regional_data.empty:
            st.dataframe(
                regional_data.style.format({
                    'revenue': '${:,.2f}',
                    'profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    with st.expander("View Category Performance Details"):
        if not category_data.empty:
            st.dataframe(
                category_data.style.format({
                    'revenue': '${:,.2f}',
                    'profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )


if __name__ == "__main__":
    run_page(render, title="Executive Overview", icon="🏠")

