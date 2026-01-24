import requests

url = "http://127.0.0.1:8090/device/information?oldPass=12345678&newPass=12345678"

print(f"发送请求到: {url}")

response = requests.get(url)

print(f"\n响应状态码: {response.status_code}")
print(f"响应头: {response.headers}")
print(f"响应内容: {response.text}")

# 尝试解析JSON
if "application/json" in response.headers.get("Content-Type", ""):
    try:
        json_response = response.json()
        print(f"\nJSON响应: {json_response}")
    except ValueError:
        print("\n响应内容不是有效的JSON格式")
