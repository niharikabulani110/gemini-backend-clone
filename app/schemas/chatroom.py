from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.schemas.message import MessageResponse

class ChatroomCreate(BaseModel):
    name: str

class ChatroomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    created_at: datetime

class ChatroomDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    created_at: datetime
    messages: List[MessageResponse]
