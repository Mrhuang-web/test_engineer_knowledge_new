#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from b_interface_parser import BInterfaceParser

class FailedCaseTest:
    """失败案例测试类"""
    
    def __init__(self):
        self.parser = BInterfaceParser()
    
    def test_failed_case(self):
        """测试用户提供的失败案例"""
        print("=== 测试用户提供的失败案例 ===")
        
        # 用户提供的失败案例中的透传数据
        # 透传数据（十六进制）: 7e79f781100000000000000000000000000000000000000000000001020d
        transparent_data = bytes.fromhex('7e79f781100000000000000000000000000000000000000000000001020d')
        
        print(f"测试透传数据：{transparent_data.hex()}")
        print(f"透传数据（ASCII）：{transparent_data.decode('ascii', errors='replace')}")
        print()
        
        try:
            # 调用透传数据解析方法
            result = self.parser._parse_transparent_data(transparent_data)
            
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
        
        print()
        print("=== 测试完成 ===")

# 运行测试
if __name__ == "__main__":
    test = FailedCaseTest()
    test.test_failed_case()
