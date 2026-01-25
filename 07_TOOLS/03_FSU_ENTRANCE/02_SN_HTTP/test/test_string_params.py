#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证API是否能正确处理字符串类型的数字参数
"""

import requests
import json

# 服务器地址
BASE_URL = "http://localhost:8092"

def test_open_door_control_string_type():
    """测试开门控制接口，使用字符串类型的type参数"""
    print("=== 测试开门控制接口 (字符串类型type参数) ===")
    url = f"{BASE_URL}/device/openDoorControl"
    
    # 使用字符串类型的type参数 ('1')
    payload = {
        "pass": "123456",
        "type": "1"  # 字符串类型的数字
    }
    
    try:
        # 发送表单数据，模拟APIFox可能的行为
        response = requests.post(url, data=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"Content-Type: application/x-www-form-urlencoded")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 开门控制接口成功处理字符串类型的type参数")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_open_door_control_json_string_type():
    """测试开门控制接口，使用JSON格式的字符串类型type参数"""
    print("=== 测试开门控制接口 (JSON格式字符串类型type参数) ===")
    url = f"{BASE_URL}/device/openDoorControl"
    
    # 使用JSON格式的字符串类型type参数
    payload = {
        "pass": "123456",
        "type": "1"  # 字符串类型的数字
    }
    
    try:
        # 发送JSON数据
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"Content-Type: application/json")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 开门控制接口成功处理JSON格式字符串类型的type参数")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_set_identify_callback_string_base64_enable():
    """测试识别回调设置接口，使用字符串类型的base64Enable参数"""
    print("=== 测试识别回调设置接口 (字符串类型base64Enable参数) ===")
    url = f"{BASE_URL}/setIdentifyCallBack"
    
    # 使用字符串类型的base64Enable参数 ('1')
    payload = {
        "pass": "123456",
        "callbackUrl": "http://example.com/callback",
        "base64Enable": "1"  # 字符串类型的数字
    }
    
    try:
        # 发送表单数据
        response = requests.post(url, data=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"Content-Type: application/x-www-form-urlencoded")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 识别回调设置接口成功处理字符串类型的base64Enable参数")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
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
    print("测试API是否能正确处理字符串类型的数字参数\n")
    
    # 初始设置密码
    setup_password()
    
    # 运行各个测试用例
    test_open_door_control_string_type()
    test_open_door_control_json_string_type()
    test_set_identify_callback_string_base64_enable()
    
    print("所有测试完成！")

if __name__ == "__main__":
    main()