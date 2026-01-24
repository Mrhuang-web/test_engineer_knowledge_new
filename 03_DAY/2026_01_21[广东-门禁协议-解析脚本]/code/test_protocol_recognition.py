#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from b_interface_parser import BInterfaceParser

class ProtocolRecognitionTest:
    """协议识别测试类"""
    
    def __init__(self):
        self.parser = BInterfaceParser()
    
    def test_bangxun_protocol(self):
        """测试邦讯协议识别"""
        print("=== 测试邦讯协议识别 ===")
        
        # 原始邦讯协议数据包示例（命令号0x1001，远程开门指令）
        bangxun_raw_packet = "10018048200EF0E00000000000FAC8"
        print(f"测试原始邦讯协议：{bangxun_raw_packet}")
        
        # 转换为字节流模拟透传数据
        try:
            bangxun_data = bytes.fromhex(bangxun_raw_packet)
            # 模拟B接口解析器的协议识别逻辑
            result = self.parser._parse_transparent_data(bangxun_data)
            print(f"识别结果：{result}")
            print()
        except Exception as e:
            print(f"测试失败：{e}")
            print()
    
    def test_zhongda_protocol(self):
        """测试中达协议识别"""
        print("=== 测试中达协议识别 ===")
        
        # 中达CHD805协议数据包示例（包含起始符0x7E和结束符0x0D）
        zhongda_raw_packet = "7E10018048200EF0E00000000000FAC80D"
        print(f"测试中达CHD805协议：{zhongda_raw_packet}")
        
        # 转换为字节流模拟透传数据
        try:
            zhongda_data = bytes.fromhex(zhongda_raw_packet)
            # 模拟B接口解析器的协议识别逻辑
            result = self.parser._parse_transparent_data(zhongda_data)
            print(f"识别结果：{result}")
            print()
        except Exception as e:
            print(f"测试失败：{e}")
            print()
    
    def run_all_tests(self):
        """运行所有测试"""
        self.test_bangxun_protocol()
        self.test_zhongda_protocol()

# 运行测试
if __name__ == "__main__":
    test = ProtocolRecognitionTest()
    test.run_all_tests()
