# FastAPI main entry point
from fastapi import FastAPI
from .database import create_db_and_tables
from dotenv import load_dotenv
import os
from .routers import users, expenses, analytics

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