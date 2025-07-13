from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chatroom import ChatroomCreate, ChatroomOut, ChatroomDetail
from app.services.chatroom_service import create_chatroom, get_user_chatrooms, get_chatroom_detail
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
    try:
        return create_chatroom(user_id, payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ChatroomOut])
def list_chatrooms(user_id: int = Depends(get_user_id)):
    return get_user_chatrooms(user_id)

@router.get("/{chatroom_id}", response_model=ChatroomDetail)
def get_chatroom(chatroom_id: int, user_id: int = Depends(get_user_id)):
    try:
        return get_chatroom_detail(user_id, chatroom_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
