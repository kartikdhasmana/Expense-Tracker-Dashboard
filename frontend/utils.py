# Helper functions for API calls
import httpx

BASE_URL = "http://localhost:8000"

def make_request(endpoint, method="GET", data=None):
    url = f"{BASE_URL}/{endpoint}"
    if method == "GET":
        response = httpx.get(url)
    elif method == "POST":
        response = httpx.post(url, json=data)
    return response.json()