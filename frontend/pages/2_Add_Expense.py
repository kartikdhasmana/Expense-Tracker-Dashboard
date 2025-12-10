# Add Expense page
import streamlit as st

st.title("Add Expense")
date = st.date_input("Date")
category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Other"])
amount = st.number_input("Amount", min_value=0.0)
note = st.text_area("Note")
if st.button("Add Expense"):
    st.success("Expense added successfully")