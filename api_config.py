import os

class APIConfig:
    DOUBAO_LLM_ENDPOINT = "ep-20260511114916-8vh5d"
    DOUBAO_API_KEY = os.environ.get('ARK_API_KEY')
    
    KIMI_API_KEY = os.environ.get('KIMI_API_KEY', "sk-mOsNqxU6WTBriYzQbdU8KapaTEwjpCBjmkoptc3ppjiAxHSt")
    
    DOUBAO_LLM_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    @staticmethod
    def get_doubao_headers():
        if not APIConfig.DOUBAO_API_KEY:
            raise ValueError("ARK_API_KEY 环境变量未设置")
        return {
            "Authorization": f"Bearer {APIConfig.DOUBAO_API_KEY}",
            "Content-Type": "application/json"
        }
    
    @staticmethod
    def get_kimi_headers():
        if not APIConfig.KIMI_API_KEY:
            raise ValueError("KIMI_API_KEY 环境变量未设置")
        return {
            "Authorization": f"Bearer {APIConfig.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }
    
    @staticmethod
    def is_doubao_available():
        return bool(APIConfig.DOUBAO_API_KEY)
    
    @staticmethod
    def is_kimi_available():
        return bool(APIConfig.KIMI_API_KEY)