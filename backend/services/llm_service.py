import urllib.request
import urllib.error
import json
from config import settings

def generate_completion(system_prompt: str, user_prompt: str, fallback_text: str = "") -> str:
    """
    Sends a synchronous request to OpenAI's Chat Completion API using Python's 
    built-in urllib library (no extra package installations required).
    If no API key is specified, it returns the fallback_text.
    """
    if not settings.OPENAI_API_KEY:
        return fallback_text

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15.0) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            return res_json["choices"][0]["message"]["content"]
    except urllib.error.URLError as e:
        print(f"OpenAI API Request failed: {e}. Returning mock text.")
        return f"[OpenAI Connection Error: {e}]\n\n{fallback_text}"
    except Exception as e:
        print(f"Unexpected error: {e}. Returning mock text.")
        return f"[Error: {e}]\n\n{fallback_text}"
