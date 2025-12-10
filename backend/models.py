# SQLModel models
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str
    category: str
    amount: float
    note: Optional[str]
    user_id: int = Field(foreign_key="user.id")