"""
DataPulse - Business Intelligence & Sales Analytics Platform
Main Application File
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import get_database_manager, initialize_database

# Page configuration
st.set_page_config(
    page_title="DataPulse - Business Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling that respects both light and dark themes
def load_custom_css():
    st.markdown("""
    <style>
    .metric-card {
        background-color: var(--secondary-background-color, rgba(128, 128, 128, 0.05));
        color: var(--text-color);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.15);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def init_db():
    """Initialize database connection"""
    try:
        db = initialize_database()
        return db
    except Exception as e:
        st.error(f"Error initializing database: {e}")
        return None

# Sidebar filters
def render_sidebar(db):
    """Render sidebar with filters"""
    with st.sidebar:
        st.title("📊 DataPulse")
        st.markdown("---")
        
        # Get filter options
        filter_options = db.get_filter_options()
        
        # Date range filter
        st.subheader("📅 Date Range")
        min_date = st.date_input("Start Date", value=None)
        max_date = st.date_input("End Date", value=None)
        
        # Region filter
        st.subheader("🌍 Region")
        regions = filter_options.get('regions', [])
        selected_region = st.selectbox("Select Region", ["All"] + regions)
        
        # Category filter
        st.subheader("📦 Category")
        categories = filter_options.get('categories', [])
        selected_category = st.selectbox("Select Category", ["All"] + categories)
        
        # Segment filter
        st.subheader("👥 Customer Segment")
        segments = filter_options.get('segments', [])
        selected_segment = st.selectbox("Select Segment", ["All"] + segments)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **DataPulse** is a comprehensive Business Intelligence platform for sales analytics.
        
        Features:
        - Executive Dashboard
        - Sales Analytics
        - Customer Insights
        - Product Analysis
        - SQL Query Explorer
        - Business Recommendations
        """)
        
        return {
            'start_date': min_date,
            'end_date': max_date,
            'region': selected_region if selected_region != "All" else None,
            'category': selected_category if selected_category != "All" else None,
            'segment': selected_segment if selected_segment != "All" else None
        }

# Main application
def main():
    """Main application function"""
    load_custom_css()
    
    # Initialize database
    db = init_db()
    
    if db is None:
        st.error("Failed to initialize database. Please check your configuration.")
        return
    
    # Render sidebar with filters
    filters = render_sidebar(db)
    
    # Store filters in session state
    st.session_state.filters = filters
    
    # Page navigation
    page = st.sidebar.radio(
        "Navigate to:",
        [
            "🏠 Executive Overview",
            "📈 Sales Analytics",
            "👥 Customer Analytics",
            "📦 Product Analytics",
            "💻 SQL Insights",
            "💡 Business Recommendations"
        ]
    )
    
    # Render selected page
    if page == "🏠 Executive Overview":
        import pages.page_Executive_Overview as EO
        EO.render(db, filters)
    elif page == "📈 Sales Analytics":
        import pages.page_Sales_Analytics as SA
        SA.render(db, filters)
    elif page == "👥 Customer Analytics":
        import pages.page_Customer_Analytics as CA
        CA.render(db, filters)
    elif page == "📦 Product Analytics":
        import pages.page_Product_Analytics as PA
        PA.render(db, filters)
    elif page == "💻 SQL Insights":
        import pages.page_SQL_Insights as SI
        SI.render(db, filters)
    elif page == "💡 Business Recommendations":
        import pages.page_Business_Recommendations as BR
        BR.render(db, filters)

if __name__ == "__main__":
    main()
