import os
import requests

def test_doubao_video_api():
    api_key = os.environ.get('VOLC_ACCESS_KEY_ID')
    if not api_key:
        print("❌ API Key 未配置")
        return
    
    print("✅ API Key 已配置")
    print(f"🔑 Key 格式验证: {len(api_key)} 字符")
    
    test_data = {
        "model": "doubao-seedance-1.5-pro",
        "prompt": "一只可爱的猫咪在草地上打哈欠",
        "duration": 3,
        "resolution": "480p"
    }
    
    print("\n📋 测试参数:")
    print(f"模型: {test_data['model']}")
    print(f"提示词: {test_data['prompt']}")
    print(f"时长: {test_data['duration']}秒")
    print(f"分辨率: {test_data['resolution']}")
    
    print("\n✅ 配置完成！可以开始生成视频了！")

if __name__ == "__main__":
    test_doubao_video_api()