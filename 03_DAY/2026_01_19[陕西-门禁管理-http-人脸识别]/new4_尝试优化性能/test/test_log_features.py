# 测试脚本：测试修改后的日志功能
import subprocess
import requests
import time
import os
import tempfile

# 测试服务器地址
base_url = 'http://localhost:8091'

# 测试1：启动服务器并检查日志输出
print("=== 测试1：启动服务器并检查日志输出 ===")

# 创建临时文件用于捕获控制台输出
console_output_file = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False)

# 启动服务器
server_process = subprocess.Popen(
    ['python', 'mockserver.py'],
    stdout=console_output_file,
    stderr=subprocess.STDOUT,
    text=True
)

# 等待服务器启动
time.sleep(3)

# 测试2：发送请求，产生日志
print("\n=== 测试2：发送请求，产生日志 ===")

# 设置密码
response = requests.post(f'{base_url}/setPassWord', data={
    'oldPass': '12345678',
    'newPass': '12345678'
})
print(f"Set password response: {response.json()}")

# 获取设备信息
response = requests.get(f'{base_url}/device/information', data={
    'pass': '12345678'
})
print(f"Get device info response: {response.json()}")

# 等待日志写入
time.sleep(1)

# 测试3：检查控制台日志输出
print("\n=== 测试3：检查控制台日志输出 ===")

# 关闭临时文件
temp_file_name = console_output_file.name
console_output_file.close()

# 读取控制台输出
with open(temp_file_name, 'r', encoding='utf-8') as f:
    console_output = f.read()

# 检查控制台输出中是否有INFO或以上级别的日志
info_level_logs = []
for line in console_output.split('\n'):
    if any(level in line for level in ['INFO', 'WARNING', 'ERROR', 'CRITICAL']):
        info_level_logs.append(line)

if info_level_logs:
    print(f"✓ 控制台日志输出正常，共记录 {len(info_level_logs)} 条INFO或以上级别的日志")
    print("  示例日志：")
    for log in info_level_logs[:3]:
        print(f"    {log}")
else:
    print("✗ 控制台日志输出异常，未找到INFO或以上级别的日志")

# 测试4：检查日志文件内容
print("\n=== 测试4：检查日志文件内容 ===")

log_file = 'logs/mockserver.log'
if os.path.exists(log_file):
    print(f"✓ 日志文件已生成: {log_file}")
    
    # 检查日志文件大小
    log_size = os.path.getsize(log_file)
    print(f"  日志文件大小: {log_size} 字节")
    
    # 检查日志文件中是否包含DEBUG级别的日志
    with open(log_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    if 'DEBUG' in file_content:
        print("✓ 日志文件记录了DEBUG级别的日志")
    else:
        print("✗ 日志文件未记录DEBUG级别的日志")
        
    # 检查日志文件中是否包含INFO级别的日志
    if 'INFO' in file_content:
        print("✓ 日志文件记录了INFO级别的日志")
    else:
        print("✗ 日志文件未记录INFO级别的日志")
else:
    print(f"✗ 日志文件不存在: {log_file}")

# 关闭服务器
print("\n关闭服务器...")
server_process.terminate()
try:
    server_process.wait(timeout=2)
except subprocess.TimeoutExpired:
    server_process.kill()
    
# 清理临时文件
os.unlink(temp_file_name)

print("\n=== 测试完成！ ===")
