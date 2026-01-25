#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证人员查询和注册功能
"""

import requests
import json

# 服务器地址
BASE_URL = "http://localhost:8090"

def setup_password():
    """初始设置设备密码"""
    url = f"{BASE_URL}/setPassWord"
    
    # 对于新设备，初始密码设置时oldPass和newPass相同
    payload = {
        "oldPass": "123456",
        "newPass": "123456"
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"密码设置结果: {result}")
        
        # 如果密码设置失败，可能是因为设备已经设置了密码
        if not result["success"] and "旧密码错误" in result["msg"]:
            print("设备已设置密码，尝试使用当前密码进行测试")
            # 不执行任何操作，使用当前密码继续测试
    except Exception as e:
        print(f"密码设置失败: {str(e)}")

def test_person_registration():
    """测试人员注册功能"""
    print("=== 测试人员注册功能 ===")
    
    url = f"{BASE_URL}/person/create"
    
    # 测试1：正确的参数注册
    print("\n1. 测试正确的参数注册")
    payload = {
        "pass": "123456",
        "person": {
            "name": "测试人员",
            "idcardNum": "12345",
            "iDNumber": "110101199001011234",
            "facePermission": 2,
            "idCardPermission": 2,
            "faceAndCardPermission": 1
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 正确参数注册成功")
        else:
            print(f"❌ 测试失败: {result['msg']}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 测试2：facePermission参数不合法
    print("\n2. 测试facePermission参数不合法")
    payload = {
        "pass": "123456",
        "person": {
            "name": "测试人员2",
            "idcardNum": "54321",
            "iDNumber": "110101199001014321",
            "facePermission": 3,  # 不合法的权限值
            "idCardPermission": 2,
            "faceAndCardPermission": 1
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"响应: {result}")
        
        if not result["success"] and result["code"] == "LAN_EXP-3011":
            print("✅ 测试通过: facePermission参数不合法时，返回正确的错误码")
        else:
            print(f"❌ 测试失败: 预期返回LAN_EXP-3011，但实际返回{result}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 测试3：idCardPermission参数不合法
    print("\n3. 测试idCardPermission参数不合法")
    payload = {
        "pass": "123456",
        "person": {
            "name": "测试人员3",
            "idcardNum": "67890",
            "iDNumber": "110101199001016789",
            "facePermission": 2,
            "idCardPermission": 3,  # 不合法的权限值
            "faceAndCardPermission": 1
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"响应: {result}")
        
        if not result["success"] and result["code"] == "LAN_EXP-3012":
            print("✅ 测试通过: idCardPermission参数不合法时，返回正确的错误码")
        else:
            print(f"❌ 测试失败: 预期返回LAN_EXP-3012，但实际返回{result}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 测试4：faceAndCardPermission参数不合法
    print("\n4. 测试faceAndCardPermission参数不合法")
    payload = {
        "pass": "123456",
        "person": {
            "name": "测试人员4",
            "idcardNum": "78901",
            "iDNumber": "110101199001017890",
            "facePermission": 2,
            "idCardPermission": 2,
            "faceAndCardPermission": 3  # 不合法的权限值
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"响应: {result}")
        
        if not result["success"] and result["code"] == "LAN_EXP-3013":
            print("✅ 测试通过: faceAndCardPermission参数不合法时，返回正确的错误码")
        else:
            print(f"❌ 测试失败: 预期返回LAN_EXP-3013，但实际返回{result}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_person_query():
    """测试人员查询功能"""
    print("\n=== 测试人员查询功能 ===")
    
    # 先注册一个人员
    register_url = f"{BASE_URL}/person/create"
    register_payload = {
        "pass": "123456",
        "person": {
            "id": "testperson123",
            "name": "张三",
            "idcardNum": "0541795575",
            "iDNumber": "210726199510296924",
            "facePermission": 2,
            "idCardPermission": 2,
            "faceAndCardPermission": 2
        }
    }
    
    try:
        register_response = requests.post(register_url, json=register_payload)
        if not register_response.json()["success"]:
            print("❌ 测试失败: 人员注册失败，无法进行查询测试")
            return
    except Exception as e:
        print(f"❌ 测试失败: 人员注册失败，{str(e)}")
        return
    
    # 查询单个人员
    url = f"{BASE_URL}/person/find"
    payload = {
        "pass": "123456",
        "id": "testperson123"
    }
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        print(f"查询单个人员响应: {result}")
        
        if result["success"]:
            print("✅ 测试通过: 人员查询成功")
            
            # 验证返回字段是否完整
            data = result["data"]
            if isinstance(data, list) and len(data) > 0:
                person = data[0]
                required_fields = ['id', 'name', 'idcardNum', 'iDNumber', 'facePermission', 'idCardPermission', 'faceAndCardPermission', 'createTime', 'iDPermission']
                
                for field in required_fields:
                    if field in person:
                        print(f"✅ {field} 字段存在")
                    else:
                        print(f"❌ {field} 字段缺失")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_person_update():
    """测试人员更新功能"""
    print("\n=== 测试人员更新功能 ===")
    
    # 先注册一个人员
    register_url = f"{BASE_URL}/person/create"
    register_payload = {
        "pass": "123456",
        "person": {
            "id": "testupdate123",
            "name": "初始人员",
            "idcardNum": "11111",
            "iDNumber": "110101199001011111",
            "facePermission": 1,
            "idCardPermission": 1,
            "faceAndCardPermission": 1
        }
    }
    
    try:
        register_response = requests.post(register_url, json=register_payload)
        if not register_response.json()["success"]:
            print("❌ 测试失败: 人员注册失败，无法进行更新测试")
            return
    except Exception as e:
        print(f"❌ 测试失败: 人员注册失败，{str(e)}")
        return
    
    # 更新人员，只修改name，不修改权限参数
    update_url = f"{BASE_URL}/person/update"
    update_payload = {
        "pass": "123456",
        "person": {
            "id": "testupdate123",
            "name": "更新后的人员",
            "idcardNum": "11111",
            "iDNumber": "110101199001011111"
            # 不修改权限参数，应该保留上一次的值
        }
    }
    
    try:
        update_response = requests.post(update_url, json=update_payload)
        update_result = update_response.json()
        print(f"更新人员响应: {update_result}")
        
        if update_result["success"]:
            print("✅ 测试通过: 人员更新成功")
            
            # 查询更新后的人员，验证权限参数是否保留
            query_url = f"{BASE_URL}/person/find"
            query_payload = {
                "pass": "123456",
                "id": "testupdate123"
            }
            
            query_response = requests.post(query_url, json=query_payload)
            query_result = query_response.json()
            
            if query_result["success"]:
                person = query_result["data"][0]
                print(f"更新后人员信息: {person}")
                
                # 验证权限参数是否保留了上一次的值
                if person["facePermission"] == 1 and person["idCardPermission"] == 1 and person["faceAndCardPermission"] == 1:
                    print("✅ 测试通过: 权限参数保留了上一次的值")
                else:
                    print("❌ 测试失败: 权限参数没有保留上一次的值")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def main():
    """运行所有测试"""
    print("测试人员查询和注册功能\n")
    
    # 初始设置密码
    setup_password()
    
    try:
        test_person_registration()
        test_person_query()
        test_person_update()
        print("\n🎉 所有测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    main()