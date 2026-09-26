"""
Customer Analytics Page for DataPulse
Customer segmentation and behavior analysis
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
import pandas as pd
from common_ui import run_page
from analytics.customer_analysis import (
    get_customer_segmentation,
    get_top_customers,
    get_repeat_customer_analysis,
    get_customer_lifetime_value,
    get_geographic_customer_distribution,
    get_segment_performance,
    plot_customer_segmentation,
    plot_top_customers,
    plot_repeat_customer_analysis,
    plot_geographic_distribution,
    plot_segment_performance,
    plot_customer_lifetime_value
)


def render(db, filters):
    """Render Customer Analytics page"""
    st.title("👥 Customer Analytics")
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
    
    # Customer Segmentation
    st.subheader("Customer Segmentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        customer_stats = get_customer_segmentation(df)
        if not customer_stats.empty:
            fig = plot_customer_segmentation(customer_stats)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        segment_performance = get_segment_performance(df)
        if not segment_performance.empty:
            fig = plot_segment_performance(segment_performance)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Top Customers
    st.subheader("Top Customers by Revenue")
    
    top_customers = get_top_customers(df, n=10)
    if not top_customers.empty:
        fig = plot_top_customers(top_customers)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Top Customers Data"):
            st.dataframe(
                top_customers.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'avg_order_value': '${:,.2f}'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Repeat Customer Analysis
    st.subheader("Repeat Customer Analysis")
    
    repeat_analysis = get_repeat_customer_analysis(df)
    if not repeat_analysis.empty:
        fig = plot_repeat_customer_analysis(repeat_analysis)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Repeat Customer Data"):
            st.dataframe(
                repeat_analysis.style.format({
                    'total_revenue': '${:,.2f}',
                    'avg_revenue_per_customer': '${:,.2f}',
                    'percentage': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Customer Lifetime Value
    st.subheader("Customer Lifetime Value (CLV)")
    
    clv_data = get_customer_lifetime_value(df)
    if not clv_data.empty:
        fig = plot_customer_lifetime_value(clv_data)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View CLV Data (Top 20)"):
            st.dataframe(
                clv_data.head(20).style.format({
                    'total_spent': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'avg_order_value': '${:,.2f}',
                    'annual_value': '${:,.2f}'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Geographic Distribution
    st.subheader("Geographic Customer Distribution")
    
    geo_data = get_geographic_customer_distribution(df)
    if not geo_data.empty:
        fig = plot_geographic_distribution(geo_data)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Geographic Data"):
            st.dataframe(
                geo_data.head(20).style.format({
                    'total_revenue': '${:,.2f}'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Segment Performance Details
    st.subheader("Segment Performance Details")
    
    if not segment_performance.empty:
        st.dataframe(
            segment_performance.style.format({
                'total_revenue': '${:,.2f}',
                'total_profit': '${:,.2f}',
                'avg_order_value': '${:,.2f}',
                'profit_margin': '{:.2f}%',
                'revenue_per_customer': '${:,.2f}'
            }),
            use_container_width=True
        )


if __name__ == "__main__":
    run_page(render, title="Customer Analytics", icon="👥")

