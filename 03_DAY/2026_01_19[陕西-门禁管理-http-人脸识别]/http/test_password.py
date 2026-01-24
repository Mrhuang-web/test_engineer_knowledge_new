# 测试密码设置逻辑的脚本

import sys
import os
import requests

# 设备地址
BASE_URL = "http://127.0.0.1:8090"

print("=== 测试设备密码设置逻辑 ===")

# 测试1：设备初始无密码，其他接口应拒绝访问
print("\n1. 测试设备初始状态，访问设备信息接口")
try:
    response = requests.get(f"{BASE_URL}/device/information?pass=12345678")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：设备信息接口被拒绝访问")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试2：首次设置密码，oldPass和newPass相同
print("\n2. 测试首次设置密码，oldPass和newPass相同")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "test1234", "newPass": "test1234"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：密码设置成功")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试3：首次设置密码，oldPass和newPass不同（应失败）
print("\n3. 测试首次设置密码，oldPass和newPass不同")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "test1234", "newPass": "different"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：密码设置失败，提示旧密码和新密码必须一致")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试4：修改密码，oldPass正确
print("\n4. 测试修改密码，oldPass正确")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "test1234", "newPass": "new1234"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：密码修改成功")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试5：修改密码，oldPass错误
print("\n5. 测试修改密码，oldPass错误")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "wrong1234", "newPass": "new5678"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：密码修改失败，提示旧密码错误")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试6：使用新密码访问设备信息接口
print("\n6. 测试使用新密码访问设备信息接口")
try:
    response = requests.get(f"{BASE_URL}/device/information?pass=new1234")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   ✅ 预期：设备信息接口访问成功")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 所有测试完成 ===")
