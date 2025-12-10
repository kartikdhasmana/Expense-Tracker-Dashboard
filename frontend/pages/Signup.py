import streamlit as st
import requests

st.title("📝 Signup")

if "token" in st.session_state:
    st.success("✅ You are already logged in!")
    st.info("Use the sidebar to navigate to other pages.")
else:
    st.markdown("Create a new account to get started.")
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if not username or not password:
                st.error("Please fill in all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif len(password) < 4:
                st.error("Password must be at least 4 characters long.")
            else:
                response = requests.post(
                    "http://127.0.0.1:8000/users/signup",
                    json={"username": username, "password": password}
                )
                if response.status_code == 200:
                    st.success("✅ Signup successful! Please go to the Login page.")
                else:
                    st.error(f"❌ Signup failed: {response.json().get('detail', 'Unknown error')}")
    
    st.markdown("---")
    st.markdown("Already have an account? Go to the **Login** page.")