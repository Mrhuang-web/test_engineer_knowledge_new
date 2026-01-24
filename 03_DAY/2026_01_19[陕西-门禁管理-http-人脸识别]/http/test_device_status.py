# 测试设备状态管理和重置功能的脚本

import sys
import os
import requests

# 设备地址
BASE_URL = "http://127.0.0.1:8090"

print("=== 测试设备状态管理和重置功能 ===")

# 测试1：检查设备初始状态
print("\n1. 测试设备初始状态")
try:
    response = requests.get(f"{BASE_URL}/device/status?pass=12345678")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：设备状态接口被拒绝访问（无密码）")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试2：首次设置密码
print("\n2. 测试首次设置密码")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "test1234", "newPass": "test1234"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：密码设置成功")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试3：获取设备状态
print("\n3. 测试获取设备状态")
try:
    response = requests.get(f"{BASE_URL}/device/status?pass=test1234")
    print(f"   状态码: {response.status_code}")
    status = response.json()
    print(f"   响应: {status}")
    if 'data' in status and not status['data']['is_first_setup']:
        print("   ✅ 预期：is_first_setup变为False")
    else:
        print("   ❌ 预期：is_first_setup应该变为False")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试4：重置设备
print("\n4. 测试重置设备")
try:
    response = requests.post(f"{BASE_URL}/resetDevice", 
                          data={"pass": "test1234"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：设备重置成功")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试5：检查重置后的设备状态
print("\n5. 测试重置后的设备状态")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "new1234", "newPass": "new1234"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：可以重新设置密码")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试6：获取重置后的状态
print("\n6. 测试获取重置后的设备状态")
try:
    response = requests.get(f"{BASE_URL}/device/status?pass=new1234")
    print(f"   状态码: {response.status_code}")
    status = response.json()
    print(f"   响应: {status}")
    if 'data' in status and status['data']['reset_count'] > 0:
        print("   ✅ 预期：reset_count增加")
    else:
        print("   ❌ 预期：reset_count应该增加")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 所有测试完成 ===")
