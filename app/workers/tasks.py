from celery import Celery
import requests
from app.core.config import settings
from app.database import SessionLocal
from app.models.message import Message
from app.services.gemini_service import get_gemini_response

# Create Celery app
celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.workers.tasks']
)

# Configure Celery
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@celery.task
def fetch_gemini_reply(prompt: str, chatroom_id: int, user_id: int = None):
    """Fetch reply from Gemini API and save to database"""
    try:
        # Get Gemini response
        response_text = get_gemini_response(prompt)
        
        # Save response to database
        db = get_db()
        try:
            bot_message = Message(
                chatroom_id=chatroom_id,
                sender="bot",
                content=response_text
            )
            db.add(bot_message)
            db.commit()
            db.refresh(bot_message)
            
            return {
                "status": "success",
                "message_id": bot_message.id,
                "content": response_text
            }
        finally:
            db.close()
            
    except Exception as e:
        # Log error and save error message to database
        error_message = f"Error generating response: {str(e)}"
        db = get_db()
        try:
            bot_message = Message(
                chatroom_id=chatroom_id,
                sender="bot",
                content=error_message
            )
            db.add(bot_message)
            db.commit()
        finally:
            db.close()
        
        return {"status": "error", "error": str(e)}
