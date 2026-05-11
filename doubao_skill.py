import os
import requests

def execute_action(action_id, params):
    api_key = os.environ.get('ARK_API_KEY')
    if not api_key:
        return {"error": "ARK_API_KEY 环境变量未设置"}
    
    if action_id == "chat":
        return chat(params.get("prompt", ""), api_key)
    
    return {"error": f"未知动作: {action_id}"}

def chat(prompt, api_key):
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "ep-20260511114916-8vh5d",
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
        
        return {
            "success": True,
            "output": content,
            "model": "doubao-seed-2-0-pro",
            "prompt": prompt
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)[:200]
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python doubao_skill.py <action_id> <prompt>")
        sys.exit(1)
    
    action_id = sys.argv[1]
    prompt = " ".join(sys.argv[2:])
    
    result = execute_action(action_id, {"prompt": prompt})
    if result.get("success"):
        print(f"💬 豆包回复：\n{result['output']}")
    else:
        print(f"❌ 错误：{result.get('error', '未知错误')}")