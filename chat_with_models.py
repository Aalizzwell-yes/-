#!/usr/bin/env python3
import sys
import os

# 先设置环境变量，再导入
os.environ['ARK_API_KEY'] = "ark-e2c6507d-fac7-4e17-a3ca-a9180211e175-be364"

from model_caller import call_doubao, call_kimi

def main():
    
    if len(sys.argv) < 2:
        print("使用方法：")
        print("  @豆包 <你的问题> - 使用豆包模型")
        print("  @kimi <你的问题> - 使用Kimi模型")
        print("\n示例：")
        print('  python chat_with_models.py @豆包 你好，请介绍一下自己')
        print('  python chat_with_models.py @kimi 你好，请写一段Python代码')
        return
    
    # 获取第一个参数
    first_arg = sys.argv[1].lower()
    # 获取问题内容
    prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "你好"
    
    if "@豆包" in sys.argv[1] or first_arg == "@豆包":
        result = call_doubao(prompt)
    elif "@kimi" in sys.argv[1] or first_arg == "@kimi":
        result = call_kimi(prompt)
    else:
        print("❌ 格式错误！请使用：")
        print("  @豆包 <你的问题> 或 @kimi <你的问题>")
        return
    
    print(result)

if __name__ == "__main__":
    main()
