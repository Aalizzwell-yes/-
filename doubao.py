
#!/usr/bin/env python3
import sys
from model_caller import call_doubao, call_kimi


def main():
    if len(sys.argv) &gt; 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "你好，请简单介绍一下自己"
    
    print("\n=== 测试豆包 API ===\n")
    print(f"输入: {prompt}\n")
    doubao_response = call_doubao(prompt)
    print(f"豆包回复: {doubao_response}\n")
    
    print("\n=== 测试 Kimi API ===\n")
    print(f"输入: {prompt}\n")
    kimi_response = call_kimi(prompt)
    print(f"Kimi回复: {kimi_response}\n")


if __name__ == "__main__":
    main()

