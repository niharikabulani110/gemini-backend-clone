import redis
import json
from app.core.config import settings
from datetime import datetime

r = redis.Redis.from_url(settings.REDIS_URL)

def get_cached_chatrooms(user_id: int):
    key = f"chatrooms:{user_id}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def set_cached_chatrooms(user_id: int, data):
    key = f"chatrooms:{user_id}"
    r.set(key, json.dumps(data, default=default_serializer), ex=300)  # 5 mins TTL
