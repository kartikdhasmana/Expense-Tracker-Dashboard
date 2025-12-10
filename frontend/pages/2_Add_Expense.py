# Add Expense page
import streamlit as st
import sys
import os
from datetime import date

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_helper import authed_request

st.title("➕ Add Expense")

# Debug: Show token status (uncomment to debug)
# st.write("Debug - Token exists:", "token" in st.session_state)

if "token" not in st.session_state:
    st.warning("⚠️ Please log in first to add expenses.")
    st.info("Go to the **Login** page from the sidebar to log in.")
    st.stop()

# Show logged in status
st.sidebar.success("✅ Logged in")

st.markdown("Fill in the details below to add a new expense.")

with st.form("add_expense_form"):
    expense_date = st.date_input("Date", value=date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Healthcare", "Other"])
    amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
    note = st.text_area("Note (optional)")
    
    submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        if amount <= 0:
            st.error("Please enter a valid amount greater than 0.")
        else:
            payload = {
                "date": expense_date.strftime("%Y-%m-%d"),
                "category": category,
                "amount": amount,
                "note": note if note else None
            }
            
            response = authed_request(
                "POST",
                "http://127.0.0.1:8000/expenses/expenses",
                json=payload
            )
            
            if response and response.status_code == 200:
                st.success("✅ Expense added successfully!")
                st.balloons()
            elif response:
                error_msg = response.json().get("detail", "Unknown error")
                st.error(f"❌ Failed to add expense: {error_msg}")
            else:
                st.error("❌ No response from server. Please check if the backend is running.")