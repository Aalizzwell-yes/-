import os

API_CONFIG = {
    "doubao": {
        "name": "豆包 (火山方舟)",
        "api_key": os.environ.get('DOUBAO_API_KEY', 'ark-e2c6507d-fac7-4e17-a3ca-a9180211e175-be364'),
        "model": "doubao-seedance-2-0-260128",
        "purpose": "视频生成",
        "status": "✅ 已配置"
    },
    "kimi": {
        "name": "Kimi (月之暗面)",
        "api_key": os.environ.get('KIMI_API_KEY', 'sk-mOsNqxU6WTBriYzQbdU8KapaTEwjpCBjmkoptc3ppjiAxHSt'),
        "model": "doubao-pro",
        "purpose": "文本对话、代码生成",
        "status": "✅ 已配置"
    }
}

def get_api_config(platform):
    return API_CONFIG.get(platform)

def list_all_platforms():
    print("\n📋 已配置的 API 平台：")
    for key, config in API_CONFIG.items():
        print(f"\n【{config['name']}】")
        print(f"  用途: {config['purpose']}")
        print(f"  状态: {config['status']}")
        print(f"  API Key: {config['api_key'][:20]}...")
        print(f"  模型: {config['model']}")
    
    print("\n" + "="*60)
    print("💡 使用方法：")
    print("  - 生成视频: 使用豆包 API")
    print("  - 对话/分析: 使用 Kimi API")
    print("="*60)

if __name__ == "__main__":
    list_all_platforms()