from pydantic import BaseModel
from enum import Enum

class SubscriptionTier(str, Enum):
    basic = "basic"
    pro = "pro"

class UserResponse(BaseModel):
    id: int
    mobile_number: str
    is_verified: bool
    subscription: SubscriptionTier

    class Config:
        from_attributes = True
