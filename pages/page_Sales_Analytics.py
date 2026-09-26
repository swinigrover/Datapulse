"""
Sales Analytics Page for DataPulse
Detailed sales performance analysis
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
import pandas as pd
from common_ui import run_page
from analytics.sales_analysis import (
    get_monthly_revenue_trend,
    get_yearly_sales_trend,
    get_sales_by_region,
    get_sales_by_category,
    get_sales_by_subcategory,
    get_discount_vs_profit_analysis,
    get_top_products,
    get_bottom_products,
    plot_monthly_revenue_trend,
    plot_sales_by_region,
    plot_discount_vs_profit,
    plot_top_products
)
import plotly.express as px
import plotly.graph_objects as go


def render(db, filters):
    """Render Sales Analytics page"""
    st.title("📈 Sales Analytics")
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
    
    # Time Trend Analysis
    st.subheader("Time Trend Analysis")
    
    trend_option = st.radio("Select Time Period", ["Monthly", "Yearly"], horizontal=True)
    
    if trend_option == "Monthly":
        monthly_data = get_monthly_revenue_trend(df)
        if not monthly_data.empty:
            fig = plot_monthly_revenue_trend(monthly_data)
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("View Monthly Data"):
                st.dataframe(
                    monthly_data.style.format({
                        'revenue': '${:,.2f}',
                        'profit': '${:,.2f}'
                    }),
                    use_container_width=True
                )
    else:
        yearly_data = get_yearly_sales_trend(df)
        if not yearly_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=yearly_data['year'],
                y=yearly_data['revenue'],
                name='Revenue',
                marker_color='#1f77b4'
            ))
            fig.add_trace(go.Bar(
                x=yearly_data['year'],
                y=yearly_data['profit'],
                name='Profit',
                marker_color='#2ca02c'
            ))
            fig.update_layout(
                title='Yearly Sales Trend',
                xaxis_title='Year',
                yaxis_title='Amount ($)',
                barmode='group',
                template='plotly_white',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("View Yearly Data"):
                st.dataframe(
                    yearly_data.style.format({
                        'revenue': '${:,.2f}',
                        'profit': '${:,.2f}'
                    }),
                    use_container_width=True
                )
    
    st.markdown("---")
    
    # Category Performance
    st.subheader("Category Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        category_data = get_sales_by_category(df)
        if not category_data.empty:
            fig = px.bar(
                category_data,
                x='category',
                y='revenue',
                title='Revenue by Category',
                color='revenue',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                xaxis_title='Category',
                yaxis_title='Revenue ($)',
                template='plotly_white',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not category_data.empty:
            fig = px.bar(
                category_data,
                x='category',
                y='profit_margin',
                title='Profit Margin by Category',
                color='profit_margin',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(
                xaxis_title='Category',
                yaxis_title='Profit Margin (%)',
                template='plotly_white',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Regional Performance
    st.subheader("Regional Performance")
    
    regional_data = get_sales_by_region(df)
    if not regional_data.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=regional_data['region'],
            y=regional_data['revenue'],
            name='Revenue',
            marker_color='#1f77b4'
        ))
        fig.add_trace(go.Bar(
            x=regional_data['region'],
            y=regional_data['profit'],
            name='Profit',
            marker_color='#2ca02c'
        ))
        fig.update_layout(
            title='Regional Performance: Revenue vs Profit',
            xaxis_title='Region',
            yaxis_title='Amount ($)',
            barmode='group',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Regional Data"):
            st.dataframe(
                regional_data.style.format({
                    'revenue': '${:,.2f}',
                    'profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Discount vs Profit Analysis
    st.subheader("Discount vs Profit Analysis")
    
    discount_data = get_discount_vs_profit_analysis(df)
    if not discount_data.empty:
        fig = plot_discount_vs_profit(discount_data)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Discount Analysis Data"):
            st.dataframe(
                discount_data.style.format({
                    'revenue': '${:,.2f}',
                    'profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%',
                    'avg_profit_per_order': '${:,.2f}'
                }),
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Product Performance
    st.subheader("Product Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top Performing Products")
        top_products = get_top_products(df, n=10)
        if not top_products.empty:
            fig = plot_top_products(top_products)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Low Performing Products")
        bottom_products = get_bottom_products(df, n=10)
        if not bottom_products.empty:
            bottom_products = bottom_products.sort_values('revenue', ascending=True)
            fig = px.bar(
                bottom_products,
                x='revenue',
                y='product_name',
                title='Bottom 10 Products by Revenue',
                orientation='h',
                color='profit_margin',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(
                xaxis_title='Revenue ($)',
                yaxis_title='Product Name',
                template='plotly_white',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Sub-Category Analysis
    st.subheader("Sub-Category Analysis")
    
    subcategory_data = get_sales_by_subcategory(df)
    if not subcategory_data.empty:
        fig = px.treemap(
            subcategory_data,
            path=['category', 'sub_category'],
            values='revenue',
            title='Revenue Distribution by Sub-Category',
            color='profit_margin',
            color_continuous_scale='RdYlGn',
            hover_data=['order_count', 'profit']
        )
        fig.update_layout(
            template='plotly_white',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Sub-Category Data"):
            st.dataframe(
                subcategory_data.style.format({
                    'revenue': '${:,.2f}',
                    'profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )


if __name__ == "__main__":
    run_page(render, title="Sales Analytics", icon="📈")

