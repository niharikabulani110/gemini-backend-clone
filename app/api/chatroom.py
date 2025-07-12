from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chatroom import ChatroomCreate, ChatroomOut
from app.services.chatroom_service import create_chatroom, get_user_chatrooms
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

@router.post("/", response_model=ChatroomOut)
def create_new_chatroom(payload: ChatroomCreate, user_id: int = Depends(get_user_id)):
    return create_chatroom(user_id, payload)

@router.get("/", response_model=list[ChatroomOut])
def list_chatrooms(user_id: int = Depends(get_user_id)):
    return get_user_chatrooms(user_id)
