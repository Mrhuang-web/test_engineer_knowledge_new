#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证数据存储功能
"""

import json
import os
import shutil
from configs.storage_config import storage_config
from datastore.data_store import data_store as global_data_store

# 测试数据目录
TEST_DATA_DIR = 'test_data'

# 保存原始配置
original_use_json = storage_config['use_json_storage']
original_dir = storage_config['json_storage_dir']

# 测试函数

def test_memory_storage():
    """测试内存存储功能"""
    print("=== 测试内存存储功能 ===")
    
    # 确保使用内存存储
    storage_config['use_json_storage'] = False
    storage_config['json_storage_dir'] = TEST_DATA_DIR
    
    # 重新创建数据存储实例
    from datastore.data_store import DataStore
    data_store = DataStore()
    
    # 测试设置设备密码
    data_store.set_password('test_pass')
    assert data_store.get_password() == 'test_pass'
    print("✅ 设备密码设置成功")
    
    # 测试创建人员信息
    person_info = {
        'name': '测试人员',
        'idcardNum': '12345',
        'iDNumber': '110101199001011234'
    }
    data_store.create_person('test123', person_info)
    assert 'test123' in data_store.persons
    print("✅ 人员信息创建成功")
    
    # 检查JSON文件是否没有创建
    json_files = os.listdir(TEST_DATA_DIR)
    assert len(json_files) == 0
    print("✅ 内存存储时，没有创建JSON文件")
    
    print("内存存储测试通过！\n")

def test_json_storage():
    """测试JSON文件存储功能"""
    print("=== 测试JSON文件存储功能 ===")
    
    # 确保使用JSON存储
    storage_config['use_json_storage'] = True
    storage_config['json_storage_dir'] = TEST_DATA_DIR
    
    # 清空测试数据目录
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    os.makedirs(TEST_DATA_DIR)
    
    # 重新创建数据存储实例
    from datastore.data_store import DataStore
    data_store = DataStore()
    
    # 测试设置设备密码
    data_store.set_password('test_pass')
    assert data_store.get_password() == 'test_pass'
    print("✅ 设备密码设置成功")
    
    # 测试创建人员信息
    person_info = {
        'name': '测试人员',
        'idcardNum': '12345',
        'iDNumber': '110101199001011234'
    }
    data_store.create_person('test123', person_info)
    assert 'test123' in data_store.persons
    print("✅ 人员信息创建成功")
    
    # 检查JSON文件是否创建
    json_files = os.listdir(TEST_DATA_DIR)
    expected_files = ['device_pass.json', 'persons.json']
    for expected_file in expected_files:
        assert expected_file in json_files
    print(f"✅ JSON文件创建成功：{json_files}")
    
    # 测试从JSON文件加载数据
    # 重新创建数据存储实例，应该从JSON文件加载数据
    data_store2 = DataStore()
    assert data_store2.get_password() == 'test_pass'
    assert 'test123' in data_store2.persons
    assert data_store2.persons['test123']['name'] == '测试人员'
    print("✅ 从JSON文件加载数据成功")
    
    print("JSON文件存储测试通过！\n")

def test_storage_switch():
    """测试存储方式切换"""
    print("=== 测试存储方式切换 ===")
    
    # 测试1：使用JSON存储
    storage_config['use_json_storage'] = True
    storage_config['json_storage_dir'] = TEST_DATA_DIR
    
    # 清空测试数据目录
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    os.makedirs(TEST_DATA_DIR)
    
    from datastore.data_store import DataStore
    data_store = DataStore()
    
    # 创建测试数据
    data_store.set_password('json_pass')
    data_store.create_person('json_test', {
        'name': 'JSON测试人员',
        'idcardNum': '54321',
        'iDNumber': '110101199001014321'
    })
    
    # 检查JSON文件是否创建
    assert 'device_pass.json' in os.listdir(TEST_DATA_DIR)
    assert 'persons.json' in os.listdir(TEST_DATA_DIR)
    print("✅ JSON存储模式下，数据保存到文件")
    
    # 测试2：切换到内存存储
    storage_config['use_json_storage'] = False
    
    # 重新创建数据存储实例
    data_store2 = DataStore()
    
    # 初始状态应该是空的
    assert data_store2.get_password() is None
    assert len(data_store2.persons) == 0
    print("✅ 切换到内存存储后，初始状态为空")
    
    # 创建内存存储数据
    data_store2.set_password('memory_pass')
    data_store2.create_person('memory_test', {
        'name': '内存测试人员',
        'idcardNum': '67890',
        'iDNumber': '110101199001016789'
    })
    
    # 检查JSON文件是否没有更新
    with open(os.path.join(TEST_DATA_DIR, 'device_pass.json'), 'r') as f:
        saved_pass = json.load(f)
    assert saved_pass == 'json_pass'  # 应该是之前保存的JSON数据，而不是新的内存数据
    print("✅ 内存存储模式下，不会更新JSON文件")
    
    print("存储方式切换测试通过！\n")

def test_data_persistence():
    """测试数据持久化"""
    print("=== 测试数据持久化 ===")
    
    # 确保使用JSON存储
    storage_config['use_json_storage'] = True
    storage_config['json_storage_dir'] = TEST_DATA_DIR
    
    # 清空测试数据目录
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    os.makedirs(TEST_DATA_DIR)
    
    # 重新创建数据存储实例
    from datastore.data_store import DataStore
    data_store = DataStore()
    
    # 测试数据持久化
    
    # 1. 设置设备密码
    data_store.set_password('persist_pass')
    
    # 2. 创建多个人员
    for i in range(3):
        person_info = {
            'name': f'测试人员{i}',
            'idcardNum': f'12345{i}',
            'iDNumber': f'11010119900101123{i}'
        }
        data_store.create_person(f'test{i}', person_info)
    
    # 3. 检查人员数量
    assert len(data_store.persons) == 3
    print("✅ 创建多个人员成功")
    
    # 4. 删除一个人员
    data_store.delete_person('test1')
    assert len(data_store.persons) == 2
    print("✅ 删除人员成功")
    
    # 5. 重新创建数据存储实例，加载数据
    data_store2 = DataStore()
    
    # 6. 验证数据完整性
    assert data_store2.get_password() == 'persist_pass'
    assert len(data_store2.persons) == 2
    assert 'test0' in data_store2.persons
    assert 'test2' in data_store2.persons
    assert 'test1' not in data_store2.persons
    print("✅ 数据持久化测试通过")
    
    print("数据持久化测试通过！\n")

def cleanup():
    """清理测试资源"""
    # 恢复原始配置
    storage_config['use_json_storage'] = original_use_json
    storage_config['json_storage_dir'] = original_dir
    
    # 删除测试数据目录
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    
    print("测试资源清理完成！")

def main():
    """运行所有测试"""
    print("测试数据存储功能\n")
    
    try:
        test_memory_storage()
        test_json_storage()
        test_storage_switch()
        test_data_persistence()
        print("🎉 所有测试通过！")
    except AssertionError as e:
        print(f"❌ 测试失败：{e}")
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
    finally:
        cleanup()

if __name__ == "__main__":
    main()