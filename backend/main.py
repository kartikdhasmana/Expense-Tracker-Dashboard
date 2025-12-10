# FastAPI main entry point
from fastapi import FastAPI
from .database import create_db_and_tables
from dotenv import load_dotenv
import os
from .routers import users, expenses, analytics
from fastapi.openapi.utils import get_openapi

# Load environment variables
load_dotenv()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Expense Tracker API"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Expense Tracker API",
        version="1.0.0",
        description="API for managing expenses, users, and analytics.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/users/login",
                    "scopes": {}
                }
            }
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi