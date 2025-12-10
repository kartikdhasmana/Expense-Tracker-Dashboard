import streamlit as st
import requests
import json

# Login function
def login(username, password):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/users/login",
            json={"username": username, "password": password}  # Send JSON data
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            st.session_state["token"] = token
            st.success("Login successful!")
            st.rerun()  # Rerun to update session state across pages
        else:
            error_message = response.json().get("detail", "Login failed. Please check your credentials.")
            st.error(f"Error: {error_message}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Helper function for authenticated requests
def authed_request(method, url, **kwargs):
    if "token" not in st.session_state:
        st.error("You are not logged in. Please log in first.")
        return None

    headers = kwargs.get("headers", {})
    headers["Authorization"] = f"Bearer {st.session_state['token']}"
    kwargs["headers"] = headers

    try:
        response = requests.request(method, url, **kwargs)
        return response
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Make sure uvicorn is running on http://127.0.0.1:8000")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request error: {e}")
        return None