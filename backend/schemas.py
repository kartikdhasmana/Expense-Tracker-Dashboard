# Pydantic schemas
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class ExpenseCreate(BaseModel):
    date: str
    category: str
    amount: float
    note: Optional[str]

class ExpenseResponse(BaseModel):
    id: int
    date: str
    category: str
    amount: float
    note: Optional[str]
    
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    sub: Optional[int]