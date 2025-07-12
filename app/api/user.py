from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserResponse
from app.models.user import User
from app.core.security import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import SessionLocal

auth_scheme = HTTPBearer()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> int:
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.get("/profile", response_model=UserResponse)
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