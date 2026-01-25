#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证API是否严格要求int类型参数
"""

import requests
import json

# 服务器地址
BASE_URL = "http://localhost:8093"

def test_open_door_control_strict_int():
    """测试开门控制接口的严格int类型检查"""
    print("=== 测试开门控制接口的严格int类型检查 ===")
    url = f"{BASE_URL}/device/openDoorControl"
    
    # 初始设置密码
    setup_password()
    
    # 测试用例1：使用正确的int类型参数
    print("\n1. 测试使用正确的int类型参数 type=1")
    payload = {
        "pass": "123456",
        "type": 1  # 正确的int类型
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 正确的int类型参数被接受")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 测试用例2：使用float类型参数
    print("\n2. 测试使用float类型参数 type=1.0")
    payload = {
        "pass": "123456",
        "type": 1.0  # float类型，应该被拒绝
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if not result["success"]:
            print("✅ 测试通过: float类型参数被正确拒绝")
        else:
            print("❌ 测试失败: float类型参数被错误接受")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 测试用例3：使用字符串类型参数
    print("\n3. 测试使用字符串类型参数 type='1'")
    payload = {
        "pass": "123456",
        "type": "1"  # 字符串类型，应该被拒绝
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if not result["success"]:
            print("✅ 测试通过: 字符串类型参数被正确拒绝")
        else:
            print("❌ 测试失败: 字符串类型参数被错误接受")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_set_identify_callback_strict_int():
    """测试识别回调设置接口的严格int类型检查"""
    print("=== 测试识别回调设置接口的严格int类型检查 ===")
    url = f"{BASE_URL}/setIdentifyCallBack"
    
    # 测试用例1：使用正确的int类型参数
    print("\n1. 测试使用正确的int类型参数 base64Enable=1")
    payload = {
        "pass": "123456",
        "callbackUrl": "http://example.com/callback",
        "base64Enable": 1  # 正确的int类型
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 正确的int类型参数被接受")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 测试用例2：使用float类型参数
    print("\n2. 测试使用float类型参数 base64Enable=1.0")
    payload = {
        "pass": "123456",
        "callbackUrl": "http://example.com/callback",
        "base64Enable": 1.0  # float类型，应该被拒绝
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if not result["success"]:
            print("✅ 测试通过: float类型参数被正确拒绝")
        else:
            print("❌ 测试失败: float类型参数被错误接受")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 测试用例3：使用字符串类型参数
    print("\n3. 测试使用字符串类型参数 base64Enable='1'")
    payload = {
        "pass": "123456",
        "callbackUrl": "http://example.com/callback",
        "base64Enable": "1"  # 字符串类型，应该被拒绝
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if not result["success"]:
            print("✅ 测试通过: 字符串类型参数被正确拒绝")
        else:
            print("❌ 测试失败: 字符串类型参数被错误接受")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def setup_password():
    """初始设置设备密码"""
    url = f"{BASE_URL}/setPassWord"
    payload = {
        "oldPass": "123456",
        "newPass": "123456"
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        # 密码设置可能成功或失败（如果已经设置过），不影响测试
    except Exception as e:
        pass

def main():
    """运行所有测试"""
    print("测试API是否严格要求int类型参数\n")
    
    # 运行各个测试用例
    test_open_door_control_strict_int()
    test_set_identify_callback_strict_int()
    
    print("所有测试完成！")

if __name__ == "__main__":
    main()