# Login page
import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth_helper import login

st.title("🔐 Login")

if "token" in st.session_state:
    st.success("✅ You are already logged in!")
    st.info("Use the sidebar to navigate to other pages.")
    if st.button("Logout"):
        del st.session_state["token"]
        st.rerun()
else:
    st.markdown("Please enter your credentials to log in.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username and password:
                login(username, password)
            else:
                st.error("Please enter both username and password.")
    
    st.markdown("---")
    st.markdown("Don't have an account? Go to the **Signup** page.")