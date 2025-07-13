from fastapi import APIRouter, Depends, HTTPException
from app.schemas.message import MessageRequest, MessageResponse
from app.services.chatroom_service import add_user_message_and_queue
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

@router.post("/{chatroom_id}/message", response_model=dict)
def send_message(chatroom_id: int, payload: MessageRequest, user_id: int = Depends(get_user_id)):
    try:
        return add_user_message_and_queue(user_id, chatroom_id, payload.content)
    except Exception as e:
        if "Daily message limit exceeded" in str(e):
            raise HTTPException(status_code=429, detail=str(e))
        elif "Chatroom not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
