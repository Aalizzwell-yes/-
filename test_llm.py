import os
import requests

def test_llm(model_id="ep-20260511114916-8vh5d"):
    api_key = os.environ.get('ARK_API_KEY')
    if not api_key:
        print("❌ ARK_API_KEY 环境变量未配置")
        return None
    
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "user",
                "content": "你好！请用一句话介绍一下你自己。"
            }
        ],
        "max_tokens": 100
    }
    
    print(f"🚀 测试语言模型接入点...")
    print(f"✅ 使用接入点: {model_id}")
    print(f"🔑 API Key: {api_key[:20]}...\n")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"\n🎉 成功！模型响应:")
            print(f"💬 {content}")
            return content
        else:
            try:
                error_detail = response.json()
                print(f"\n❌ 错误详情: {error_detail}")
            except:
                print(f"\n❌ 错误详情: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求失败: {str(e)}")
        return None

if __name__ == "__main__":
    test_llm()