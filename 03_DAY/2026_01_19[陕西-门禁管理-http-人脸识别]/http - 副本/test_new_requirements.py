# 测试新需求的脚本

import sys
import os
import requests

# 设备地址
BASE_URL = "http://127.0.0.1:8090"

print("=== 测试新需求功能 ===")

# 测试1：设备初始无密码，使用正确的oldPass和newPass（12345678）调用设备信息接口
print("\n1. 测试设备初始无密码，使用正确的oldPass和newPass（12345678）调用设备信息接口")
try:
    response = requests.get(f"{BASE_URL}/device/information?oldPass=12345678&newPass=12345678")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 预期：设备信息接口访问成功")
    else:
        print("   ❌ 预期：设备信息接口访问成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试2：设备初始无密码，使用错误的oldPass和newPass调用设备信息接口
print("\n2. 测试设备初始无密码，使用错误的oldPass和newPass调用设备信息接口")
try:
    response = requests.get(f"{BASE_URL}/device/information?oldPass=wrong&newPass=wrong")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-1001":
        print("   ✅ 预期：设备信息接口访问失败，提示密码错误")
    else:
        print("   ❌ 预期：设备信息接口访问失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试3：设备初始无密码，使用不相同的oldPass和newPass调用设备信息接口
print("\n3. 测试设备初始无密码，使用不相同的oldPass和newPass调用设备信息接口")
try:
    response = requests.get(f"{BASE_URL}/device/information?oldPass=12345678&newPass=different")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-1001":
        print("   ✅ 预期：设备信息接口访问失败，提示密码错误")
    else:
        print("   ❌ 预期：设备信息接口访问失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试4：设备初始无密码，未传入oldPass和newPass调用设备信息接口
print("\n4. 测试设备初始无密码，未传入oldPass和newPass调用设备信息接口")
try:
    response = requests.get(f"{BASE_URL}/device/information")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-1002":
        print("   ✅ 预期：设备信息接口访问失败，提示密码参数异常")
    else:
        print("   ❌ 预期：设备信息接口访问失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试5：测试set_time接口，传入空的timestamp
print("\n5. 测试set_time接口，传入空的timestamp")
try:
    response = requests.post(f"{BASE_URL}/setTime", data={"oldPass": "12345678", "newPass": "12345678", "timestamp": ""})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-2049":
        print("   ✅ 预期：set_time接口访问失败，提示timestamp参数异常")
    else:
        print("   ❌ 预期：set_time接口访问失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试6：测试set_time接口，传入格式错误的timestamp
print("\n6. 测试set_time接口，传入格式错误的timestamp")
try:
    response = requests.post(f"{BASE_URL}/setTime", data={"oldPass": "12345678", "newPass": "12345678", "timestamp": "invalid"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-2050":
        print("   ✅ 预期：set_time接口访问失败，提示timestamp时间格式错误")
    else:
        print("   ❌ 预期：set_time接口访问失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试7：测试set_time接口，传入正确的timestamp
print("\n7. 测试set_time接口，传入正确的timestamp")
try:
    response = requests.post(f"{BASE_URL}/setTime", data={"oldPass": "12345678", "newPass": "12345678", "timestamp": "1609459200000"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 预期：set_time接口访问成功")
    else:
        print("   ❌ 预期：set_time接口访问成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试8：设备有密码后，使用pass参数调用接口
print("\n8. 测试设置密码后，使用pass参数调用接口")
# 先设置密码
try:
    # 重置设备，确保初始状态
    response = requests.post(f"{BASE_URL}/resetDevice", data={"oldPass": "12345678", "newPass": "12345678"})
    
    # 设置新密码
    response = requests.post(f"{BASE_URL}/setPassWord", data={"oldPass": "test1234", "newPass": "test1234"})
    print(f"   设置密码响应: {response.json()}")
    
    # 使用pass参数调用设备信息接口
    response = requests.get(f"{BASE_URL}/device/information?pass=test1234")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 预期：设备信息接口访问成功")
    else:
        print("   ❌ 预期：设备信息接口访问成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 所有测试完成 ===")
