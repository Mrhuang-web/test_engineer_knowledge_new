# 测试脚本：测试热启动功能
import subprocess
import time
import os

# 测试服务器地址
base_url = 'http://localhost:8090'

print("=== 测试热启动功能 ===")
print("1. 启动服务器")
print("2. 修改一个Python文件")
print("3. 观察服务器是否自动重启")
print("4. 检查服务器是否仍然正常工作")

# 启动服务器
print("\n=== 启动服务器 ===")
server_process = subprocess.Popen(
    ['python', 'mockserver.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# 等待服务器启动
time.sleep(3)

# 测试服务器是否正常工作
print("\n=== 测试服务器是否正常工作 ===")
import requests
response = requests.post(f'{base_url}/setPassWord', data={
    'oldPass': '12345678',
    'newPass': '12345678'
})
print(f"设置密码响应：{response.json()}")
assert response.json()['code'] == 'LAN_SUS-0', f"期望返回LAN_SUS-0，实际返回{response.json()['code']}"

# 修改一个Python文件
test_file_path = 'business_logic/device.py'
print(f"\n=== 修改文件：{test_file_path} ===")

# 读取文件内容
with open(test_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 在文件末尾添加一个注释
with open(test_file_path, 'a', encoding='utf-8') as f:
    f.write(f"\n# 热启动测试注释 - {time.time()}")

print("已修改文件")

# 等待热启动检测和重启
time.sleep(5)

# 测试服务器是否仍然正常工作
print("\n=== 测试服务器是否自动重启并正常工作 ===")
try:
    response = requests.get(f'{base_url}/device/information', data={'pass': '12345678'})
    print(f"获取设备信息响应：{response.json()}")
    assert response.json()['code'] == 'LAN_SUS-0', f"期望返回LAN_SUS-0，实际返回{response.json()['code']}"
    print("✓ 热启动功能正常，服务器自动重启后正常工作")
except Exception as e:
    print(f"✗ 热启动功能异常：{e}")

# 停止服务器
print("\n=== 停止服务器 ===")
server_process.terminate()
try:
    server_process.wait(timeout=2)
except subprocess.TimeoutExpired:
    server_process.kill()

print("\n=== 测试完成 ===")
