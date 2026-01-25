# 测试主程序响应格式
import http.client
import json

# 启动服务器（这里需要先手动启动服务器）
# 测试不支持的URL
conn = http.client.HTTPConnection("localhost", 8090)

# 测试1：不支持的URL
print("=== 测试1：不支持的URL ===")
conn.request("GET", "/invalid_url")
response = conn.getresponse()
data = response.read().decode('utf-8')
print(f"Status: {response.status}")
print(f"Response: {data}")

# 转换为JSON并检查字段顺序
json_data = json.loads(data)
print(f"Response keys order: {list(json_data.keys())}")
print()

# 测试2：不支持的请求方法
print("=== 测试2：不支持的请求方法 ===")
conn.request("POST", "/device/information")
response = conn.getresponse()
data = response.read().decode('utf-8')
print(f"Status: {response.status}")
print(f"Response: {data}")

# 转换为JSON并检查字段顺序
json_data = json.loads(data)
print(f"Response keys order: {list(json_data.keys())}")
print()

# 测试3：参数验证失败
print("=== 测试3：参数验证失败 ===")
conn.request("POST", "/person/create")
response = conn.getresponse()
data = response.read().decode('utf-8')
print(f"Status: {response.status}")
print(f"Response: {data}")

# 转换为JSON并检查字段顺序
json_data = json.loads(data)
print(f"Response keys order: {list(json_data.keys())}")

conn.close()
print()
print("=== 测试完成 ===")