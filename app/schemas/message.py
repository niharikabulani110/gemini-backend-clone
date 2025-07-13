from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    sender: str
    content: str
    created_at: datetime
