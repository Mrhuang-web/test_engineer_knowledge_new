import requests
import json

# 测试设置密码
def test_set_password():
    print("=== 测试设置密码 ===")
    url = "http://localhost:8091/setPassWord"
    headers = {"Content-Type": "application/json"}
    data = {
        "oldPass": "123456",
        "newPass": "123456"
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print()

# 测试获取设备信息
def test_get_device_info():
    print("=== 测试获取设备信息 ===")
    url = "http://localhost:8091/device/information"
    headers = {"Content-Type": "application/json"}
    data = {
        "pass": "123456"
    }
    
    response = requests.get(url, headers=headers, json=data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print()

# 测试设置时间
def test_set_time():
    print("=== 测试设置时间 ===")
    url = "http://localhost:8091/setTime"
    headers = {"Content-Type": "application/json"}
    data = {
        "pass": "123456",
        "timestamp": "1706077213605"
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print()

# 测试切换语言
def test_set_language():
    print("=== 测试切换语言 ===")
    url = "http://localhost:8091/device/setLanguage"
    headers = {"Content-Type": "application/json"}
    data = {
        "pass": "123456",
        "languageType": "en"
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print()

if __name__ == "__main__":
    test_set_password()
    test_get_device_info()
    test_set_time()
    test_set_language()