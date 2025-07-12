from app.models.user import User, SubscriptionTier
from app.core.utils import generate_otp
from app.core.security import create_access_token
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.config import settings
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

def signup_user(mobile_number: str):
    db = get_db()
    try:
        user = db.query(User).filter(User.mobile_number == mobile_number).first()
        if not user:
            user = User(mobile_number=mobile_number)
            db.add(user)
            db.commit()
            db.refresh(user)
        return {"message": "User registered"}
    finally:
        db.close()

def send_otp(mobile_number: str):
    db = get_db()
    try:
        otp = generate_otp()
        user = db.query(User).filter(User.mobile_number == mobile_number).first()
        if not user:
            raise Exception("User not found")
        user.otp = otp
        user.otp_generated_at = datetime.utcnow()
        db.commit()
        return {"otp": otp}  # For testing/demo
    finally:
        db.close()

def verify_otp_token(mobile_number: str, otp: str):
    db = get_db()
    try:
        user = db.query(User).filter(User.mobile_number == mobile_number, User.otp == otp).first()
        if not user:
            return None
        user.is_verified = True
        user.otp = None
        db.commit()
        return create_access_token({"sub": str(user.id)})
    finally:
        db.close()
