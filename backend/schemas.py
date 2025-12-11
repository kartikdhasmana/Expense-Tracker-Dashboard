# Pydantic schemas
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class SendOTPRequest(BaseModel):
    email: str

class SendOTPResponse(BaseModel):
    message: str
    email: str

class VerifyOTPSignupRequest(BaseModel):
    email: str
    otp: str
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