# Expense Tracker Dashboard

## Overview
A simple expense tracker application built using FastAPI for the backend and Streamlit for the frontend.

## Features
- User Login
- Add Expenses
- List & Filter Expenses
- Analytics Dashboard

## Tech Stack
- **Backend**: FastAPI, SQLite, SQLModel, JWT
- **Frontend**: Streamlit, Plotly, httpx

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the backend:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. Run the frontend:
   ```bash
   streamlit run frontend/app.py
   ```