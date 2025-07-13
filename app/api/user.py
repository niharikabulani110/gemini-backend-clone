from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserResponse
from app.models.user import User
from app.core.security import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import SessionLocal
from app.services.rate_limit_service import get_user_usage

auth_scheme = HTTPBearer()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> int:
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.get("/me", response_model=UserResponse)
def get_user_profile(user_id: int = Depends(get_user_id)):
    """Get current user's profile information"""
    db = get_db()
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        db.close()

@router.get("/profile", response_model=UserResponse)
def get_user_profile_alt(user_id: int = Depends(get_user_id)):
    """Alternative endpoint for user profile (backward compatibility)"""
    return get_user_profile(user_id)

@router.get("/usage")
def get_usage_stats(user_id: int = Depends(get_user_id)):
    """Get user's current usage statistics"""
    return get_user_usage(user_id) 