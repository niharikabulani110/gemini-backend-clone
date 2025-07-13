from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import (
    SignupRequest, SendOtpRequest, VerifyOtpRequest, 
    ForgotPasswordRequest, ChangePasswordRequest, AuthTokenResponse
)
from app.services.auth_service import (
    signup_user, send_otp, verify_otp_token, 
    send_forgot_password_otp, change_password, reset_password_with_otp
)
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

@router.post("/signup")
def signup(payload: SignupRequest):
    try:
        return signup_user(payload.mobile_number, payload.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/send-otp")
def send_otp_api(payload: SendOtpRequest):
    try:
        return send_otp(payload.mobile_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify-otp", response_model=AuthTokenResponse)
def verify(payload: VerifyOtpRequest):
    token = verify_otp_token(payload.mobile_number, payload.otp)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest):
    try:
        return send_forgot_password_otp(payload.mobile_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/change-password")
def change_password_api(payload: ChangePasswordRequest, user_id: int = Depends(get_user_id)):
    try:
        return change_password(user_id, payload.old_password, payload.new_password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
def reset_password(payload: VerifyOtpRequest, new_password: str):
    try:
        return reset_password_with_otp(payload.mobile_number, payload.otp, new_password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
