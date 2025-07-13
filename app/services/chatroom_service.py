from app.models.chatroom import Chatroom
from app.models.message import Message
from app.schemas.chatroom import ChatroomCreate, ChatroomOut, ChatroomDetail
from app.cache.redis_cache import get_cached_chatrooms, set_cached_chatrooms, invalidate_chatroom_cache
from app.database import SessionLocal
from app.core.config import settings
from app.workers.tasks import fetch_gemini_reply
from app.services.rate_limit_service import check_rate_limit, increment_message_count

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def create_chatroom(user_id: int, payload: ChatroomCreate):
    db = get_db()
    try:
        chatroom = Chatroom(name=payload.name, user_id=user_id)
        db.add(chatroom)
        db.commit()
        db.refresh(chatroom)
        
        # Invalidate cache for this user
        invalidate_chatroom_cache(user_id)
        
        return chatroom
    finally:
        db.close()

def get_user_chatrooms(user_id: int):
    cached = get_cached_chatrooms(user_id)
    if cached:
        return cached

    db = get_db()
    try:
        rooms = db.query(Chatroom).filter(Chatroom.user_id == user_id).all()
        serialized = [ChatroomOut.model_validate(room).model_dump() for room in rooms]
        set_cached_chatrooms(user_id, serialized)
        return serialized
    finally:
        db.close()

def get_chatroom_detail(user_id: int, chatroom_id: int):
    """Get detailed chatroom information including messages"""
    db = get_db()
    try:
        chatroom = db.query(Chatroom).filter(
            Chatroom.id == chatroom_id, 
            Chatroom.user_id == user_id
        ).first()
        
        if not chatroom:
            raise Exception("Chatroom not found")
        
        # Get messages for this chatroom
        messages = db.query(Message).filter(
            Message.chatroom_id == chatroom_id
        ).order_by(Message.created_at.asc()).all()
        
        return {
            "id": chatroom.id,
            "name": chatroom.name,
            "created_at": chatroom.created_at,
            "messages": messages
        }
    finally:
        db.close()

def add_user_message_and_queue(user_id: int, chatroom_id: int, content: str):
    # Check rate limit first
    if not check_rate_limit(user_id):
        raise Exception("Daily message limit exceeded. Upgrade to Pro for unlimited messages.")
    
    db = get_db()
    try:
        chatroom = db.query(Chatroom).filter_by(id=chatroom_id, user_id=user_id).first()
        if not chatroom:
            raise Exception("Chatroom not found")

        # Add user message
        msg = Message(chatroom_id=chatroom_id, sender="user", content=content)
        db.add(msg)
        db.commit()
        db.refresh(msg)

        # Increment usage count
        increment_message_count(user_id)

        # Trigger Gemini async reply
        fetch_gemini_reply.delay(content, chatroom_id, user_id)

        return {"status": "message queued", "message_id": msg.id}
    finally:
        db.close()
