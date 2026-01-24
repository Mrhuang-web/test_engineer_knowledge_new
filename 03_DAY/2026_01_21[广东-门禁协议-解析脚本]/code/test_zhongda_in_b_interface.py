#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试B接口透传协议中包含中达CHD805协议的解析功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from b_interface_parser import BInterfaceParser

def test_zhongda_in_b_interface():
    """测试B接口透传协议中包含中达CHD805协议的解析"""
    print("=== 测试B接口透传协议中包含中达CHD805协议的解析 ===")
    b_parser = BInterfaceParser()
    
    # 用户提供的中达CHD805协议数据包
    user_packet = "FF3230323530313137000000000000000000000000000000000000000001002500EE010020007E3130303138303438323030454630453030303030303030303030464143380D96FE"
    
    print(f"用户提供的数据包：{user_packet}")
    print(f"数据包长度：{len(user_packet)} 字符")
    
    # 解析数据包
    result = b_parser.parse_packet(user_packet)
    
    # 输出解析结果
    if isinstance(result, dict):
        print("\n=== B接口解析结果 ===")
        for key, value in result.items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
    else:
        print(f"\n解析错误：{result}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_zhongda_in_b_interface()
