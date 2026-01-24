import requests
import json

# 测试服务器地址
BASE_URL = "http://127.0.0.1:8093"

def test_server_running():
    """测试服务器是否正在运行"""
    print("测试服务器是否正在运行...")
    url = f"{BASE_URL}/device/information"
    
    try:
        # 使用GET请求，不传递任何参数
        response = requests.get(url, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        return True
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    test_server_running()