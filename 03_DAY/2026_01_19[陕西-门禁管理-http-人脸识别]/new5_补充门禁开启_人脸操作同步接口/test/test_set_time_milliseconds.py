# 测试脚本：测试设置设备时间接口的毫秒级时间戳处理
import requests
import time

# 测试服务器地址
base_url = 'http://localhost:8090'

# 确保服务器已启动
print("=== 测试设置设备时间接口（毫秒级时间戳） ===")
print("请确保服务器已启动")

# 测试1：设置密码（如果还未设置）
print("\n=== 测试1：设置密码 ===")
response = requests.post(f'{base_url}/setPassWord', data={
    'oldPass': '12345678',
    'newPass': '12345678'
})
print(f"设置密码响应：{response.json()}")

# 测试2：使用秒级时间戳设置时间
print("\n=== 测试2：使用秒级时间戳设置时间 ===")
# 获取当前秒级时间戳
current_second = int(time.time())
print(f"当前秒级时间戳：{current_second}")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': str(current_second)
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_SUS-0', f"期望返回LAN_SUS-0，实际返回{response.json()['code']}"

# 测试3：使用毫秒级时间戳设置时间
print("\n=== 测试3：使用毫秒级时间戳设置时间 ===")
# 获取当前毫秒级时间戳
current_millisecond = int(time.time() * 1000)
print(f"当前毫秒级时间戳：{current_millisecond}")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': str(current_millisecond)
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_SUS-0', f"期望返回LAN_SUS-0，实际返回{response.json()['code']}"

# 测试4：使用时间戳格式错误（非数字）
print("\n=== 测试4：使用时间戳格式错误（非数字） ===")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': 'invalid_timestamp'
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-2050', f"期望返回LAN_EXP-2050，实际返回{response.json()['code']}"

# 测试5：使用正确的毫秒级时间戳（手动输入）
print("\n=== 测试5：使用正确的毫秒级时间戳（手动输入） ===")
# 使用一个已知的正确毫秒级时间戳
manual_millisecond = "1640995200000"  # 2022-01-01 00:00:00
print(f"手动输入的毫秒级时间戳：{manual_millisecond}")
response = requests.post(f'{base_url}/setTime', data={
    'pass': '12345678',
    'timestamp': manual_millisecond
})
print(f"设置时间响应：{response.json()}")
assert response.json()['code'] == 'LAN_SUS-0', f"期望返回LAN_SUS-0，实际返回{response.json()['code']}"

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

print("\n=== 所有测试通过！ ===")
print("设置设备时间接口已支持毫秒级时间戳处理。")
print("\n使用说明：")
print("- 支持秒级时间戳（10位或更少）")
print("- 支持毫秒级时间戳（13位）")
print("- 会自动转换为秒级进行处理")
print("- 返回正确的错误信息")
