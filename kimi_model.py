import os
import requests

def call_kimi(prompt):
    api_key = os.environ.get('KIMI_API_KEY')
    if not api_key:
        api_key = "sk-mOsNqxU6WTBriYzQbdU8KapaTEwjpCBjmkoptc3ppjiAxHSt"

    url = "https://api.moonshot.cn/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "kimi-k2.6",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 2000
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        return content

    except Exception as e:
        return f"错误: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "你好，你是什么模型版本"

    result = call_kimi(prompt)
    print(result)
