"""
Product Analysis Module for DataPulse
Provides functions for product analytics and insights
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_best_selling_products(df, n=10):
    """
    Get best-selling products by quantity and revenue
    
    Args:
        df: DataFrame with orders data
        n: Number of top products to return
        
    Returns:
        DataFrame with best-selling products
    """
    product_stats = df.groupby(['product_id', 'product_name', 'category', 'sub_category']).agg({
        'quantity': 'sum',
        'sales': 'sum',
        'order_id': 'count',
        'profit': 'sum'
    }).reset_index()
    
    product_stats.columns = ['product_id', 'product_name', 'category', 'sub_category', 
                             'total_quantity', 'total_revenue', 'order_count', 'total_profit']
    product_stats['profit_margin'] = (product_stats['total_profit'] / product_stats['total_revenue']) * 100
    product_stats = product_stats.sort_values('total_quantity', ascending=False).head(n)
    
    return product_stats


def get_most_profitable_products(df, n=10):
    """
    Get most profitable products by profit margin and total profit
    
    Args:
        df: DataFrame with orders data
        n: Number of top products to return
        
    Returns:
        DataFrame with most profitable products
    """
    product_stats = df.groupby(['product_id', 'product_name', 'category', 'sub_category']).agg({
        'quantity': 'sum',
        'sales': 'sum',
        'order_id': 'count',
        'profit': 'sum'
    }).reset_index()
    
    product_stats.columns = ['product_id', 'product_name', 'category', 'sub_category', 
                             'total_quantity', 'total_revenue', 'order_count', 'total_profit']
    product_stats['profit_margin'] = (product_stats['total_profit'] / product_stats['total_revenue']) * 100
    product_stats = product_stats.sort_values('total_profit', ascending=False).head(n)
    
    return product_stats


def get_low_performing_products(df, n=10):
    """
    Get low-performing products by revenue and profit
    
    Args:
        df: DataFrame with orders data
        n: Number of bottom products to return
        
    Returns:
        DataFrame with low-performing products
    """
    product_stats = df.groupby(['product_id', 'product_name', 'category', 'sub_category']).agg({
        'quantity': 'sum',
        'sales': 'sum',
        'order_id': 'count',
        'profit': 'sum'
    }).reset_index()
    
    product_stats.columns = ['product_id', 'product_name', 'category', 'sub_category', 
                             'total_quantity', 'total_revenue', 'order_count', 'total_profit']
    product_stats['profit_margin'] = (product_stats['total_profit'] / product_stats['total_revenue']) * 100
    product_stats = product_stats.sort_values('total_revenue', ascending=True).head(n)
    
    return product_stats


def get_category_analysis(df):
    """
    Analyze product performance by category
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with category analysis
    """
    category_stats = df.groupby('category').agg({
        'product_id': 'nunique',
        'quantity': 'sum',
        'sales': 'sum',
        'order_id': 'count',
        'profit': 'sum'
    }).reset_index()
    
    category_stats.columns = ['category', 'unique_products', 'total_quantity', 
                              'total_revenue', 'order_count', 'total_profit']
    category_stats['profit_margin'] = (category_stats['total_profit'] / category_stats['total_revenue']) * 100
    category_stats['avg_revenue_per_product'] = category_stats['total_revenue'] / category_stats['unique_products']
    
    return category_stats


def get_subcategory_analysis(df):
    """
    Analyze product performance by sub-category
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with sub-category analysis
    """
    subcategory_stats = df.groupby(['category', 'sub_category']).agg({
        'product_id': 'nunique',
        'quantity': 'sum',
        'sales': 'sum',
        'order_id': 'count',
        'profit': 'sum'
    }).reset_index()
    
    subcategory_stats.columns = ['category', 'sub_category', 'unique_products', 
                                  'total_quantity', 'total_revenue', 'order_count', 'total_profit']
    subcategory_stats['profit_margin'] = (subcategory_stats['total_profit'] / subcategory_stats['total_revenue']) * 100
    subcategory_stats = subcategory_stats.sort_values('total_revenue', ascending=False)
    
    return subcategory_stats


def get_product_ranking_by_category(df):
    """
    Rank products within each category by sales
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with product rankings
    """
    product_sales = df.groupby(['category', 'product_id', 'product_name']).agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    product_sales.columns = ['category', 'product_id', 'product_name', 'total_revenue', 'total_profit', 'order_count']
    product_sales['profit_margin'] = (product_sales['total_profit'] / product_sales['total_revenue']) * 100
    
    # Rank within each category
    product_sales['rank'] = product_sales.groupby('category')['total_revenue'].rank(ascending=False)
    
    return product_sales.sort_values(['category', 'rank'])


def get_high_revenue_low_profit_products(df):
    """
    Identify products with high revenue but low profit margin
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with high revenue low profit products
    """
    product_stats = df.groupby(['product_id', 'product_name', 'category']).agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    product_stats.columns = ['product_id', 'product_name', 'category', 'total_revenue', 'total_profit', 'order_count']
    product_stats['profit_margin'] = (product_stats['total_profit'] / product_stats['total_revenue']) * 100
    
    # Filter for high revenue (> median) and low profit margin (< 15%)
    median_revenue = product_stats['total_revenue'].median()
    high_revenue_low_profit = product_stats[
        (product_stats['total_revenue'] > median_revenue) & 
        (product_stats['profit_margin'] < 15)
    ].sort_values('total_revenue', ascending=False)
    
    return high_revenue_low_profit


def plot_best_selling_products(product_data):
    """
    Create horizontal bar chart for best-selling products
    
    Args:
        product_data: DataFrame with best-selling products
        
    Returns:
        Plotly figure
    """
    product_data = product_data.sort_values('total_quantity', ascending=True)
    
    fig = px.bar(
        product_data,
        x='total_quantity',
        y='product_name',
        title='Best-Selling Products by Quantity',
        orientation='h',
        color='category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        xaxis_title='Total Quantity Sold',
        yaxis_title='Product Name',
        template='plotly_white',
        height=500,
        legend_title='Category'
    )
    
    return fig


def plot_most_profitable_products(product_data):
    """
    Create horizontal bar chart for most profitable products
    
    Args:
        product_data: DataFrame with most profitable products
        
    Returns:
        Plotly figure
    """
    product_data = product_data.sort_values('total_profit', ascending=True)
    
    fig = px.bar(
        product_data,
        x='total_profit',
        y='product_name',
        title='Most Profitable Products',
        orientation='h',
        color='profit_margin',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        xaxis_title='Total Profit ($)',
        yaxis_title='Product Name',
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    return fig


def plot_category_performance(category_data):
    """
    Create grouped bar chart for category performance
    
    Args:
        category_data: DataFrame with category performance
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=category_data['category'],
        y=category_data['total_revenue'],
        name='Revenue',
        marker_color='#1f77b4'
    ))
    
    fig.add_trace(go.Bar(
        x=category_data['category'],
        y=category_data['total_profit'],
        name='Profit',
        marker_color='#2ca02c'
    ))
    
    fig.update_layout(
        title='Category Performance: Revenue vs Profit',
        xaxis_title='Category',
        yaxis_title='Amount ($)',
        barmode='group',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_subcategory_analysis(subcategory_data):
    """
    Create tree map for sub-category analysis
    
    Args:
        subcategory_data: DataFrame with sub-category data
        
    Returns:
        Plotly figure
    """
    fig = px.treemap(
        subcategory_data,
        path=['category', 'sub_category'],
        values='total_revenue',
        title='Revenue Distribution by Sub-Category',
        color='profit_margin',
        color_continuous_scale='RdYlGn',
        hover_data=['total_quantity', 'order_count']
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500
    )
    
    return fig


def plot_product_profitability_scatter(product_data):
    """
    Create scatter plot for product profitability analysis
    
    Args:
        product_data: DataFrame with product data
        
    Returns:
        Plotly figure
    """
    fig = px.scatter(
        product_data,
        x='total_revenue',
        y='profit_margin',
        color='category',
        size='order_count',
        hover_data=['product_name', 'total_profit'],
        title='Product Profitability Analysis',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Add quadrant lines
    median_revenue = product_data['total_revenue'].median()
    median_margin = product_data['profit_margin'].median()
    
    fig.add_hline(y=median_margin, line_dash="dash", line_color="gray", annotation_text="Avg Margin")
    fig.add_vline(x=median_revenue, line_dash="dash", line_color="gray", annotation_text="Avg Revenue")
    
    fig.update_layout(
        xaxis_title='Total Revenue ($)',
        yaxis_title='Profit Margin (%)',
        template='plotly_white',
        height=500,
        legend_title='Category'
    )
    
    return fig


def plot_low_performing_products(product_data):
    """
    Create horizontal bar chart for low-performing products
    
    Args:
        product_data: DataFrame with low-performing products
        
    Returns:
        Plotly figure
    """
    product_data = product_data.sort_values('total_revenue', ascending=True)
    
    fig = px.bar(
        product_data,
        x='total_revenue',
        y='product_name',
        title='Low-Performing Products by Revenue',
        orientation='h',
        color='profit_margin',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        xaxis_title='Total Revenue ($)',
        yaxis_title='Product Name',
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    return fig
