from sqlmodel import SQLModel, create_engine
import logging
from .models import User, Expense  # Ensure models are imported

# Database URL from environment variables or default
DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        logging.info("Database and tables created successfully.")
        logging.info(f"Registered tables: {list(SQLModel.metadata.tables.keys())}")
    except Exception as e:
        logging.error(f"Error creating database and tables: {e}")