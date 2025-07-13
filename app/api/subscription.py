from fastapi import APIRouter, Depends, HTTPException
from app.services.stripe_service import create_stripe_checkout, get_subscription_status
from app.schemas.subscription import SubscriptionStatusResponse
from app.core.security import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

auth_scheme = HTTPBearer()
router = APIRouter()

def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> int:
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.post("/pro")
def start_subscription(user_id: int = Depends(get_user_id)):
    try:
        return create_stripe_checkout(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status", response_model=SubscriptionStatusResponse)
def check_status(user_id: int = Depends(get_user_id)):
    try:
        status = get_subscription_status(user_id)
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
