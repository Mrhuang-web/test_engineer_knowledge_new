#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邦讯门禁控制器协议（旧版202003）解析脚本
用于解析邦讯门禁控制器旧版协议的16进制码流
"""

from base_parser import BaseParser

class BangxunOldParser(BaseParser):
    """邦讯门禁控制器协议（旧版）解析器"""
    
    def __init__(self):
        super().__init__()
        self.name = "邦讯门禁控制器协议（旧版）"
    
    def parse_packet(self, hex_string):
        """解析邦讯旧版门禁协议数据包"""
        # 将16进制字符串转换为字节流
        data, error = self.hex_to_bytes(hex_string)
        if data is None:
            return error
        
        # 检查数据包长度
        if len(data) < 10:  # 最小数据包长度
            return "解析错误：数据包长度不足"
        
        # 示例：这里需要根据邦讯旧版协议的具体格式进行解析
        # 由于具体的协议格式未完全明确，这里提供一个基础的解析框架
        # 实际使用时需要根据完整的协议文档进行修改
        
        result = {
            "协议名称": self.name,
            "原始数据": hex_string,
            "数据长度": len(data),
            "数据包": data.hex()
        }
        
        # 示例：假设协议包含命令号、地址、数据等字段
        # 实际解析逻辑需要根据具体协议格式进行调整
        if len(data) >= 4:
            result["命令号"] = int.from_bytes(data[0:2], byteorder='big')
            result["地址"] = data[2]
            result["数据长度"] = data[3]
            
            if len(data) > 4:
                result["数据部分"] = data[4:].hex()
        
        return result
    
    def parse_time_hms(self, time_bytes):
        """解析时分秒格式"""
        if len(time_bytes) < 2:
            return "无效的时间数据"
        
        # 短时间格式：Time(HMS)（时分秒）
        # Bit Position: 0-4: Hours, 5-9: Minutes, B-F: 2-second increments
        time_value = int.from_bytes(time_bytes, byteorder='big')
        hours = (time_value >> 11) & 0x1F
        minutes = (time_value >> 5) & 0x3F
        seconds = (time_value & 0x1F) * 2
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def parse_date_ymd(self, date_bytes):
        """解析年月日格式"""
        if len(date_bytes) < 2:
            return "无效的日期数据"
        
        # 日期格式：Date(YMD)（年月日）
        # Bit Position: 0-6: Year(relative to 2000), 7-A: Month, B-F: Day
        date_value = int.from_bytes(date_bytes, byteorder='big')
        year = 2000 + ((date_value >> 9) & 0x7F)
        month = ((date_value >> 5) & 0x0F)
        day = (date_value & 0x1F)
        
        return f"{year:04d}-{month:02d}-{day:02d}"

# 示例用法
if __name__ == "__main__":
    parser = BangxunOldParser()
    
    # 示例数据包
    example_packet = "00 10 01 04 01 02 03 04"
    
    print("=== 邦讯门禁控制器协议（旧版）解析示例 ===")
    result = parser.parse_packet(example_packet)
    print(parser.format_result(result))
    
    # 示例时间解析
    print("\n=== 时间解析示例 ===")
    time_example = bytes.fromhex("5D 0D")  # 对应11时40分26秒
    print(f"原始时间数据：{time_example.hex()}")
    print(f"解析结果：{parser.parse_time_hms(time_example)}")
    
    # 示例日期解析
    print("\n=== 日期解析示例 ===")
    date_example = bytes.fromhex("02 B3")  # 对应2001年5月19日
    print(f"原始日期数据：{date_example.hex()}")
    print(f"解析结果：{parser.parse_date_ymd(date_example)}")