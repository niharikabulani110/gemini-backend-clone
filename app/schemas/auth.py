from pydantic import BaseModel

class SignupRequest(BaseModel):
    mobile_number: str

class SendOtpRequest(BaseModel):
    mobile_number: str

class VerifyOtpRequest(BaseModel):
    mobile_number: str
    otp: str

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
