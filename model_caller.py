
import requests
from api_config import (
    DOUBAO_API_KEY,
    DOUBAO_BASE_URL,
    DOUBAO_MODEL,
    KIMI_API_KEY,
    KIMI_BASE_URL,
    KIMI_MODEL
)


def call_doubao(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -&gt; str:
    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": DOUBAO_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            f"{DOUBAO_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"调用豆包 API 失败: {str(e)}"


def call_kimi(prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -&gt; str:
    headers = {
        "Authorization": f"Bearer {KIMI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": KIMI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            f"{KIMI_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"调用 Kimi API 失败: {str(e)}"

