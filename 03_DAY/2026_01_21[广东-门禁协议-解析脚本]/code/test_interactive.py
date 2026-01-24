#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ProtocolParserMain

class MockProtocolParserMain(ProtocolParserMain):
    """模拟交互式输入的协议解析器测试类"""
    
    def get_user_input(self):
        """模拟用户输入选择中达CHD805协议"""
        return "12"
    
    def get_hex_string(self):
        """模拟用户输入测试数据包"""
        return "FF3230323530313137000000000000000000000000000000000000000001002500EE010020007E3130303138303438323030454630453030303030303030303030464143380D96FE"

# 运行测试
if __name__ == "__main__":
    print("=== 测试交互式协议解析器 ===")
    print("测试场景：选择中达CHD805协议解析器，输入包含B接口的数据包")
    print("=" * 50)
    
    main = MockProtocolParserMain()
    
    # 模拟一次解析过程
    parser_info = main.parsers["12"]
    print(f"\n已选择：{parser_info['name']}")
    
    hex_string = main.get_hex_string()
    print(f"输入的16进制码流：{hex_string}")
    
    print("\n正在解析...")
    
    # 测试新的解析逻辑
    try:
        data = bytes.fromhex(hex_string.replace(' ', ''))
        if data[0] == 0xFF and "12" != "1":
            # 包含B接口，自动先使用B接口解析器解析
            print("检测到B接口封装，自动先解析B接口...")
            from b_interface_parser import BInterfaceParser
            b_parser = BInterfaceParser()
            b_result = b_parser.parse_packet(hex_string)
            if isinstance(b_result, dict) and "透传数据解析" in b_result:
                result = b_result
            else:
                # B接口解析失败，再尝试直接用选择的解析器解析
                result = parser_info["parser"].parse_packet(hex_string)
        else:
            # 不包含B接口或已选择B接口解析器，直接解析
            result = parser_info["parser"].parse_packet(hex_string)
    except ValueError:
        # 无效的16进制字符串，直接解析
        result = parser_info["parser"].parse_packet(hex_string)
    
    print("\n解析结果：")
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
    else:
        print(result)
    
    print("\n" + "=" * 50)
    print("测试完成")
