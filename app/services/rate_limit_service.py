from app.models.user import User, SubscriptionTier
from app.models.subscription import UserUsage
from app.database import SessionLocal
from datetime import datetime, date
from sqlalchemy import func

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def check_rate_limit(user_id: int) -> bool:
    """
    Check if user has exceeded their daily message limit
    Returns True if user can send message, False if limit exceeded
    """
    db = get_db()
    try:
        # Get user subscription tier
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return False
        
        # Pro users have unlimited messages
        if user.subscription == SubscriptionTier.PRO:
            return True
        
        # Basic users have daily limit
        today = date.today()
        usage = db.query(UserUsage).filter(
            UserUsage.user_id == user_id,
            func.date(UserUsage.date) == today
        ).first()
        
        if not usage:
            # First message of the day
            usage = UserUsage(user_id=user_id, message_count=0, daily_limit=5)
            db.add(usage)
            db.commit()
            return True
        
        # Check if limit exceeded
        if usage.message_count >= usage.daily_limit:
            return False
        
        return True
    finally:
        db.close()

def increment_message_count(user_id: int):
    """Increment the daily message count for a user"""
    db = get_db()
    try:
        today = date.today()
        usage = db.query(UserUsage).filter(
            UserUsage.user_id == user_id,
            func.date(UserUsage.date) == today
        ).first()
        
        if usage:
            usage.message_count += 1
        else:
            usage = UserUsage(user_id=user_id, message_count=1, daily_limit=5)
            db.add(usage)
        
        db.commit()
    finally:
        db.close()

def get_user_usage(user_id: int) -> dict:
    """Get current user's usage statistics"""
    db = get_db()
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found"}
        
        today = date.today()
        usage = db.query(UserUsage).filter(
            UserUsage.user_id == user_id,
            func.date(UserUsage.date) == today
        ).first()
        
        if user.subscription == SubscriptionTier.PRO:
            return {
                "tier": "pro",
                "daily_limit": "unlimited",
                "used_today": usage.message_count if usage else 0,
                "remaining": "unlimited"
            }
        else:
            used_today = usage.message_count if usage else 0
            remaining = max(0, 5 - used_today)
            return {
                "tier": "basic",
                "daily_limit": 5,
                "used_today": used_today,
                "remaining": remaining
            }
    finally:
        db.close() 