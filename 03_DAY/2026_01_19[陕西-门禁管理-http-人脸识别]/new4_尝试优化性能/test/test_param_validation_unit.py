#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试：验证参数验证逻辑
直接测试device.py中的方法，不依赖HTTP服务器
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from business_logic.device import DeviceService
from datastore.data_store import data_store

def test_set_identify_callback():
    """测试识别回调设置的参数验证"""
    print("\n=== 测试识别回调设置 ===")
    device_service = DeviceService()
    
    # 设置设备密码
    device_service.data_store.set_password("123456")
    
    # 测试数据
    base_data = {"pass": "123456", "callbackUrl": "http://example.com/callback"}
    
    # 1. 测试base64Enable为字符串类型（预期失败）
    result = device_service.set_identify_callback({**base_data, "base64Enable": "0"})
    print(f"测试1 - base64Enable为字符串类型: {result}")
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    # 2. 测试base64Enable为int类型（预期成功）
    result = device_service.set_identify_callback({**base_data, "base64Enable": 0})
    print(f"测试2 - base64Enable为int类型: {result}")
    assert result["code"] == "LAN_SUS-0", f"预期LAN_SUS-0，实际{result['code']}"
    
    # 3. 测试base64Enable为int类型1（预期成功）
    result = device_service.set_identify_callback({**base_data, "base64Enable": 1})
    print(f"测试3 - base64Enable为int类型1: {result}")
    assert result["code"] == "LAN_SUS-0", f"预期LAN_SUS-0，实际{result['code']}"
    
    print("识别回调设置测试通过！")

def test_set_img_reg_callback():
    """测试注册照片回调设置的参数验证"""
    print("\n=== 测试注册照片回调设置 ===")
    device_service = DeviceService()
    
    # 设置设备密码
    device_service.data_store.set_password("123456")
    
    # 测试数据
    base_data = {"pass": "123456", "url": "http://example.com/callback"}
    
    # 1. 测试base64Enable为字符串类型（预期失败）
    result = device_service.set_img_reg_callback({**base_data, "base64Enable": "1"})
    print(f"测试1 - base64Enable为字符串类型: {result}")
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    # 2. 测试base64Enable为int类型（预期成功）
    result = device_service.set_img_reg_callback({**base_data, "base64Enable": 1})
    print(f"测试2 - base64Enable为int类型: {result}")
    assert result["code"] == "LAN_SUS-0", f"预期LAN_SUS-0，实际{result['code']}"
    
    print("注册照片回调设置测试通过！")

def test_open_door_control():
    """测试远程控制输出的参数验证"""
    print("\n=== 测试远程控制输出 ===")
    device_service = DeviceService()
    
    # 设置设备密码
    device_service.data_store.set_password("123456")
    
    # 测试数据
    base_data = {"pass": "123456"}
    
    # 1. 测试type为字符串类型（预期失败）
    result = device_service.open_door_control({**base_data, "type": "1"})
    print(f"测试1 - type为字符串类型: {result}")
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    # 2. 测试type为int类型但值为2（预期失败）
    result = device_service.open_door_control({**base_data, "type": 2})
    print(f"测试2 - type为int类型但值为2: {result}")
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    # 3. 测试type为int类型且值为1（预期成功）
    result = device_service.open_door_control({**base_data, "type": 1})
    print(f"测试3 - type为int类型且值为1: {result}")
    assert result["code"] == "LAN_SUS-0", f"预期LAN_SUS-0，实际{result['code']}"
    
    # 4. 测试不传递type参数（预期成功）
    result = device_service.open_door_control(base_data)
    print(f"测试4 - 不传递type参数: {result}")
    assert result["code"] == "LAN_SUS-0", f"预期LAN_SUS-0，实际{result['code']}"
    
    print("远程控制输出测试通过！")

if __name__ == "__main__":
    print("开始执行参数验证单元测试")
    
    try:
        test_set_identify_callback()
        test_set_img_reg_callback()
        test_open_door_control()
        print("\n所有测试通过！参数验证逻辑实现正确。")
    except AssertionError as e:
        print(f"\n测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)