#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试B接口透传协议中盈佳MJ200协议的解析功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from b_interface_parser import BInterfaceParser

def test_yingjia_in_b_interface():
    """直接测试B接口解析器的透传数据解析功能"""
    print("=== 测试B接口解析器的盈佳MJ200透传数据解析 ===")
    b_parser = BInterfaceParser()
    
    # 示例盈佳MJ200协议数据包
    yingjia_packet = "FA55FA55FA5500FF8048000200010000FD22FD22"
    transparent_data = bytes.fromhex(yingjia_packet)
    
    # 直接调用透传数据解析方法
    result = b_parser._parse_transparent_data(transparent_data)
    
    print("透传数据解析结果：")
    for key, value in result.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    test_yingjia_in_b_interface()
