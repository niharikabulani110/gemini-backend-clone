from app.models.chatroom import Chatroom
from app.models.message import Message
from app.schemas.chatroom import ChatroomCreate
from app.cache.redis_cache import get_cached_chatrooms, set_cached_chatrooms
from app.schemas.chatroom import ChatroomOut
from app.database import SessionLocal
from app.core.config import settings
from app.workers.tasks import fetch_gemini_reply

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

def create_chatroom(user_id: int, payload: ChatroomCreate):
    db = get_db()
    try:
        chatroom = Chatroom(name=payload.name, user_id=user_id)
        db.add(chatroom)
        db.commit()
        db.refresh(chatroom)
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
        serialized = [ChatroomOut.from_orm(room).dict() for room in rooms]
        set_cached_chatrooms(user_id, serialized)
        return serialized
    finally:
        db.close()

def add_user_message_and_queue(user_id: int, chatroom_id: int, content: str):
    db = get_db()
    try:
        chatroom = db.query(Chatroom).filter_by(id=chatroom_id, user_id=user_id).first()
        if not chatroom:
            raise Exception("Chatroom not found")

        msg = Message(chatroom_id=chatroom_id, sender="user", content=content)
        db.add(msg)
        db.commit()
        db.refresh(msg)

        # Trigger Gemini async reply
        fetch_gemini_reply.delay(content, chatroom_id)

        return {"status": "message queued"}
    finally:
        db.close()
