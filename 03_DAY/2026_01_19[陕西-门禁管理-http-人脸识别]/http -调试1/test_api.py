import requests

# 测试设置密码接口
print("=== 测试设置密码接口 ===")
url = "http://127.0.0.1:8093/setPassWord"
data = {
    "oldPass": "12345678",
    "newPass": "12345678"
}

try:
    response = requests.post(url, data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")

# 测试远程开门接口
print("\n=== 测试远程开门接口 ===")
open_url = "http://127.0.0.1:8093/device/openDoorControl"
open_data = {
    "type": 1,
    "pass": "12345678"
}

try:
    response = requests.post(open_url, data=open_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")

# 测试设备信息查询
print("\n=== 测试设备信息查询接口 ===")
info_url = "http://127.0.0.1:8093/device/information?pass=12345678"

try:
    response = requests.get(info_url)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")
