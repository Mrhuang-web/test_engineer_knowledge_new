import requests

# 测试设置密码接口
print("=== 测试设置密码接口 ===")
url = "http://127.0.0.1:8092/setPassWord"
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
