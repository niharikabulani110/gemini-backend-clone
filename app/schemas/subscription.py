from pydantic import BaseModel

class SubscriptionStatusResponse(BaseModel):
    status: str  # "basic" or "pro"
