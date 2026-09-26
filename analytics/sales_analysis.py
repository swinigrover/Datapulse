"""
Sales Analysis Module for DataPulse
Provides functions for sales analytics and insights
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_monthly_revenue_trend(df):
    """
    Calculate monthly revenue trend
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with monthly revenue data
    """
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period('M')
    
    monthly_data = df.groupby('month').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    monthly_data['month'] = monthly_data['month'].astype(str)
    monthly_data.columns = ['month', 'revenue', 'profit', 'order_count']
    
    return monthly_data


def get_yearly_sales_trend(df):
    """
    Calculate yearly sales trend
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with yearly sales data
    """
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year'] = df['order_date'].dt.year
    
    yearly_data = df.groupby('year').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    yearly_data.columns = ['year', 'revenue', 'profit', 'order_count']
    
    return yearly_data


def get_sales_by_region(df):
    """
    Calculate sales by region
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with regional sales data
    """
    regional_data = df.groupby('region').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count',
        'customer_id': 'nunique'
    }).reset_index()
    
    regional_data.columns = ['region', 'revenue', 'profit', 'order_count', 'customer_count']
    regional_data = regional_data.sort_values('revenue', ascending=False)
    
    return regional_data


def get_sales_by_category(df):
    """
    Calculate sales by category
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with category sales data
    """
    category_data = df.groupby('category').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    category_data['profit_margin'] = (category_data['profit'] / category_data['sales']) * 100
    category_data.columns = ['category', 'revenue', 'profit', 'order_count', 'profit_margin']
    category_data = category_data.sort_values('revenue', ascending=False)
    
    return category_data


def get_sales_by_subcategory(df):
    """
    Calculate sales by sub-category
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with sub-category sales data
    """
    subcategory_data = df.groupby(['category', 'sub_category']).agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    subcategory_data['profit_margin'] = (subcategory_data['profit'] / subcategory_data['sales']) * 100
    subcategory_data.columns = ['category', 'sub_category', 'revenue', 'profit', 'order_count', 'profit_margin']
    subcategory_data = subcategory_data.sort_values('revenue', ascending=False)
    
    return subcategory_data


def get_discount_vs_profit_analysis(df):
    """
    Analyze relationship between discount and profit
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with discount analysis
    """
    df = df.copy()
    df['discount_category'] = pd.cut(df['discount'], 
                                     bins=[-0.01, 0, 0.1, 0.2, 1.0],
                                     labels=['No Discount', 'Low (0-10%)', 'Medium (10-20%)', 'High (>20%)'])
    
    discount_data = df.groupby('discount_category', observed=False).agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    discount_data.columns = ['discount_category', 'revenue', 'profit', 'order_count']
    discount_data['profit_margin'] = (discount_data['profit'] / discount_data['revenue']) * 100
    discount_data['avg_profit_per_order'] = discount_data['profit'] / discount_data['order_count']
    
    return discount_data


def get_top_products(df, n=10):
    """
    Get top N products by sales
    
    Args:
        df: DataFrame with orders data
        n: Number of top products to return
        
    Returns:
        DataFrame with top products
    """
    product_sales = df.groupby(['product_id', 'product_name']).agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    product_sales['profit_margin'] = (product_sales['profit'] / product_sales['sales']) * 100
    product_sales.columns = ['product_id', 'product_name', 'revenue', 'profit', 'order_count', 'profit_margin']
    product_sales = product_sales.sort_values('revenue', ascending=False).head(n)
    
    return product_sales


def get_bottom_products(df, n=10):
    """
    Get bottom N products by sales
    
    Args:
        df: DataFrame with orders data
        n: Number of bottom products to return
        
    Returns:
        DataFrame with bottom products
    """
    product_sales = df.groupby(['product_id', 'product_name']).agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    product_sales['profit_margin'] = (product_sales['profit'] / product_sales['sales']) * 100
    product_sales.columns = ['product_id', 'product_name', 'revenue', 'profit', 'order_count', 'profit_margin']
    product_sales = product_sales.sort_values('revenue', ascending=True).head(n)
    
    return product_sales


def plot_monthly_revenue_trend(monthly_data):
    """
    Create line chart for monthly revenue trend
    
    Args:
        monthly_data: DataFrame with monthly revenue data
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_data['month'],
        y=monthly_data['revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_data['month'],
        y=monthly_data['profit'],
        mode='lines+markers',
        name='Profit',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Monthly Revenue and Profit Trend',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_sales_by_region(regional_data):
    """
    Create bar chart for sales by region
    
    Args:
        regional_data: DataFrame with regional sales data
        
    Returns:
        Plotly figure
    """
    fig = px.bar(
        regional_data,
        x='region',
        y='revenue',
        title='Sales by Region',
        color='revenue',
        color_continuous_scale='Blues',
        text_auto=True
    )
    
    fig.update_layout(
        xaxis_title='Region',
        yaxis_title='Revenue ($)',
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig


def plot_sales_by_category(category_data):
    """
    Create pie chart for sales by category
    
    Args:
        category_data: DataFrame with category sales data
        
    Returns:
        Plotly figure
    """
    fig = px.pie(
        category_data,
        values='revenue',
        names='category',
        title='Revenue Distribution by Category',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=12
    )
    
    fig.update_layout(
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_profit_by_category(category_data):
    """
    Create bar chart for profit by category
    
    Args:
        category_data: DataFrame with category sales data
        
    Returns:
        Plotly figure
    """
    fig = px.bar(
        category_data,
        x='category',
        y='profit',
        title='Profit by Category',
        color='profit',
        color_continuous_scale='RdYlGn',
        text_auto=True
    )
    
    fig.update_layout(
        xaxis_title='Category',
        yaxis_title='Profit ($)',
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig


def plot_discount_vs_profit(discount_data):
    """
    Create bar chart for discount vs profit analysis
    
    Args:
        discount_data: DataFrame with discount analysis
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=discount_data['discount_category'],
        y=discount_data['revenue'],
        name='Revenue',
        marker_color='#1f77b4'
    ))
    
    fig.add_trace(go.Bar(
        x=discount_data['discount_category'],
        y=discount_data['profit'],
        name='Profit',
        marker_color='#2ca02c'
    ))
    
    fig.update_layout(
        title='Revenue and Profit by Discount Category',
        xaxis_title='Discount Category',
        yaxis_title='Amount ($)',
        barmode='group',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_top_products(product_data):
    """
    Create horizontal bar chart for top products
    
    Args:
        product_data: DataFrame with product sales data
        
    Returns:
        Plotly figure
    """
    product_data = product_data.sort_values('revenue', ascending=True)
    
    fig = px.bar(
        product_data,
        x='revenue',
        y='product_name',
        title='Top 10 Products by Revenue',
        orientation='h',
        color='revenue',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_title='Revenue ($)',
        yaxis_title='Product Name',
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    return fig
