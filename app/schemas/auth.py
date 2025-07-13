from pydantic import BaseModel

class SignupRequest(BaseModel):
    mobile_number: str
    password: str

class SendOtpRequest(BaseModel):
    mobile_number: str

class VerifyOtpRequest(BaseModel):
    mobile_number: str
    otp: str

class ForgotPasswordRequest(BaseModel):
    mobile_number: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
