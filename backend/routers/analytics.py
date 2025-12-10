# Analytics routes
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy import func
from ..database import engine
from ..models import Expense

router = APIRouter()

def get_db():
    with Session(engine) as session:
        yield session

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    total_spend = db.query(func.sum(Expense.amount)).scalar()
    category_summary = db.query(Expense.category, func.sum(Expense.amount)).group_by(Expense.category).all()

    return {
        "total_spend": total_spend,
        "category_summary": category_summary
    }