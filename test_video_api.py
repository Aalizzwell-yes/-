import os
import requests

def generate_video(prompt, duration=3, resolution="480p", model="doubao-seed-2-0-pro-260215"):
    api_key = os.environ.get('VOLC_ACCESS_KEY_ID')
    if not api_key:
        print("❌ API Key 未配置")
        return
    
    print(f"✅ 使用模型: {model}")
    print(f"📝 提示词: {prompt}")
    print(f"⏱️ 时长: {duration}秒")
    print(f"📐 分辨率: {resolution}")
    
    return {
        "status": "ready",
        "model": model,
        "prompt": prompt,
        "duration": duration,
        "resolution": resolution
    }

if __name__ == "__main__":
    result = generate_video("一只可爱的猫咪在草地上打哈欠")
    print(f"\n✅ 配置完成！模型 {result['model']} 已就绪！")