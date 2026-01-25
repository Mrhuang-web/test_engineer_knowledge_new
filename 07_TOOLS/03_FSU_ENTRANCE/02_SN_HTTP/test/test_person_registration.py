#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证人员注册的完整逻辑
"""

import requests
import json

# 服务器地址
BASE_URL = "http://localhost:8093"

def test_person_registration_no_id():
    """测试人员注册：不传id参数，系统生成32位id"""
    print("=== 测试人员注册：不传id参数，系统生成32位id ===")
    url = f"{BASE_URL}/person/create"
    
    # 初始设置密码
    setup_password()
    
    # 使用正确的参数，但不传id
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
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 不传id参数时，人员注册成功")
            
            # 验证生成的id是否为32位
            # 由于响应中没有返回生成的id，我们可以通过查询所有人员来验证
            get_url = f"{BASE_URL}/person/find"
            get_payload = {
                "pass": "123456",
                "id": "-1"
            }
            get_response = requests.post(get_url, json=get_payload)
            get_result = get_response.json()
            
            if get_result["success"] and len(get_result["data"]) > 0:
                # 查找刚注册的人员
                for person in get_result["data"]:
                    if person["name"] == "测试人员":
                        generated_id = person["id"]
                        print(f"生成的32位id: {generated_id}")
                        if len(generated_id) == 32:
                            print("✅ 测试通过: 生成的id是32位")
                        else:
                            print(f"❌ 测试失败: 生成的id不是32位，长度为{len(generated_id)}")
                        break
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_person_registration_with_valid_id():
    """测试人员注册：传入合法id参数"""
    print("=== 测试人员注册：传入合法id参数 ===")
    url = f"{BASE_URL}/person/create"
    
    # 使用正确的参数，传入合法id
    payload = {
        "pass": "123456",
        "person": {
            "id": "test_person_001",
            "name": "测试人员2",
            "idcardNum": "54321",
            "iDNumber": "110101199001014321"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 传入合法id参数时，人员注册成功")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_person_registration_with_invalid_id():
    """测试人员注册：传入非法id参数"""
    print("=== 测试人员注册：传入非法id参数 ===")
    url = f"{BASE_URL}/person/create"
    
    # 使用非法id：包含特殊字符
    payload = {
        "pass": "123456",
        "person": {
            "id": "test_person@001",
            "name": "测试人员3",
            "idcardNum": "67890",
            "iDNumber": "110101199001015678"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if not result["success"] and result["code"] == "LAN_EXP-3003":
            print("✅ 测试通过: 传入非法id参数时，人员注册失败，返回正确的错误码")
        else:
            print(f"❌ 测试失败: 预期返回LAN_EXP-3003，但实际返回{result}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_person_registration_without_name():
    """测试人员注册：不传name参数"""
    print("=== 测试人员注册：不传name参数 ===")
    url = f"{BASE_URL}/person/create"
    
    # 不传name参数
    payload = {
        "pass": "123456",
        "person": {
            "id": "test_person_004",
            "idcardNum": "98765",
            "iDNumber": "110101199001019876"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if not result["success"] and result["code"] == "LAN_EXP-3004":
            print("✅ 测试通过: 不传name参数时，人员注册失败，返回正确的错误码")
        else:
            print(f"❌ 测试失败: 预期返回LAN_EXP-3004，但实际返回{result}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_person_registration_with_empty_name():
    """测试人员注册：name参数为空"""
    print("=== 测试人员注册：name参数为空 ===")
    url = f"{BASE_URL}/person/create"
    
    # name参数为空
    payload = {
        "pass": "123456",
        "person": {
            "id": "test_person_005",
            "name": "",
            "idcardNum": "55555",
            "iDNumber": "110101199001015555"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if not result["success"] and result["code"] == "LAN_EXP-3004":
            print("✅ 测试通过: name参数为空时，人员注册失败，返回正确的错误码")
        else:
            print(f"❌ 测试失败: 预期返回LAN_EXP-3004，但实际返回{result}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_person_registration_with_permission_params():
    """测试人员注册：权限参数处理"""
    print("=== 测试人员注册：权限参数处理 ===")
    url = f"{BASE_URL}/person/create"
    
    # 不传入权限参数，测试默认值
    payload = {
        "pass": "123456",
        "person": {
            "id": "test_person_006",
            "name": "测试人员6",
            "idcardNum": "66666",
            "iDNumber": "110101199001016666"
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"请求: {url}")
        print(f"参数: {payload}")
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 不传入权限参数时，人员注册成功")
            
            # 查询刚注册的人员，验证权限参数的默认值
            get_url = f"{BASE_URL}/person/find"
            get_payload = {
                "pass": "123456",
                "id": "test_person_006"
            }
            get_response = requests.post(get_url, json=get_payload)
            get_result = get_response.json()
            
            if get_result["success"] and len(get_result["data"]) > 0:
                person = get_result["data"][0]
                print(f"人员信息: {person}")
                
                # 验证默认值
                # facePermission: 2（默认开）
                if person.get("facePermission") == 2:
                    print("✅ 测试通过: facePermission默认值为2")
                else:
                    print(f"❌ 测试失败: facePermission默认值不正确，实际为{person.get('facePermission')}")
                
                # idCardPermission: 2（默认开）
                if person.get("idCardPermission") == 2:
                    print("✅ 测试通过: idCardPermission默认值为2")
                else:
                    print(f"❌ 测试失败: idCardPermission默认值不正确，实际为{person.get('idCardPermission')}")
                
                # faceAndCardPermission: 1（默认关）
                if person.get("faceAndCardPermission") == 1:
                    print("✅ 测试通过: faceAndCardPermission默认值为1")
                else:
                    print(f"❌ 测试失败: faceAndCardPermission默认值不正确，实际为{person.get('faceAndCardPermission')}")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_person_registration_duplicate_id():
    """测试人员注册：重复id处理"""
    print("=== 测试人员注册：重复id处理 ===")
    url = f"{BASE_URL}/person/create"
    
    # 第一次注册，使用id=test_duplicate
    payload1 = {
        "pass": "123456",
        "person": {
            "id": "test_duplicate",
            "name": "测试人员7",
            "idcardNum": "77777",
            "iDNumber": "110101199001017777"
        }
    }
    
    try:
        # 第一次注册
        response1 = requests.post(url, json=payload1)
        result1 = response1.json()
        print(f"第一次注册响应: {result1}")
        
        if result1["success"]:
            print("✅ 测试通过: 第一次注册成功")
            
            # 第二次注册，使用相同的id
            payload2 = {
                "pass": "123456",
                "person": {
                    "id": "test_duplicate",
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
            print(f"❌ 测试失败: 第一次注册失败，{result1['msg']}")
            
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
    print("测试人员注册的完整逻辑\n")
    
    # 初始设置密码
    setup_password()
    
    # 运行各个测试用例
    test_person_registration_no_id()
    test_person_registration_with_valid_id()
    test_person_registration_with_invalid_id()
    test_person_registration_without_name()
    test_person_registration_with_empty_name()
    test_person_registration_with_permission_params()
    test_person_registration_duplicate_id()
    
    print("所有测试完成！")

if __name__ == "__main__":
    main()