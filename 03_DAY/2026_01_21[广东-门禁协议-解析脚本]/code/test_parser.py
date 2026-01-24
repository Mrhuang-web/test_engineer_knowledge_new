#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from b_interface_parser import BInterfaceParser

# 用户提供的测试数据包
user_packet = "FF3230323530313137000000000000000000000000000000000000000001002500EE010020007E3130303138303438323030454630453030303030303030303030464143380D96FE"

# 创建解析器实例
parser = BInterfaceParser()

# 解析数据包
result = parser.parse_packet(user_packet)

# 打印结果
if isinstance(result, dict):
    print("=== B接口解析结果 ===")
    for key, value in result.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
else:
    print(f"解析错误: {result}")
