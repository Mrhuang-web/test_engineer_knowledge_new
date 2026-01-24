# 测试回调机制的脚本

import sys
import os
import requests

# 设备地址
BASE_URL = "http://127.0.0.1:8090"

print("=== 测试回调机制功能 ===")

# 测试1：设置识别回调地址
print("\n1. 测试设置识别回调地址")
try:
    callback_url = "http://192.168.16.250:8888/lan/identifyCallback"
    response = requests.post(f"{BASE_URL}/setIdentifyCallBack", 
                          data={"oldPass": "12345678", "newPass": "12345678", "callbackUrl": callback_url, "base64Enable": "2"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    if response.json().get('code') == 'LAN_SUS-0' and response.json().get('msg') == '设置成功':
        print("   ✅ 预期：设置识别回调地址成功")
    else:
        print("   ❌ 预期：设置识别回调地址成功，但实际失败")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试2：设置无效的识别回调地址
print("\n2. 测试设置无效的识别回调地址")
try:
    invalid_url = "invalid-url"
    response = requests.post(f"{BASE_URL}/setIdentifyCallBack", 
                          data={"oldPass": "12345678", "newPass": "12345678", "callbackUrl": invalid_url, "base64Enable": "1"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    if response.json().get('code') == 'LAN_EXP-2099':
        print("   ✅ 预期：设置无效识别回调地址失败，返回正确的错误码")
    else:
        print("   ❌ 预期：设置无效识别回调地址失败，但实际返回不同的错误码")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试3：清空识别回调地址
print("\n3. 测试清空识别回调地址")
try:
    response = requests.post(f"{BASE_URL}/setIdentifyCallBack", 
                          data={"oldPass": "12345678", "newPass": "12345678", "callbackUrl": "", "base64Enable": "1"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    if response.json().get('code') == 'LAN_SUS-0' and response.json().get('msg') == '设置成功':
        print("   ✅ 预期：清空识别回调地址成功")
    else:
        print("   ❌ 预期：清空识别回调地址成功，但实际失败")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试4：设置注册照片回调地址
print("\n4. 测试设置注册照片回调地址")
try:
    callback_url = "http://192.168.16.250:8888/lan/imgRegCallback"
    response = requests.post(f"{BASE_URL}/setImgRegCallBack", 
                          data={"oldPass": "12345678", "newPass": "12345678", "url": callback_url, "base64Enable": "1"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    if response.json().get('code') == 'LAN_SUS-0' and response.json().get('msg') == '设置成功':
        print("   ✅ 预期：设置注册照片回调地址成功")
    else:
        print("   ❌ 预期：设置注册照片回调地址成功，但实际失败")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试5：设置事件回调地址
print("\n5. 测试设置事件回调地址")
try:
    callback_url = "http://192.168.16.250:8888/lan/eventCallback"
    response = requests.post(f"{BASE_URL}/device/eventCallBack", 
                          data={"oldPass": "12345678", "newPass": "12345678", "url": callback_url})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    if response.json().get('code') == 'LAN_SUS-0' and response.json().get('msg') == '设置成功':
        print("   ✅ 预期：设置事件回调地址成功")
    else:
        print("   ❌ 预期：设置事件回调地址成功，但实际失败")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 所有测试完成 ===")
