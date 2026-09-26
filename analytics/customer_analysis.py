"""
Customer Analysis Module for DataPulse
Provides functions for customer analytics and insights
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_customer_segmentation(df):
    """
    Analyze customer segmentation by order count and revenue
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with customer segmentation
    """
    customer_stats = df.groupby('customer_id').agg({
        'customer_name': 'first',
        'segment': 'first',
        'order_id': 'count',
        'sales': 'sum',
        'profit': 'sum'
    }).reset_index()
    
    customer_stats.columns = ['customer_id', 'customer_name', 'segment', 'order_count', 'total_spent', 'total_profit']
    
    # Classify customers based on order count
    customer_stats['customer_type'] = pd.cut(
        customer_stats['order_count'],
        bins=[0, 1, 5, float('inf')],
        labels=['One-time', 'Occasional', 'Loyal']
    )
    
    return customer_stats


def get_top_customers(df, n=10):
    """
    Get top N customers by revenue
    
    Args:
        df: DataFrame with orders data
        n: Number of top customers to return
        
    Returns:
        DataFrame with top customers
    """
    customer_revenue = df.groupby(['customer_id', 'customer_name', 'segment']).agg({
        'sales': 'sum',
        'order_id': 'count',
        'profit': 'sum'
    }).reset_index()
    
    customer_revenue.columns = ['customer_id', 'customer_name', 'segment', 'total_revenue', 'order_count', 'total_profit']
    customer_revenue['avg_order_value'] = customer_revenue['total_revenue'] / customer_revenue['order_count']
    customer_revenue = customer_revenue.sort_values('total_revenue', ascending=False).head(n)
    
    return customer_revenue


def get_repeat_customer_analysis(df):
    """
    Analyze repeat customer behavior
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with repeat customer analysis
    """
    customer_orders = df.groupby('customer_id').agg({
        'order_id': 'count',
        'sales': 'sum'
    }).reset_index()
    
    customer_orders.columns = ['customer_id', 'order_count', 'total_spent']
    
    # Classify customers
    customer_orders['customer_type'] = pd.cut(
        customer_orders['order_count'],
        bins=[0, 1, 2, 5, float('inf')],
        labels=['One-time', 'Repeat (2)', 'Regular (3-5)', 'Loyal (5+)']
    )
    
    # Get summary statistics
    summary = customer_orders.groupby('customer_type').agg({
        'customer_id': 'count',
        'total_spent': 'sum',
        'order_count': 'sum'
    }).reset_index()
    
    summary.columns = ['customer_type', 'customer_count', 'total_revenue', 'total_orders']
    summary['avg_revenue_per_customer'] = summary['total_revenue'] / summary['customer_count']
    summary['percentage'] = (summary['customer_count'] / summary['customer_count'].sum()) * 100
    
    return summary


def get_customer_lifetime_value(df):
    """
    Calculate customer lifetime value (CLV)
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with CLV calculations
    """
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    customer_stats = df.groupby('customer_id').agg({
        'customer_name': 'first',
        'segment': 'first',
        'order_id': 'count',
        'sales': 'sum',
        'profit': 'sum',
        'order_date': ['min', 'max']
    }).reset_index()
    
    customer_stats.columns = ['customer_id', 'customer_name', 'segment', 'order_count', 
                              'total_spent', 'total_profit', 'first_purchase', 'last_purchase']
    
    # Calculate days active
    customer_stats['days_active'] = (customer_stats['last_purchase'] - customer_stats['first_purchase']).dt.days + 1
    
    # Calculate average order value
    customer_stats['avg_order_value'] = customer_stats['total_spent'] / customer_stats['order_count']
    
    # Calculate estimated annual value (simple CLV)
    customer_stats['annual_value'] = (customer_stats['total_spent'] / customer_stats['days_active']) * 365
    
    customer_stats = customer_stats.sort_values('total_spent', ascending=False)
    
    return customer_stats


def get_geographic_customer_distribution(df):
    """
    Analyze geographic distribution of customers
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with geographic distribution
    """
    geo_data = df.groupby(['region', 'state', 'city']).agg({
        'customer_id': 'nunique',
        'sales': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    geo_data.columns = ['region', 'state', 'city', 'unique_customers', 'total_revenue', 'order_count']
    geo_data = geo_data.sort_values('total_revenue', ascending=False)
    
    return geo_data


def get_segment_performance(df):
    """
    Analyze performance by customer segment
    
    Args:
        df: DataFrame with orders data
        
    Returns:
        DataFrame with segment performance
    """
    segment_data = df.groupby('segment').agg({
        'customer_id': 'nunique',
        'order_id': 'count',
        'sales': 'sum',
        'profit': 'sum'
    }).reset_index()
    
    segment_data.columns = ['segment', 'unique_customers', 'total_orders', 'total_revenue', 'total_profit']
    segment_data['avg_order_value'] = segment_data['total_revenue'] / segment_data['total_orders']
    segment_data['profit_margin'] = (segment_data['total_profit'] / segment_data['total_revenue']) * 100
    segment_data['revenue_per_customer'] = segment_data['total_revenue'] / segment_data['unique_customers']
    
    return segment_data


def plot_customer_segmentation(customer_stats):
    """
    Create pie chart for customer segmentation
    
    Args:
        customer_stats: DataFrame with customer segmentation
        
    Returns:
        Plotly figure
    """
    segment_counts = customer_stats['customer_type'].value_counts().reset_index()
    segment_counts.columns = ['customer_type', 'count']
    
    fig = px.pie(
        segment_counts,
        values='count',
        names='customer_type',
        title='Customer Segmentation by Purchase Frequency',
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


def plot_top_customers(customer_data):
    """
    Create horizontal bar chart for top customers
    
    Args:
        customer_data: DataFrame with top customers
        
    Returns:
        Plotly figure
    """
    customer_data = customer_data.sort_values('total_revenue', ascending=True)
    
    fig = px.bar(
        customer_data,
        x='total_revenue',
        y='customer_name',
        title='Top 10 Customers by Revenue',
        orientation='h',
        color='segment',
        color_discrete_map={
            'Consumer': '#1f77b4',
            'Corporate': '#ff7f0e',
            'Home Office': '#2ca02c'
        }
    )
    
    fig.update_layout(
        xaxis_title='Total Revenue ($)',
        yaxis_title='Customer Name',
        template='plotly_white',
        height=500,
        legend_title='Segment'
    )
    
    return fig


def plot_repeat_customer_analysis(summary_data):
    """
    Create bar chart for repeat customer analysis
    
    Args:
        summary_data: DataFrame with repeat customer summary
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=summary_data['customer_type'],
        y=summary_data['customer_count'],
        name='Customer Count',
        marker_color='#1f77b4'
    ))
    
    fig.add_trace(go.Bar(
        x=summary_data['customer_type'],
        y=summary_data['total_revenue'] / 1000,
        name='Total Revenue (K$)',
        marker_color='#2ca02c'
    ))
    
    fig.update_layout(
        title='Repeat Customer Analysis',
        xaxis_title='Customer Type',
        yaxis_title='Count / Revenue (K$)',
        barmode='group',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_geographic_distribution(geo_data):
    """
    Create tree map for geographic distribution
    
    Args:
        geo_data: DataFrame with geographic data
        
    Returns:
        Plotly figure
    """
    fig = px.treemap(
        geo_data.head(20),
        path=['region', 'state', 'city'],
        values='total_revenue',
        title='Geographic Distribution of Revenue',
        color='total_revenue',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500
    )
    
    return fig


def plot_segment_performance(segment_data):
    """
    Create grouped bar chart for segment performance
    
    Args:
        segment_data: DataFrame with segment performance
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=segment_data['segment'],
        y=segment_data['total_revenue'],
        name='Total Revenue',
        marker_color='#1f77b4'
    ))
    
    fig.add_trace(go.Bar(
        x=segment_data['segment'],
        y=segment_data['total_profit'],
        name='Total Profit',
        marker_color='#2ca02c'
    ))
    
    fig.update_layout(
        title='Performance by Customer Segment',
        xaxis_title='Segment',
        yaxis_title='Amount ($)',
        barmode='group',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_customer_lifetime_value(clv_data):
    """
    Create scatter plot for customer lifetime value
    
    Args:
        clv_data: DataFrame with CLV data
        
    Returns:
        Plotly figure
    """
    fig = px.scatter(
        clv_data.head(50),
        x='order_count',
        y='total_spent',
        color='segment',
        size='annual_value',
        hover_data=['customer_name', 'avg_order_value'],
        title='Customer Lifetime Value Analysis',
        color_discrete_map={
            'Consumer': '#1f77b4',
            'Corporate': '#ff7f0e',
            'Home Office': '#2ca02c'
        }
    )
    
    fig.update_layout(
        xaxis_title='Order Count',
        yaxis_title='Total Spent ($)',
        template='plotly_white',
        height=500,
        legend_title='Segment'
    )
    
    return fig
