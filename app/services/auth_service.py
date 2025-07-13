from app.models.user import User, SubscriptionTier
from app.core.utils import generate_otp
from app.core.security import create_access_token, verify_password, get_password_hash
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

def signup_user(mobile_number: str, password: str):
    db = get_db()
    try:
        user = db.query(User).filter(User.mobile_number == mobile_number).first()
        if not user:
            user = User(mobile_number=mobile_number, hashed_password=get_password_hash(password))
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # If user exists but doesn't have a password, update it
            if not user.hashed_password:
                user.hashed_password = get_password_hash(password)
                db.commit()
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
        user.otp_generated_at = datetime.now(timezone.utc)
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
        
        # Check if OTP is expired (15 minutes)
        if user.otp_generated_at and datetime.now(timezone.utc) - user.otp_generated_at > timedelta(minutes=15):
            return None
            
        user.is_verified = True
        user.otp = None
        db.commit()
        return create_access_token({"sub": str(user.id)})
    finally:
        db.close()

def send_forgot_password_otp(mobile_number: str):
    """Send OTP for password reset"""
    db = get_db()
    try:
        otp = generate_otp()
        user = db.query(User).filter(User.mobile_number == mobile_number).first()
        if not user:
            raise Exception("User not found")
        
        user.otp = otp
        user.otp_generated_at = datetime.now(timezone.utc)
        db.commit()
        return {"otp": otp, "message": "Password reset OTP sent"}
    finally:
        db.close()

def change_password(user_id: int, old_password: str, new_password: str):
    """Change user password"""
    db = get_db()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise Exception("User not found")
        
        if not user.hashed_password:
            raise Exception("No password set for this user")
        
        if not verify_password(old_password, user.hashed_password):
            raise Exception("Invalid old password")
        
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        return {"message": "Password changed successfully"}
    finally:
        db.close()

def reset_password_with_otp(mobile_number: str, otp: str, new_password: str):
    """Reset password using OTP"""
    db = get_db()
    try:
        user = db.query(User).filter(User.mobile_number == mobile_number, User.otp == otp).first()
        if not user:
            raise Exception("Invalid OTP")
        
        # Check if OTP is expired (15 minutes)
        if user.otp_generated_at and datetime.now(timezone.utc) - user.otp_generated_at > timedelta(minutes=15):
            raise Exception("OTP expired")
        
        user.hashed_password = get_password_hash(new_password)
        user.otp = None
        db.commit()
        return {"message": "Password reset successfully"}
    finally:
        db.close()
