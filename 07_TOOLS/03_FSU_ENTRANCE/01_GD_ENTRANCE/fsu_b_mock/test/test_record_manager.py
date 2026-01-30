#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试记录区管理模块
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from event.record_manager import RecordManager

def test_record_manager():
    """测试记录区管理器"""
    print("=" * 60)
    print("测试记录区管理器")
    print("=" * 60)
    
    # 测试1: 基本功能测试
    print("\n1. 基本功能测试")
    print("-" * 40)
    
    # 创建记录管理器，设置最大深度为5
    record_manager = RecordManager(max_len=5)
    
    # 测试添加记录
    for i in range(3):
        record = {
            "id": i,
            "data": f"Record {i}",
            "timestamp": f"2024-01-01 12:00:0{i}"
        }
        record_manager.add_record(record)
        print(f"添加记录 {i}: {record}")
    
    # 测试记录未满时的状态
    print(f"记录未满时的状态:")
    print(f"  MAXLEN: {record_manager.MAXLEN}")
    print(f"  BOTTOM: {record_manager.BOTTOM}")
    print(f"  SAVEP: {record_manager.SAVEP}")
    print(f"  LOADP: {record_manager.LOADP}")
    print(f"  MF: 0x{record_manager.MF:02X}")
    print(f"  是否已满: {record_manager.is_full()}")
    print(f"  LOADP是否连续: {record_manager.is_loadp_continuous()}")
    print(f"  有效记录数: {record_manager.get_record_count()}")
    print(f"  LOADP有效范围: {record_manager.get_loadp_range()}")
    
    # 测试获取有效记录
    valid_records = record_manager.get_valid_records()
    print(f"  有效记录: {[r['data'] for r in valid_records]}")
    
    # 测试2: 记录已满时的覆盖逻辑
    print("\n2. 记录已满时的覆盖逻辑测试")
    print("-" * 40)
    
    # 继续添加记录，直到已满
    for i in range(3, 7):
        record = {
            "id": i,
            "data": f"Record {i}",
            "timestamp": f"2024-01-01 12:00:0{i}"
        }
        record_manager.add_record(record)
        print(f"添加记录 {i}: {record}")
        print(f"  SAVEP: {record_manager.SAVEP}")
        print(f"  MF: 0x{record_manager.MF:02X}")
        print(f"  是否已满: {record_manager.is_full()}")
    
    # 测试记录已满时的状态
    print(f"记录已满时的状态:")
    print(f"  MAXLEN: {record_manager.MAXLEN}")
    print(f"  BOTTOM: {record_manager.BOTTOM}")
    print(f"  SAVEP: {record_manager.SAVEP}")
    print(f"  LOADP: {record_manager.LOADP}")
    print(f"  MF: 0x{record_manager.MF:02X}")
    print(f"  是否已满: {record_manager.is_full()}")
    print(f"  LOADP是否连续: {record_manager.is_loadp_continuous()}")
    print(f"  有效记录数: {record_manager.get_record_count()}")
    print(f"  LOADP有效范围: {record_manager.get_loadp_range()}")
    
    # 测试获取有效记录（已满时）
    valid_records_full = record_manager.get_valid_records()
    print(f"  有效记录: {[r['data'] for r in valid_records_full]}")
    
    # 测试3: 最新和最早记录测试
    print("\n3. 最新和最早记录测试")
    print("-" * 40)
    
    print("开始获取最新记录...")
    try:
        latest_record = record_manager.get_latest_record()
        print(f"获取最新记录成功: {latest_record}")
        if latest_record:
            print(f"最新记录数据: {latest_record['data']}")
        else:
            print("最新记录为None")
    except Exception as e:
        print(f"获取最新记录时出错: {e}")
    
    print("开始获取最早记录...")
    try:
        oldest_record = record_manager.get_oldest_record()
        print(f"获取最早记录成功: {oldest_record}")
        if oldest_record:
            print(f"最早记录数据: {oldest_record['data']}")
        else:
            print("最早记录为None")
    except Exception as e:
        print(f"获取最早记录时出错: {e}")
    
    # 测试4: LOADP更新测试
    print("\n4. LOADP更新测试")
    print("-" * 40)
    
    print(f"当前LOADP: {record_manager.LOADP}")
    record_manager.update_loadp(2)
    print(f"更新后的LOADP: {record_manager.LOADP}")
    
    # 测试5: 记录区信息测试
    print("\n5. 记录区信息测试")
    print("-" * 40)
    
    record_info = record_manager.get_record_info()
    print(f"记录区信息:")
    for key, value in record_info.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_record_manager()
