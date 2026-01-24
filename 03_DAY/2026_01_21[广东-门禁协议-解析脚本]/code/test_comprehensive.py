#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from b_interface_parser import BInterfaceParser

class ComprehensiveProtocolTest:
    """综合协议解析测试类"""
    
    def __init__(self):
        self.parser = BInterfaceParser()
        self.test_cases = [
            {
                "name": "邦讯协议（命令号0x1001）",
                "transparent_data": b"~10018048200EF0E00000000000FAC8\r"
            },
            {
                "name": "中达CHD805协议",
                "transparent_data": b"~7E10018048200EF0E00000000000FAC80D\r"
            },
            {
                "name": "高新兴260R协议（版本号0x20）",
                "transparent_data": b"~7E20018048200EF0E00000000000FAC80D\r"
            },
            {
                "name": "力维/维谛/钛迪协议（版本号0x10）",
                "transparent_data": b"~7E10018048200EF0E00000000000FAC80D\r"
            },
            {
                "name": "亚奥协议（起始符0x55）",
                "transparent_data": b"~550102030405060708090A0B0C0D\r"
            },
            {
                "name": "海能协议（起始符0x68）",
                "transparent_data": b"~680102030405060708090A0B0C0D\r"
            }
        ]
    
    def run_tests(self):
        """运行所有测试用例"""
        print("=== 综合协议解析测试 ===")
        print("测试各种协议的透传数据解包和识别")
        print("=" * 50)
        
        for test_case in self.test_cases:
            print(f"\n测试：{test_case['name']}")
            print(f"透传数据：{test_case['transparent_data'].hex()}")
            
            try:
                # 调用透传数据解析方法
                result = self.parser._parse_transparent_data(test_case['transparent_data'])
                
                # 打印解析结果
                print("解析结果：")
                if isinstance(result, dict):
                    for key, value in result.items():
                        if isinstance(value, dict):
                            print(f"  {key}:")
                            for sub_key, sub_value in value.items():
                                print(f"    {sub_key}: {sub_value}")
                        else:
                            print(f"  {key}: {value}")
                else:
                    print(f"  解析错误：{result}")
                    
            except Exception as e:
                print(f"  测试失败：{e}")
        
        print("\n" + "=" * 50)
        print("=== 测试完成 ===")

# 运行测试
if __name__ == "__main__":
    test = ComprehensiveProtocolTest()
    test.run_tests()
