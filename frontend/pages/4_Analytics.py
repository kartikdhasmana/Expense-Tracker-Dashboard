# Analytics page
import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_helper import authed_request

st.title("📈 Analytics Dashboard")

if "token" not in st.session_state:
    st.warning("⚠️ Please log in first to view analytics.")
    st.stop()

st.markdown("Visualize your spending patterns and insights.")

# Fetch analytics data
response = authed_request("GET", "http://127.0.0.1:8000/analytics/analytics")

if response and response.status_code == 200:
    data = response.json()
    total_spend = data.get("total_spend", 0) or 0
    category_summary = data.get("category_summary", [])
    
    # Display total spend
    st.subheader("💰 Total Spending")
    st.metric("Total Amount Spent", f"${total_spend:.2f}")
    
    st.markdown("---")
    
    if category_summary:
        # Convert to DataFrame
        df = pd.DataFrame(category_summary, columns=["Category", "Amount"])
        
        # Display metrics by category
        st.subheader("📊 Spending by Category")
        
        cols = st.columns(min(len(df), 4))
        for idx, row in df.iterrows():
            with cols[idx % 4]:
                percentage = (row["Amount"] / total_spend * 100) if total_spend > 0 else 0
                st.metric(row["Category"], f"${row['Amount']:.2f}", f"{percentage:.1f}%")
        
        st.markdown("---")
        
        # Pie Chart
        st.subheader("🥧 Spending Distribution")
        fig_pie = px.pie(
            df, 
            values="Amount", 
            names="Category",
            title="Expense Distribution by Category",
            hole=0.3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Bar Chart
        st.subheader("📊 Category Comparison")
        fig_bar = px.bar(
            df,
            x="Category",
            y="Amount",
            title="Spending by Category",
            color="Category",
            text="Amount"
        )
        fig_bar.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    else:
        st.info("No expense data available yet. Add some expenses to see analytics!")
        
else:
    error_msg = response.json().get("detail", "Unknown error") if response else "No response from server"
    st.error(f"❌ Failed to fetch analytics: {error_msg}")