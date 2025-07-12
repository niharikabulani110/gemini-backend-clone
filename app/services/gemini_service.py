import requests
from app.core.config import settings

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def get_gemini_response(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}"
    }

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(GEMINI_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        try:
            parts = response.json()["candidates"][0]["content"]["parts"]
            return parts[0]["text"]
        except Exception:
            return "[Gemini response parsing failed]"
    else:
        return f"[Gemini API error: {response.status_code}]"
