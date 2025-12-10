# List Expenses page
import streamlit as st
import sys
import os
from datetime import date, timedelta
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_helper import authed_request

st.title("📋 List Expenses")

if "token" not in st.session_state:
    st.warning("⚠️ Please log in first to view your expenses.")
    st.stop()

st.markdown("View and filter your expense history.")

# Filter options
st.subheader("🔍 Filters")
col1, col2, col3 = st.columns(3)

with col1:
    category_filter = st.selectbox(
        "Category",
        ["All", "Food", "Transport", "Entertainment", "Shopping", "Bills", "Healthcare", "Other"]
    )

with col2:
    start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))

with col3:
    end_date = st.date_input("End Date", value=date.today())

# Build query parameters
params = {}
if category_filter != "All":
    params["category"] = category_filter
if start_date:
    params["start_date"] = start_date.strftime("%Y-%m-%d")
if end_date:
    params["end_date"] = end_date.strftime("%Y-%m-%d")

# Fetch expenses
if st.button("🔄 Refresh Expenses") or "expenses_loaded" not in st.session_state:
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"http://127.0.0.1:8000/expenses/expenses?{query_string}" if query_string else "http://127.0.0.1:8000/expenses/expenses"
    
    response = authed_request("GET", url)
    
    if response and response.status_code == 200:
        expenses = response.json()
        st.session_state["expenses_data"] = expenses
        st.session_state["expenses_loaded"] = True
    else:
        error_msg = response.json().get("detail", "Unknown error") if response else "No response from server"
        st.error(f"❌ Failed to fetch expenses: {error_msg}")
        st.session_state["expenses_data"] = []

# Display expenses
st.subheader("📊 Your Expenses")
if "expenses_data" in st.session_state and st.session_state["expenses_data"]:
    expenses = st.session_state["expenses_data"]
    df = pd.DataFrame(expenses)
    
    # Reorder columns for better display
    if not df.empty:
        columns_order = ["date", "category", "amount", "note"]
        df = df[[col for col in columns_order if col in df.columns]]
        
        st.dataframe(df, use_container_width=True)
        
        # Summary statistics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Expenses", f"${df['amount'].sum():.2f}")
        with col2:
            st.metric("Number of Entries", len(df))
        with col3:
            st.metric("Average Expense", f"${df['amount'].mean():.2f}")
else:
    st.info("No expenses found. Add some expenses to see them here!")