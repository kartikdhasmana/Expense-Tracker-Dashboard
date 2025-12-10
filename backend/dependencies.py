from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from backend.schemas import TokenData
from sqlmodel import Session
from backend.models import User

# Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Extracts the user ID from the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")