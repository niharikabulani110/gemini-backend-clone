import requests
from app.core.config import settings

def get_gemini_response(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # Add API key as query parameter
    url = f"{settings.GEMINI_API_URL}?key={settings.GEMINI_API_KEY}"

    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            try:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    parts = result["candidates"][0]["content"]["parts"]
                    return parts[0]["text"]
                else:
                    return "[Gemini response parsing failed - no candidates]"
            except Exception as e:
                return f"[Gemini response parsing failed: {str(e)}]"
        else:
            error_detail = ""
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_detail = f" - {error_data['error'].get('message', '')}"
            except:
                pass
            return f"[Gemini API error: {response.status_code}{error_detail}]"
    except Exception as e:
        return f"[Gemini API request failed: {str(e)}]"
