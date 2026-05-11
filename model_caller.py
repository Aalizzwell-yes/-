import os
import requests
from api_config import APIConfig

def call_model(prompt, model="auto"):
    available_models = []
    if APIConfig.is_doubao_available():
        available_models.append("doubao")
    if APIConfig.is_kimi_available():
        available_models.append("kimi")
    
    if not available_models:
        return "❌ 没有可用的模型，请先配置API Key"
    
    if model == "auto":
        model = available_models[0]
    
    if model == "doubao":
        return call_doubao(prompt)
    elif model == "kimi":
        return call_kimi(prompt)
    else:
        return f"❌ 未知模型: {model}，可用模型: {available_models}"

def call_doubao(prompt):
    if not APIConfig.is_doubao_available():
        return "❌ 豆包模型不可用，请配置 ARK_API_KEY"
    
    url = APIConfig.DOUBAO_LLM_URL
    headers = APIConfig.get_doubao_headers()
    
    payload = {
        "model": APIConfig.DOUBAO_LLM_ENDPOINT,
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
        return f"💬 豆包回复：\n{content}"
        
    except requests.exceptions.RequestException as e:
        return f"❌ 豆包调用失败: {str(e)[:100]}"

def call_kimi(prompt):
    if not APIConfig.is_kimi_available():
        return "❌ Kimi模型不可用，请配置 KIMI_API_KEY"
    
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = APIConfig.get_kimi_headers()
    
    payload = {
        "model": "moonshot-v1-8k",
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
        return f"💬 Kimi回复：\n{content}"
        
    except requests.exceptions.RequestException as e:
        return f"❌ Kimi调用失败: {str(e)[:100]}"

def list_available_models():
    models = []
    if APIConfig.is_doubao_available():
        models.append("✅ 豆包 (doubao-seed-2-0-pro)")
    if APIConfig.is_kimi_available():
        models.append("✅ Kimi (moonshot-v1-8k)")
    
    if not models:
        return "❌ 没有可用的模型"
    
    return "📋 可用模型列表：\n" + "\n".join(models)

if __name__ == "__main__":
    print(list_available_models())