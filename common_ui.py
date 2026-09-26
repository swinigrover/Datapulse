"""
Common UI components and runner for DataPulse Streamlit pages.
"""

import os
import sys
import streamlit as st

# Ensure project root is in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from database.database import get_database_manager, initialize_database


def load_custom_css():
    """Load styling for consistent look across pages"""
    st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #f5f5f5;
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar(db):
    """Render sidebar with filters and return filter dict"""
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
        """)
        
        return {
            'start_date': min_date,
            'end_date': max_date,
            'region': selected_region if selected_region != "All" else None,
            'category': selected_category if selected_category != "All" else None,
            'segment': selected_segment if selected_segment != "All" else None
        }


def run_page(render_func, title="DataPulse", icon="📊"):
    """Helper to run a page standalone when clicked directly in Streamlit page navigation"""
    st.set_page_config(
        page_title=f"{title} - DataPulse",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    load_custom_css()
    db = get_database_manager()
    filters = render_sidebar(db)
    render_func(db, filters)
