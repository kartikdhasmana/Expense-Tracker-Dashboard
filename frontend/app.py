import streamlit as st

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Expense Tracker Dashboard")

st.markdown("""
Welcome to the **Expense Tracker Dashboard**! 

This application helps you manage and analyze your personal expenses.

## Getting Started

1. **Sign Up** - Create a new account if you don't have one
2. **Login** - Log in to access your dashboard
3. **Add Expenses** - Track your daily expenses
4. **List Expenses** - View and filter your expense history
5. **Analytics** - Visualize your spending patterns

---

### Navigation
Use the **sidebar** on the left to navigate between pages.
""")

# Display login status in sidebar
if "token" in st.session_state:
    st.sidebar.success("✅ You are logged in")
    if st.sidebar.button("Logout"):
        del st.session_state["token"]
        st.rerun()
else:
    st.sidebar.warning("⚠️ Please log in to access all features")