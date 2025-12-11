# User routes
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from datetime import datetime, timedelta
from ..database import engine
from ..models import User, OTPVerification
from ..schemas import UserCreate, UserLogin, SendOTPRequest, SendOTPResponse, VerifyOTPSignupRequest
from passlib.context import CryptContext
from ..config import SECRET_KEY, ALGORITHM
from ..email_utils import generate_otp, send_otp_email
from jose import jwt

router = APIRouter()

# Replace bcrypt with argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# OTP expiration time in minutes
OTP_EXPIRE_MINUTES = 10

def get_db():
    with Session(engine) as session:
        yield session

@router.post("/send-otp", response_model=SendOTPResponse)
def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """Send OTP to email for verification"""
    email = request.email.lower().strip()
    
    # Check if email already registered
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered. Please login instead.")
    
    # Delete any existing OTPs for this email
    db.query(OTPVerification).filter(OTPVerification.email == email).delete()
    db.commit()
    
    # Generate new OTP
    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    
    # Save OTP to database
    otp_record = OTPVerification(
        email=email,
        otp=otp,
        expires_at=expires_at
    )
    db.add(otp_record)
    db.commit()
    
    # Send OTP email
    if not send_otp_email(email, otp):
        raise HTTPException(status_code=500, detail="Failed to send OTP email. Please try again.")
    
    return SendOTPResponse(message="OTP sent successfully", email=email)

@router.post("/verify-otp-signup", response_model=dict)
def verify_otp_signup(request: VerifyOTPSignupRequest, db: Session = Depends(get_db)):
    """Verify OTP and create user account"""
    email = request.email.lower().strip()
    
    # Find the OTP record
    otp_record = db.query(OTPVerification).filter(
        OTPVerification.email == email,
        OTPVerification.otp == request.otp,
        OTPVerification.is_verified == False
    ).first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP. Please try again.")
    
    # Check if OTP expired
    if datetime.utcnow() > otp_record.expires_at:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")
    
    # Check if username already taken
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken. Please choose another.")
    
    # Check if email already registered (double check)
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    # Mark OTP as verified
    otp_record.is_verified = True
    db.commit()
    
    # Create user account
    hashed_password = pwd_context.hash(request.password)
    db_user = User(
        email=email,
        username=request.username,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Delete used OTP
    db.delete(otp_record)
    db.commit()
    
    # Generate JWT token (auto login after signup)
    payload = {"sub": str(db_user.id)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "Account created successfully"
    }

@router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
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