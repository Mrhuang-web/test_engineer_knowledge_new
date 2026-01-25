#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本：验证人员注册的核心逻辑
"""

import requests
import json

# 服务器地址
BASE_URL = "http://localhost:8090"

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
        print(f"密码设置结果: {result}")
    except Exception as e:
        print(f"密码设置失败: {str(e)}")

def test_person_registration_no_id():
    """测试人员注册：不传id参数，系统生成32位id"""
    print("\n=== 测试1: 不传id参数，系统生成32位id ===")
    url = f"{BASE_URL}/person/create"
    
    payload = {
        "pass": "123456",
        "person": {
            "name": "测试人员",
            "idcardNum": "12345",
            "iDNumber": "110101199001011234"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 不传id参数时，人员注册成功")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_person_registration_with_valid_id():
    """测试人员注册：传入合法id参数"""
    print("\n=== 测试2: 传入合法id参数 ===")
    url = f"{BASE_URL}/person/create"
    
    payload = {
        "pass": "123456",
        "person": {
            "id": "testperson001",
            "name": "测试人员2",
            "idcardNum": "54321",
            "iDNumber": "110101199001014321"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 传入合法id参数时，人员注册成功")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_person_registration_with_empty_name():
    """测试人员注册：name参数为空"""
    print("\n=== 测试3: name参数为空 ===")
    url = f"{BASE_URL}/person/create"
    
    payload = {
        "pass": "123456",
        "person": {
            "id": "testperson003",
            "name": "",
            "idcardNum": "67890",
            "iDNumber": "110101199001015678"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"响应: {result}")
        
        if not result["success"] and result["code"] == "LAN_EXP-3004":
            print("✅ 测试通过: name参数为空时，人员注册失败，返回正确的错误码")
        else:
            print(f"❌ 测试失败: 预期返回LAN_EXP-3004，但实际返回{result}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_person_registration_duplicate_id():
    """测试人员注册：重复id处理"""
    print("\n=== 测试4: 重复id处理 ===")
    url = f"{BASE_URL}/person/create"
    
    # 第一次注册
    payload1 = {
        "pass": "123456",
        "person": {
            "id": "testduplicate",
            "name": "测试人员7",
            "idcardNum": "77777",
            "iDNumber": "110101199001017777"
        }
    }
    
    try:
        response1 = requests.post(url, json=payload1)
        result1 = response1.json()
        print(f"第一次注册响应: {result1}")
        
        if result1["success"]:
            print("✅ 第一次注册成功")
            
            # 第二次注册，使用相同的id
            payload2 = {
                "pass": "123456",
                "person": {
                    "id": "testduplicate",
                    "name": "测试人员8",
                    "idcardNum": "88888",
                    "iDNumber": "110101199001018888"
                }
            }
            
            response2 = requests.post(url, json=payload2)
            result2 = response2.json()
            print(f"第二次注册响应: {result2}")
            
            if not result2["success"] and result2["code"] == "LAN_EXP-3005":
                print("✅ 测试通过: 重复id时，人员注册失败，返回正确的错误码")
            else:
                print(f"❌ 测试失败: 预期返回LAN_EXP-3005，但实际返回{result2}")
        else:
            print(f"❌ 第一次注册失败，{result1['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def main():
    """运行所有测试"""
    print("简单测试人员注册的核心逻辑")
    
    # 初始设置密码
    setup_password()
    
    # 运行各个测试用例
    test_person_registration_no_id()
    test_person_registration_with_valid_id()
    test_person_registration_with_empty_name()
    test_person_registration_duplicate_id()
    
    print("\n所有测试完成！")

if __name__ == "__main__":
    main()