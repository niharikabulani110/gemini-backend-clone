from pydantic import BaseModel, ConfigDict
from enum import Enum

class SubscriptionTier(str, Enum):
    basic = "basic"
    pro = "pro"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    mobile_number: str
    is_verified: bool
    subscription: SubscriptionTier
