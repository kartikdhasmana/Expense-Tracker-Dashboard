# User routes
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from ..database import engine
from ..models import User
from ..schemas import UserCreate
from passlib.context import CryptContext
from ..config import SECRET_KEY, ALGORITHM
from jose import jwt

router = APIRouter()

# Replace bcrypt with argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_db():
    with Session(engine) as session:
        yield session

@router.post("/signup", response_model=UserCreate)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Truncate password to 72 characters to comply with bcrypt limitations
    truncated_password = user.password[:72]
    hashed_password = pwd_context.hash(truncated_password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=dict)
def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid username or password. Please try again.")

        # Generate JWT token (sub must be a string per JWT spec)
        payload = {"sub": str(db_user.id)}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print("Error during login:", str(e))  # Debug log for errors
        raise