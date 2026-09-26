"""
Business Recommendations Page for DataPulse
Automatically generates business insights and recommendations
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
    get_sales_by_region,
    get_sales_by_category,
    get_discount_vs_profit_analysis
)
from analytics.customer_analysis import (
    get_segment_performance,
    get_top_customers
)
from analytics.product_analysis import (
    get_category_analysis,
    get_high_revenue_low_profit_products,
    get_low_performing_products
)


def render(db, filters):
    """Render Business Recommendations page"""
    st.title("💡 Business Recommendations")
    st.markdown("---")
    st.markdown("""
    This page automatically generates actionable business insights based on the data analysis.
    Recommendations are derived from key performance metrics and trends.
    """)
    
    # Get filtered data
    with st.spinner("Analyzing data for recommendations..."):
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
        
        # Get analytics data
        regional_data = get_sales_by_region(df)
        category_data = get_sales_by_category(df)
        discount_data = get_discount_vs_profit_analysis(df)
        segment_data = get_segment_performance(df)
        category_perf = get_category_analysis(df)
        high_rev_low_profit = get_high_revenue_low_profit_products(df)
        low_performing = get_low_performing_products(df)
    
    recommendations = []
    
    # Regional Analysis Recommendations
    if not regional_data.empty:
        best_region = regional_data.iloc[0]['region']
        worst_region = regional_data.iloc[-1]['region']
        best_region_revenue = regional_data.iloc[0]['revenue']
        worst_region_revenue = regional_data.iloc[-1]['revenue']
        
        if best_region_revenue > worst_region_revenue * 2:
            recommendations.append({
                "category": "Regional Performance",
                "priority": "High",
                "insight": f"The {best_region} region is significantly outperforming {worst_region} region (${best_region_revenue:,.0f} vs ${worst_region_revenue:,.0f}).",
                "recommendation": f"Consider investigating successful strategies in {best_region} and replicate them in {worst_region}. Allocate additional marketing budget to underperforming regions.",
                "actionable": True
            })
    
    # Category Performance Recommendations
    if not category_data.empty:
        best_category = category_data.iloc[0]['category']
        worst_category = category_data.iloc[-1]['category']
        best_margin = category_data.iloc[0]['profit_margin']
        worst_margin = category_data.iloc[-1]['profit_margin']
        
        if worst_margin < 15:
            recommendations.append({
                "category": "Category Profitability",
                "priority": "High",
                "insight": f"The {worst_category} category has a low profit margin of {worst_margin:.1f}%.",
                "recommendation": f"Review pricing strategy and cost structure for {worst_category} products. Consider bundling with high-margin products or discontinuing low-margin items.",
                "actionable": True
            })
        
        if best_margin > 25:
            recommendations.append({
                "category": "Category Profitability",
                "priority": "Medium",
                "insight": f"The {best_category} category shows strong profitability with {best_margin:.1f}% margin.",
                "recommendation": f"Increase marketing focus on {best_category} products. Consider expanding product offerings in this high-margin category.",
                "actionable": True
            })
    
    # Discount Analysis Recommendations
    if not discount_data.empty:
        high_discount = discount_data[discount_data['discount_category'].str.contains('High', case=False, na=False)]
        if not high_discount.empty and len(high_discount) > 0:
            high_discount_margin = high_discount.iloc[0]['profit_margin']
            no_discount_data = discount_data[discount_data['discount_category'] == 'No Discount']
            if not no_discount_data.empty:
                no_discount_margin = no_discount_data.iloc[0]['profit_margin']
                
                if high_discount_margin < no_discount_margin - 10:
                    recommendations.append({
                        "category": "Discount Strategy",
                        "priority": "High",
                        "insight": f"High discounts (>20%) are significantly reducing profit margins ({high_discount_margin:.1f}% vs {no_discount_margin:.1f}% for no discount).",
                        "recommendation": "Reevaluate discount strategy. Consider reducing high discount levels and focus on value-based selling instead of price-based promotions.",
                        "actionable": True
                    })
    
    # Segment Performance Recommendations
    if not segment_data.empty:
        best_segment = segment_data.loc[segment_data['revenue_per_customer'].idxmax(), 'segment']
        best_segment_value = segment_data['revenue_per_customer'].max()
        
        recommendations.append({
            "category": "Customer Segment",
            "priority": "Medium",
            "insight": f"The {best_segment} segment generates the highest revenue per customer (${best_segment_value:,.0f}).",
            "recommendation": f"Develop targeted acquisition strategies for {best_segment} customers. Create loyalty programs to retain high-value customers in this segment.",
            "actionable": True
        })
    
    # High Revenue Low Profit Products
    if not high_rev_low_profit.empty:
        recommendations.append({
            "category": "Product Portfolio",
            "priority": "High",
            "insight": f"Found {len(high_rev_low_profit)} products with high revenue but low profit margin (<15%).",
            "recommendation": "Review these products for cost optimization opportunities. Consider price increases or negotiate better supplier terms. Evaluate if these products are strategic loss leaders.",
            "actionable": True
        })
    
    # Low Performing Products
    if not low_performing.empty:
        worst_product = low_performing.iloc[0]['product_name']
        worst_product_revenue = low_performing.iloc[0]['total_revenue']
        
        recommendations.append({
            "category": "Product Portfolio",
            "priority": "Medium",
            "insight": f"The product '{worst_product}' is the lowest performer with only ${worst_product_revenue:,.0f} in revenue.",
            "recommendation": "Evaluate whether to discontinue or reposition this product. Consider bundling with popular items or running targeted promotions to boost sales.",
            "actionable": True
        })
    
    # Display Recommendations
    if recommendations:
        st.subheader("Actionable Business Recommendations")
        
        for i, rec in enumerate(recommendations, 1):
            priority_color = {
                "High": "🔴",
                "Medium": "🟡",
                "Low": "🟢"
            }
            
            with st.expander(f"{priority_color[rec['priority']]} {i}. {rec['category']} - Priority: {rec['priority']}"):
                st.markdown("### 📊 Insight")
                st.info(rec['insight'])
                
                st.markdown("### 💡 Recommendation")
                st.success(rec['recommendation'])
                
                if rec['actionable']:
                    st.markdown("### ✅ Action Items")
                    st.markdown("- [ ] Review this recommendation with the sales team")
                    st.markdown("- [ ] Develop implementation plan")
                    st.markdown("- [ ] Set up tracking metrics")
            
            st.markdown("---")
    else:
        st.info("No specific recommendations generated based on current data patterns.")
    
    # Summary Statistics
    st.subheader("Key Metrics Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not regional_data.empty:
            st.metric("Top Region", regional_data.iloc[0]['region'])
    
    with col2:
        if not category_data.empty:
            st.metric("Top Category", category_data.iloc[0]['category'])
    
    with col3:
        if not segment_data.empty:
            st.metric("Best Segment", segment_data.iloc[0]['segment'])
    
    with col4:
        if not high_rev_low_profit.empty:
            st.metric("Low Margin Products", len(high_rev_low_profit))
        else:
            st.metric("Low Margin Products", 0)
    
    # Detailed Analysis Tables
    st.markdown("---")
    st.subheader("Supporting Data Analysis")
    
    with st.expander("View Regional Performance"):
        if not regional_data.empty:
            st.dataframe(
                regional_data.style.format({
                    'revenue': '${:,.2f}',
                    'profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    with st.expander("View Category Performance"):
        if not category_perf.empty:
            st.dataframe(
                category_perf.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )
    
    with st.expander("View Segment Performance"):
        if not segment_data.empty:
            st.dataframe(
                segment_data.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'avg_order_value': '${:,.2f}',
                    'profit_margin': '{:.2f}%',
                    'revenue_per_customer': '${:,.2f}'
                }),
                use_container_width=True
            )
    
    with st.expander("View High Revenue Low Profit Products"):
        if not high_rev_low_profit.empty:
            st.dataframe(
                high_rev_low_profit.style.format({
                    'total_revenue': '${:,.2f}',
                    'total_profit': '${:,.2f}',
                    'profit_margin': '{:.2f}%'
                }),
                use_container_width=True
            )


if __name__ == "__main__":
    run_page(render, title="Business Recommendations", icon="💡")

