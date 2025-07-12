from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import SignupRequest, SendOtpRequest, VerifyOtpRequest, AuthTokenResponse
from app.services.auth_service import signup_user, send_otp, verify_otp_token

router = APIRouter()

@router.post("/signup")
def signup(payload: SignupRequest):
    return signup_user(payload.mobile_number)

@router.post("/send-otp")
def send_otp_api(payload: SendOtpRequest):
    return send_otp(payload.mobile_number)

@router.post("/verify-otp", response_model=AuthTokenResponse)
def verify(payload: VerifyOtpRequest):
    token = verify_otp_token(payload.mobile_number, payload.otp)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    return {"access_token": token}
