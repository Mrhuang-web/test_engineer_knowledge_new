#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试脚本：直接测试人员查询和注册的业务逻辑
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from business_logic.person import PersonService
from datastore.data_store import DataStore

# 创建测试数据存储实例
class TestDataStore(DataStore):
    """测试用的数据存储，绕过密码验证"""
    def verify_password(self, password):
        """测试时，所有密码都视为正确"""
        return True

def test_person_registration():
    """测试人员注册功能"""
    print("=== 单元测试：人员注册功能 ===")
    
    # 创建测试数据存储和人员服务
    test_data_store = TestDataStore()
    person_service = PersonService()
    person_service.data_store = test_data_store
    
    # 测试1：正确的参数注册
    print("\n1. 测试正确的参数注册")
    params = {
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
    
    result = person_service.create_person(params)
    print(f"响应: {result}")
    
    if result["success"]:
        print("✅ 测试通过: 正确参数注册成功")
    else:
        print(f"❌ 测试失败: {result['msg']}")
    
    # 测试2：facePermission参数不合法
    print("\n2. 测试facePermission参数不合法")
    params = {
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
    
    result = person_service.create_person(params)
    print(f"响应: {result}")
    
    if not result["success"] and result["code"] == "LAN_EXP-3011":
        print("✅ 测试通过: facePermission参数不合法时，返回正确的错误码")
    else:
        print(f"❌ 测试失败: 预期返回LAN_EXP-3011，但实际返回{result}")
    
    # 测试3：idCardPermission参数不合法
    print("\n3. 测试idCardPermission参数不合法")
    params = {
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
    
    result = person_service.create_person(params)
    print(f"响应: {result}")
    
    if not result["success"] and result["code"] == "LAN_EXP-3012":
        print("✅ 测试通过: idCardPermission参数不合法时，返回正确的错误码")
    else:
        print(f"❌ 测试失败: 预期返回LAN_EXP-3012，但实际返回{result}")
    
    # 测试4：faceAndCardPermission参数不合法
    print("\n4. 测试faceAndCardPermission参数不合法")
    params = {
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
    
    result = person_service.create_person(params)
    print(f"响应: {result}")
    
    if not result["success"] and result["code"] == "LAN_EXP-3013":
        print("✅ 测试通过: faceAndCardPermission参数不合法时，返回正确的错误码")
    else:
        print(f"❌ 测试失败: 预期返回LAN_EXP-3013，但实际返回{result}")

def test_person_formatting():
    """测试人员数据格式化功能"""
    print("\n=== 单元测试：人员数据格式化功能 ===")
    
    # 创建测试数据存储和人员服务
    test_data_store = TestDataStore()
    person_service = PersonService()
    person_service.data_store = test_data_store
    
    # 先注册一个人员
    params = {
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
    
    register_result = person_service.create_person(params)
    if not register_result["success"]:
        print("❌ 测试失败: 人员注册失败，无法进行格式化测试")
        return
    
    # 测试人员数据格式化
    print("\n1. 测试人员数据格式化")
    person = test_data_store.get_person("testperson123")
    formatted_person = person_service._format_person_data(person)
    
    print(f"格式化后的人员数据: {formatted_person}")
    
    # 验证返回字段是否完整
    required_fields = ['id', 'name', 'idcardNum', 'iDNumber', 'facePermission', 'idCardPermission', 'faceAndCardPermission', 'createTime', 'iDPermission']
    
    all_fields_exist = True
    for field in required_fields:
        if field in formatted_person:
            print(f"✅ {field} 字段存在")
        else:
            print(f"❌ {field} 字段缺失")
            all_fields_exist = False
    
    if all_fields_exist:
        print("✅ 测试通过: 所有必需字段都存在")
    else:
        print("❌ 测试失败: 缺少必需字段")

def test_person_update():
    """测试人员更新功能"""
    print("\n=== 单元测试：人员更新功能 ===")
    
    # 创建测试数据存储和人员服务
    test_data_store = TestDataStore()
    person_service = PersonService()
    person_service.data_store = test_data_store
    
    # 先注册一个人员
    register_params = {
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
    
    register_result = person_service.create_person(register_params)
    if not register_result["success"]:
        print("❌ 测试失败: 人员注册失败，无法进行更新测试")
        return
    
    # 测试更新人员，只修改name，不修改权限参数
    print("\n1. 测试人员更新，不修改权限参数")
    update_params = {
        "pass": "123456",
        "person": {
            "id": "testupdate123",
            "name": "更新后的人员",
            "idcardNum": "11111",
            "iDNumber": "110101199001011111"
            # 不修改权限参数，应该保留上一次的值
        }
    }
    
    update_result = person_service.update_person(update_params)
    print(f"更新响应: {update_result}")
    
    if update_result["success"]:
        print("✅ 测试通过: 人员更新成功")
        
        # 查询更新后的人员，验证权限参数是否保留
        updated_person = test_data_store.get_person("testupdate123")
        print(f"更新后人员信息: {updated_person}")
        
        # 验证权限参数是否保留了上一次的值
        if updated_person["facePermission"] == 1 and updated_person["idCardPermission"] == 1 and updated_person["faceAndCardPermission"] == 1:
            print("✅ 测试通过: 权限参数保留了上一次的值")
        else:
            print("❌ 测试失败: 权限参数没有保留上一次的值")
    else:
        print(f"❌ 测试失败: {update_result['msg']}")

def main():
    """运行所有单元测试"""
    print("人员查询和注册功能单元测试\n")
    
    try:
        test_person_registration()
        test_person_formatting()
        test_person_update()
        print("\n🎉 所有单元测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    main()