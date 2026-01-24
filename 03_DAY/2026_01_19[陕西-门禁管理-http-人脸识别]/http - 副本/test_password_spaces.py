# 测试密码空格校验的脚本

import sys
import os
import requests

# 设备地址
BASE_URL = "http://127.0.0.1:8090"

print("=== 测试密码空格校验逻辑 ===")

# 测试1：旧密码为空
print("\n1. 测试旧密码为空")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "", "newPass": "test1234"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["code"] == "LAN_EXP-2003":
        print("   ✅ 预期：返回旧密码不允许为空或空格错误")
    else:
        print("   ❌ 预期：返回旧密码不允许为空或空格错误，但实际返回不同的错误")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试2：旧密码只包含空格
print("\n2. 测试旧密码只包含空格")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "    ", "newPass": "test1234"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["code"] == "LAN_EXP-2003":
        print("   ✅ 预期：返回旧密码不允许为空或空格错误")
    else:
        print("   ❌ 预期：返回旧密码不允许为空或空格错误，但实际返回不同的错误")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试3：新密码为空
print("\n3. 测试新密码为空")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "test1234", "newPass": ""})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["code"] == "LAN_EXP-2004":
        print("   ✅ 预期：返回新密码不允许为空或空格错误")
    else:
        print("   ❌ 预期：返回新密码不允许为空或空格错误，但实际返回不同的错误")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试4：新密码只包含空格
print("\n4. 测试新密码只包含空格")
try:
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "test1234", "newPass": "    "})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["code"] == "LAN_EXP-2004":
        print("   ✅ 预期：返回新密码不允许为空或空格错误")
    else:
        print("   ❌ 预期：返回新密码不允许为空或空格错误，但实际返回不同的错误")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试5：正常设置密码
print("\n5. 测试正常设置密码")
try:
    # 先重置设备
    response = requests.post(f"{BASE_URL}/resetDevice", 
                          data={"oldPass": "12345678", "newPass": "12345678"})
    
    response = requests.post(f"{BASE_URL}/setPassWord", 
                          data={"oldPass": "newtest123", "newPass": "newtest123"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 预期：正常设置密码成功")
    else:
        print("   ❌ 预期：正常设置密码成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 所有测试完成 ===")
