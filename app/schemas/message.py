from pydantic import BaseModel
from datetime import datetime

class MessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
