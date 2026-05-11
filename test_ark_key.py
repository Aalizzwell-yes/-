import os
import requests

def test_ark_api_key():
    api_key = os.environ.get('ARK_API_KEY')
    if not api_key:
        print("❌ 未找到 ARK_API_KEY 环境变量")
        print("请先运行: export ARK_API_KEY='你的key'")
        return
    
    print(f"🔑 检测到 API Key: {api_key[:30]}...")
    
    url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    test_models = [
        "doubao-seedance-2-0",
        "doubao-seedance-1-0-pro",
        "doubao-seedance-1-0-pro-fast"
    ]
    
    print("\n🧪 测试视频生成模型...\n")
    
    for model in test_models:
        print(f"{'='*60}")
        print(f"📋 测试模型: {model}")
        print(f"{'='*60}")
        
        payload = {
            "model": model,
            "content": [{"type": "text", "text": "测试"}],
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
            else:
                error_code = result.get('error', {}).get('code', 'Unknown')
                print(f"❌ 错误代码: {error_code}")
                if 'ModelNotOpen' in error_code:
                    print(f"   → 模型未开通")
                elif 'InvalidEndpoint' in error_code or 'NotFound' in error_code:
                    print(f"   → 模型不存在或无访问权限")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {str(e)[:100]}")
    
    print("\n\n💡 建议：")
    print("1. 检查控制台中是否已开通视频生成模型")
    print("2. 确认模型名称是否正确")
    print("3. 可能需要创建推理接入点")

if __name__ == "__main__":
    test_ark_api_key()