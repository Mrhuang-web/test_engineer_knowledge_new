#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试B接口透传协议中包含不同门禁协议的解析功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from b_interface_parser import BInterfaceParser

def test_b_interface_transparent_parsing():
    """测试B接口透传协议中包含不同门禁协议的解析"""
    print("=== 测试B接口透传协议的自动识别和解析功能 ===")
    b_parser = BInterfaceParser()
    
    # 测试用例1：盈佳MJ200门禁协议
    print("\n1. 测试盈佳MJ200门禁协议透传：")
    yingjia_data = b'\xFA\x55\xFA\x55\xFA\x55\x00\xFF\x80\x48\x00\x02\x00\x01\x00\x00\xFD\x22\xFD\x22'
    result = b_parser._parse_transparent_data(yingjia_data)
    print_transparent_result(result)
    
    # 测试用例2：亚奥门禁协议
    print("\n2. 测试亚奥门禁协议透传：")
    yaao_data = b'\x55\x7F\x02\x03\x00\x03\xAA'
    result = b_parser._parse_transparent_data(yaao_data)
    print_transparent_result(result)
    
    # 测试用例3：海能门禁协议
    print("\n3. 测试海能门禁协议透传：")
    haineng_data = b'\x68\x01\x02\x83\x00\x83\x0D'
    result = b_parser._parse_transparent_data(haineng_data)
    print_transparent_result(result)
    
    # 测试用例4：高新兴260R门禁协议
    print("\n4. 测试高新兴260R门禁协议透传：")
    gaoxin260r_data = b'\x7E\x20\x01\x80\x48\x00\x02\x00\x01\x12\x34\x0D'
    result = b_parser._parse_transparent_data(gaoxin260r_data)
    print_transparent_result(result)
    
    # 测试用例5：邦讯门禁协议
    print("\n5. 测试邦讯门禁协议透传：")
    bangxun_data = b'\x10\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    result = b_parser._parse_transparent_data(bangxun_data)
    print_transparent_result(result)
    
    print("\n=== 所有测试用例执行完毕 ===")

def print_transparent_result(result):
    """打印透传数据解析结果"""
    for key, value in result.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")

if __name__ == "__main__":
    test_b_interface_transparent_parsing()
