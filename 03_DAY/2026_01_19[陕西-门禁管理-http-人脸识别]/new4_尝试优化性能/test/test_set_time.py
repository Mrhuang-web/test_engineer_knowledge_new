# 测试脚本：测试设置设备时间接口的时间戳处理
import requests
import time

# 测试服务器地址
base_url = 'http://localhost:8090'

# 确保服务器已启动
print("=== 测试设置设备时间接口 ===")
print("请确保服务器已启动")

# 测试1：设置密码（如果还未设置）
print("\n=== 测试1：设置密码 ===")
response = requests.post(f'{base_url}/setPassWord', data={
    'oldPass': '12345678',
    'newPass': '12345678'
})
print(f"设置密码响应：{response.json()}")

# 测试2：使用正确的时间戳设置时间
print("\n=== 测试2：使用正确的时间戳设置时间 ===")
# 获取当前时间戳（秒）
current_timestamp = int(time.time())
print(f"当前时间戳：{current_timestamp}")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': str(current_timestamp)
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_SUS-0', f"期望返回LAN_SUS-0，实际返回{response.json()['code']}"

# 测试3：使用时间戳格式错误（非数字）
print("\n=== 测试3：使用时间戳格式错误（非数字） ===")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': 'invalid_timestamp'
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-2050', f"期望返回LAN_EXP-2050，实际返回{response.json()['code']}"

# 测试4：使用时间戳范围错误（小于0）
print("\n=== 测试4：使用时间戳范围错误（小于0） ===")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': '-1'
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-2050', f"期望返回LAN_EXP-2050，实际返回{response.json()['code']}"

# 测试5：使用时间戳范围错误（大于2100年）
print("\n=== 测试5：使用时间戳范围错误（大于2100年） ===")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': '5000000000'  # 大约2080年
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-2050', f"期望返回LAN_EXP-2050，实际返回{response.json()['code']}"

# 测试6：使用空时间戳
print("\n=== 测试6：使用空时间戳 ===")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': ''
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-2049', f"期望返回LAN_EXP-2049，实际返回{response.json()['code']}"

# 测试7：缺少时间戳参数
print("\n=== 测试7：缺少时间戳参数 ===")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678'
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1002', f"期望返回LAN_EXP-1002，实际返回{response.json()['code']}"

# 测试8：使用密码错误
print("\n=== 测试8：使用密码错误 ===")
response = requests.post(f'{base_url}/setTime', data={
    'pass': 'wrong_password',
    'timestamp': str(current_timestamp)
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1001', f"期望返回LAN_EXP-1001，实际返回{response.json()['code']}"

print("\n=== 所有测试通过！ ===")
print("设置设备时间接口的时间戳处理已完善，能正确处理各种情况。")
