#!/usr/bin/env python3
import sys
import os

os.environ['ARK_API_KEY'] = "ark-e2c6507d-fac7-4e17-a3ca-a9180211e175-be364"

from model_caller import call_kimi

def main():
    if len(sys.argv) < 2:
        print("使用方法：python kimi.py <你的问题>")
        return
    
    prompt = " ".join(sys.argv[1:])
    result = call_kimi(prompt)
    print(result)

if __name__ == "__main__":
    main()
