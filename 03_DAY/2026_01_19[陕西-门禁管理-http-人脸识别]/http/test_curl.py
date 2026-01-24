import requests

url = "http://127.0.0.1:8090/newDeleteRecords"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "pass": "12345678",
    "personId": "-1",
    "startTime": "0",
    "endTime": "9999-12-31 23:59:59",
    "model": "-1"
}

print(f"发送请求到: {url}")
print(f"请求头: {headers}")
print(f"请求数据: {data}")

response = requests.post(url, headers=headers, data=data)

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
