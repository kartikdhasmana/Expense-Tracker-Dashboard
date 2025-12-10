# Analytics routes
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy import func
from ..database import engine
from ..models import Expense
from ..dependencies import get_current_user_id

router = APIRouter()

def get_db():
    with Session(engine) as session:
        yield session

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    # Get total spend for the current user
    total_spend = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).scalar() or 0
    
    # Get category summary for the current user
    category_results = db.query(
        Expense.category, 
        func.sum(Expense.amount)
    ).filter(Expense.user_id == user_id).group_by(Expense.category).all()
    
    # Convert Row objects to list of lists for JSON serialization
    category_summary = [[row[0], row[1]] for row in category_results]

    return {
        "total_spend": total_spend,
        "category_summary": category_summary
    }