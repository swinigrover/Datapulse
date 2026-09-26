"""
Database Module for DataPulse
Handles database connections, data loading, and query execution
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st


class DatabaseManager:
    """Manages database operations for DataPulse"""
    
    def __init__(self, use_postgres=False):
        """
        Initialize database connection
        
        Args:
            use_postgres: If True, use PostgreSQL. If False, use SQLite
        """
        self.use_postgres = use_postgres
        self.engine = None
        self._connect()
    
    def _connect(self):
        """Establish database connection"""
        try:
            if self.use_postgres:
                # PostgreSQL connection
                db_user = os.getenv('DB_USER', 'postgres')
                db_password = os.getenv('DB_PASSWORD', 'password')
                db_host = os.getenv('DB_HOST', 'localhost')
                db_port = os.getenv('DB_PORT', '5432')
                db_name = os.getenv('DB_NAME', 'datapulse')
                
                connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
                self.engine = create_engine(connection_string)
            else:
                # SQLite connection (default for easy deployment)
                db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'datapulse.db')
                self.engine = create_engine(f'sqlite:///{db_path}')
            
            print(f"Connected to {'PostgreSQL' if self.use_postgres else 'SQLite'} database")
            
        except SQLAlchemyError as e:
            st.error(f"Database connection error: {e}")
            raise
    
    def load_data_from_csv(self):
        """Load data from CSV files into database"""
        try:
            # Read CSV files
            orders_df = pd.read_csv('data/sales_data.csv')
            customers_df = pd.read_csv('data/customers.csv')
            products_df = pd.read_csv('data/products.csv')
            
            # Load into database
            orders_df.to_sql('orders', self.engine, if_exists='replace', index=False)
            customers_df.to_sql('customers', self.engine, if_exists='replace', index=False)
            products_df.to_sql('products', self.engine, if_exists='replace', index=False)
            
            print("Data loaded successfully from CSV files")
            return True
            
        except Exception as e:
            st.error(f"Error loading data from CSV: {e}")
            return False
    
    def execute_query(self, query):
        """
        Execute SQL query and return results as DataFrame
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with query results
        """
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql_query(text(query), conn)
            return df
        except SQLAlchemyError as e:
            st.error(f"Query execution error: {e}")
            return pd.DataFrame()
    
    def get_orders_data(self, start_date=None, end_date=None, region=None, category=None, segment=None):
        """
        Get orders data with optional filters
        
        Args:
            start_date: Filter orders from this date
            end_date: Filter orders until this date
            region: Filter by region
            category: Filter by category
            segment: Filter by customer segment
            
        Returns:
            DataFrame with filtered orders data
        """
        query = """
        SELECT o.*, c.customer_name, c.segment, c.city, c.state, p.product_name, p.unit_price
        FROM orders o
        INNER JOIN customers c ON o.customer_id = c.customer_id
        INNER JOIN products p ON o.product_id = p.product_id
        WHERE 1=1
        """
        
        params = {}
        
        if start_date:
            query += " AND o.order_date >= :start_date"
            params['start_date'] = start_date
        
        if end_date:
            query += " AND o.order_date <= :end_date"
            params['end_date'] = end_date
        
        if region:
            query += " AND o.region = :region"
            params['region'] = region
        
        if category:
            query += " AND o.category = :category"
            params['category'] = category
        
        if segment:
            query += " AND c.segment = :segment"
            params['segment'] = segment
        
        return self.execute_query(query)
    
    def get_kpis(self, start_date=None, end_date=None, region=None, category=None, segment=None):
        """
        Calculate key performance indicators
        
        Returns:
            Dictionary with KPI values
        """
        query = """
        SELECT 
            COUNT(DISTINCT order_id) as total_orders,
            SUM(sales) as total_revenue,
            SUM(profit) as total_profit,
            COUNT(DISTINCT customer_id) as total_customers,
            AVG(sales) as avg_order_value
        FROM orders o
        INNER JOIN customers c ON o.customer_id = c.customer_id
        WHERE 1=1
        """
        
        params = {}
        
        if start_date:
            query += " AND o.order_date >= :start_date"
            params['start_date'] = start_date
        
        if end_date:
            query += " AND o.order_date <= :end_date"
            params['end_date'] = end_date
        
        if region:
            query += " AND o.region = :region"
            params['region'] = region
        
        if category:
            query += " AND o.category = :category"
            params['category'] = category
        
        if segment:
            query += " AND c.segment = :segment"
            params['segment'] = segment
        
        df = self.execute_query(query)
        
        if not df.empty:
            kpis = {
                'total_orders': int(df.iloc[0]['total_orders']),
                'total_revenue': float(df.iloc[0]['total_revenue']),
                'total_profit': float(df.iloc[0]['total_profit']),
                'total_customers': int(df.iloc[0]['total_customers']),
                'avg_order_value': float(df.iloc[0]['avg_order_value'])
            }
            
            # Calculate profit margin
            if kpis['total_revenue'] > 0:
                kpis['profit_margin'] = (kpis['total_profit'] / kpis['total_revenue']) * 100
            else:
                kpis['profit_margin'] = 0
            
            return kpis
        
        return {
            'total_orders': 0,
            'total_revenue': 0,
            'total_profit': 0,
            'total_customers': 0,
            'avg_order_value': 0,
            'profit_margin': 0
        }
    
    def get_filter_options(self):
        """
        Get available filter options from database
        
        Returns:
            Dictionary with filter options
        """
        regions = self.execute_query("SELECT DISTINCT region FROM orders ORDER BY region")
        categories = self.execute_query("SELECT DISTINCT category FROM orders ORDER BY category")
        segments = self.execute_query("SELECT DISTINCT segment FROM customers ORDER BY segment")
        
        return {
            'regions': regions['region'].tolist() if not regions.empty else [],
            'categories': categories['category'].tolist() if not categories.empty else [],
            'segments': segments['segment'].tolist() if not segments.empty else []
        }
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            print("Database connection closed")


# Singleton instance for the application
_db_manager = None


def get_database_manager(use_postgres=False):
    """
    Get or create database manager instance
    
    Args:
        use_postgres: If True, use PostgreSQL
        
    Returns:
        DatabaseManager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(use_postgres)
    return _db_manager


def initialize_database():
    """Initialize database with data from CSV files"""
    db = get_database_manager()
    db.load_data_from_csv()
    return db
