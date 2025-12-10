# Streamlit main entry point
import streamlit as st

st.title("Expense Tracker Dashboard")
st.sidebar.header("Navigation")
st.sidebar.selectbox("Go to:", ["Login", "Add Expense", "List Expenses", "Analytics"])