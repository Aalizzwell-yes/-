import os
import requests

def test_video_models():
    api_key = os.environ.get('VIDEO_API_KEY')
    if not api_key:
        print("❌ API Key 未配置")
        return
    
    url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    test_models = [
        "doubao-seedance-2-0",
        "doubao-seedance-2-0-fast",
        "doubao-seedance-2-0-pro",
        "doubao-seedance-2-0-260215",
        "seedance-2-0",
        "doubao-seed-2-0-pro"
    ]
    
    test_prompt = "一只可爱的橘猫在草地上打哈欠"
    
    print("🧪 测试视频生成模型可用性...")
    print(f"🔑 API Key: {api_key[:20]}...\n")
    
    for model in test_models:
        print(f"\n{'='*60}")
        print(f"📋 测试模型: {model}")
        print(f"{'='*60}")
        
        payload = {
            "model": model,
            "content": [
                {
                    "type": "text",
                    "text": test_prompt
                }
            ],
            "duration": 3,
            "resolution": "480p",
            "return_last_frame": False
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            result = response.json()
            
            if response.status_code == 200:
                print(f"✅ 成功！任务ID: {result.get('id')}")
                return model, result
            elif 'ModelNotOpen' in str(result):
                print(f"⚠️  模型未开通")
            elif 'InvalidParameter' in str(result):
                print(f"❌ 参数错误")
            else:
                print(f"❌ 错误: {result}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {str(e)[:100]}")
    
    print("\n\n💡 所有测试的模型都不可用")
    print("请在火山方舟控制台确认正确的视频生成模型名称")
    return None, None

if __name__ == "__main__":
    test_video_models()