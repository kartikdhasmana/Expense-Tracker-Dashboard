# Expense routes
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import List, Optional
from datetime import date
from ..database import engine
from ..models import Expense
from ..schemas import ExpenseCreate
from ..dependencies import get_current_user_id

router = APIRouter()

def get_db():
    with Session(engine) as session:
        yield session

@router.post("/expenses", response_model=ExpenseCreate)
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_expense = Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/expenses", response_model=List[ExpenseCreate])
def list_expenses(
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    query = db.query(Expense).filter(Expense.user_id == user_id)

    if category:
        query = query.filter(Expense.category == category)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    return query.all()