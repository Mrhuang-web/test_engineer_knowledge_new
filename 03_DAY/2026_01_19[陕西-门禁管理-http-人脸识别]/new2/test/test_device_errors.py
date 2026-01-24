# 测试脚本：测试设备管理接口的错误处理
import requests
import time

# 测试服务器地址
base_url = 'http://localhost:8090'

# 测试1：设备未设置密码时调用接口
print("=== 测试1：设备未设置密码时调用接口 ===")

# 清除密码（通过重新启动服务器实现）
print("1. 请确保服务器处于未设置密码状态")
print("2. 或者重启服务器来清除密码")
print("\n正在测试...")

# 测试获取设备信息接口
response = requests.get(f'{base_url}/device/information', data={'pass': '12345678'})
print(f"获取设备信息响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1003', f"期望返回LAN_EXP-1003，实际返回{response.json()['code']}"

# 测试远程开门接口
response = requests.post(f'{base_url}/device/openDoorControl', data={'pass': '12345678', 'type': 1})
print(f"远程开门响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1003', f"期望返回LAN_EXP-1003，实际返回{response.json()['code']}"

# 测试2：设置密码
print("\n=== 测试2：设置密码 ===")
response = requests.post(f'{base_url}/setPassWord', data={
    'oldPass': '12345678',
    'newPass': '12345678'
})
print(f"设置密码响应：{response.json()}")
assert response.json()['code'] == 'LAN_SUS-0', f"期望返回LAN_SUS-0，实际返回{response.json()['code']}"

# 测试3：密码错误时调用接口
print("\n=== 测试3：密码错误时调用接口 ===")

# 测试获取设备信息接口
response = requests.get(f'{base_url}/device/information', data={'pass': 'wrong_password'})
print(f"获取设备信息响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1001', f"期望返回LAN_EXP-1001，实际返回{response.json()['code']}"

# 测试远程开门接口
response = requests.post(f'{base_url}/device/openDoorControl', data={'pass': 'wrong_password', 'type': 1})
print(f"远程开门响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1001', f"期望返回LAN_EXP-1001，实际返回{response.json()['code']}"

# 测试4：缺少pass参数时调用接口
print("\n=== 测试4：缺少pass参数时调用接口 ===")

# 测试获取设备信息接口
response = requests.get(f'{base_url}/device/information')
print(f"获取设备信息响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1002', f"期望返回LAN_EXP-1002，实际返回{response.json()['code']}"

# 测试远程开门接口
response = requests.post(f'{base_url}/device/openDoorControl', data={'type': 1})
print(f"远程开门响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1002', f"期望返回LAN_EXP-1002，实际返回{response.json()['code']}"

# 测试5：设置设备时间时的各种错误情况
print("\n=== 测试5：设置设备时间时的各种错误情况 ===")

# 测试5.1：缺少timestamp参数
response = requests.post(f'{base_url}/setTime', data={'pass': '12345678'})
print(f"缺少timestamp参数响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-1002', f"期望返回LAN_EXP-1002，实际返回{response.json()['code']}"

# 测试5.2：timestamp参数为空
response = requests.post(f'{base_url}/setTime', data={'pass': '12345678', 'timestamp': ''})
print(f"timestamp参数为空响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-2049', f"期望返回LAN_EXP-2049，实际返回{response.json()['code']}"

# 测试5.3：timestamp时间格式错误
response = requests.post(f'{base_url}/setTime', data={'pass': '12345678', 'timestamp': '2023-01-01'})
print(f"timestamp格式错误响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-2050', f"期望返回LAN_EXP-2050，实际返回{response.json()['code']}"

# 测试5.4：timestamp含有非法字符
response = requests.post(f'{base_url}/setTime', data={'pass': '12345678', 'timestamp': '2023-01-01 00:00:00abc'})
print(f"timestamp含非法字符响应：{response.json()}")
assert response.json()['code'] == 'LAN_EXP-2050', f"期望返回LAN_EXP-2050，实际返回{response.json()['code']}"

# 测试5.5：正确的时间格式
response = requests.post(f'{base_url}/setTime', data={'pass': '12345678', 'timestamp': '2023-01-01 00:00:00'})
print(f"正确时间格式响应：{response.json()}")
assert response.json()['code'] == 'LAN_SUS-0', f"期望返回LAN_SUS-0，实际返回{response.json()['code']}"

print("\n=== 所有测试通过！ ===")
print("设备管理接口的错误处理已完善，能正确返回相应的错误码。")
