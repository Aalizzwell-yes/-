import os
import requests
import time

def generate_video(prompt, duration=7, resolution="1080p", model="doubao-seedance-1-0-pro-fast-251015"):
    api_key = os.environ.get('VOLC_ACCESS_KEY_ID')
    if not api_key:
        print("❌ API Key 未配置")
        return None
    
    url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    full_prompt = f"{prompt}"
    
    payload = {
        "model": model,
        "content": [
            {
                "type": "text",
                "text": full_prompt
            }
        ],
        "duration": duration,
        "resolution": resolution,
        "return_last_frame": False
    }
    
    print(f"🚀 开始生成视频...")
    print(f"✅ 使用模型: {model}")
    print(f"📝 提示词: {prompt}")
    print(f"⏱️ 时长: {duration}秒")
    print(f"📐 分辨率: {resolution}")
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"📤 请求体: {payload}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"\n📊 响应状态码: {response.status_code}")
        
        try:
            result = response.json()
            print(f"📝 响应内容: {result}")
        except:
            print(f"📝 响应内容(文本): {response.text}")
        
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ 视频生成任务已提交！")
        print(f"📋 任务ID: {result.get('id', '未知')}")
        
        task_id = result.get('id')
        if task_id:
            print(f"\n⏳ 正在等待视频生成...")
            return check_task_status(task_id, api_key)
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求失败: {str(e)}")
        if response:
            try:
                error_detail = response.json()
                print(f"📝 错误详情: {error_detail}")
            except:
                print(f"📝 错误详情: {response.text}")
        return None

def check_task_status(task_id, api_key):
    url = f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            status = result.get('status', 'unknown')
            
            print(f"🔄 检查状态 ({i+1}/{max_retries}): {status}")
            
            if status == 'succeeded':
                video_url = result.get('content', {}).get('video_url')
                print(f"\n🎉 视频生成完成！")
                print(f"🔗 视频链接: {video_url}")
                return video_url
                
            elif status == 'failed':
                error = result.get('error', {}).get('message', '未知错误')
                print(f"\n❌ 视频生成失败: {error}")
                return None
                
            elif status in ['queued', 'running']:
                time.sleep(10)
                continue
            else:
                print(f"\n⚠️ 未知状态: {status}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"\n❌ 查询失败: {str(e)}")
            return None
    
    print(f"\n⏰ 超时！视频生成时间过长")
    return None

if __name__ == "__main__":
    prompt = "一只可爱的橘猫在绿色草地上打哈欠，前面有一盆猫粮，阳光明媚，画面温馨治愈"
    result = generate_video(prompt, duration=7, resolution="1080p")
    
    if result:
        print(f"\n📥 视频链接已获取！")