#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证API是否能正确处理float类型的整数参数
"""

import requests
import json

# 服务器地址
BASE_URL = "http://localhost:8092"

def test_open_door_control_float_type():
    """测试开门控制接口，使用float类型的type参数"""
    print("=== 测试开门控制接口 (float类型type参数) ===")
    url = f"{BASE_URL}/device/openDoorControl"
    
    # 初始设置密码
    setup_password()
    
    # 使用float类型的type参数 (1.0)
    payload = {
        "pass": "123456",
        "type": 1.0  # float类型的整数
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 开门控制接口成功处理float类型的type参数")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_set_identify_callback_float_base64_enable():
    """测试识别回调设置接口，使用float类型的base64Enable参数"""
    print("=== 测试识别回调设置接口 (float类型base64Enable参数) ===")
    url = f"{BASE_URL}/setIdentifyCallBack"
    
    # 使用float类型的base64Enable参数 (1.0)
    payload = {
        "pass": "123456",
        "callbackUrl": "http://example.com/callback",
        "base64Enable": 1.0  # float类型的整数
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 识别回调设置接口成功处理float类型的base64Enable参数")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_set_signal_input_float_params():
    """测试信号输入设置接口，使用float类型的整数参数"""
    print("=== 测试信号输入设置接口 (float类型整数参数) ===")
    url = f"{BASE_URL}/device/setSignalInput"
    
    # 使用float类型的inputNo、type参数
    payload = {
        "pass": "123456",
        "config": {
            "inputNo": 1.0,  # float类型的整数
            "isEnable": True,
            "type": 1.0,  # float类型的整数
            "name": "测试信号"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 信号输入设置接口成功处理float类型的整数参数")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_card_info_set_float_params():
    """测试卡片设置接口，使用float类型的整数参数"""
    print("=== 测试卡片设置接口 (float类型整数参数) ===")
    url = f"{BASE_URL}/cardInfoSet"
    
    # 使用float类型的整数参数
    payload = {
        "pass": "123456",
        "readDataEnable": True,
        "readSector": 1.0,  # float类型的整数
        "readBlock": 0.0,  # float类型的整数
        "readShift": 0.0,  # float类型的整数
        "readKeyA": "FFFFFFFFFFFF",
        "wgOutType": 1.0  # float类型的整数
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 卡片设置接口成功处理float类型的整数参数")
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
    print("测试API是否能正确处理float类型的整数参数\n")
    
    # 运行各个测试用例
    test_open_door_control_float_type()
    test_set_identify_callback_float_base64_enable()
    test_set_signal_input_float_params()
    test_card_info_set_float_params()
    
    print("所有测试完成！")

if __name__ == "__main__":
    main()