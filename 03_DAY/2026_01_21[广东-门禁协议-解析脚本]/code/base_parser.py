#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用门禁协议解析基类
为各种门禁协议解析提供基础框架
"""

class BaseParser:
    """通用门禁协议解析基类"""
    
    def __init__(self):
        self.name = "通用门禁协议"
    
    def hex_to_bytes(self, hex_string):
        """将16进制字符串转换为字节流"""
        try:
            # 移除空格并转换为字节流
            return bytes.fromhex(hex_string.replace(' ', '')), None
        except ValueError as e:
            return None, f"无效的16进制字符串: {e}"
    
    def calculate_checksum(self, data, method="xor"):
        """计算校验和
        
        Args:
            data: 要计算校验和的数据字节流
            method: 校验和计算方法，支持 "xor"（异或）、"sum"（累加和）、"crc16"（CRC16校验）
        
        Returns:
            计算得到的校验和
        """
        if method == "xor":
            checksum = 0
            for byte in data:
                checksum ^= byte
            return checksum
        elif method == "sum":
            return sum(data) & 0xFF
        elif method == "crc16":
            # 标准CRC16校验
            crc = 0xFFFF
            for byte in data:
                crc ^= byte
                for _ in range(8):
                    if crc & 0x0001:
                        crc = (crc >> 1) ^ 0xA001
                    else:
                        crc >>= 1
            return crc
        else:
            raise ValueError(f"不支持的校验和计算方法: {method}")
    
    def parse_packet(self, hex_string):
        """解析协议数据包
        
        子类需要重写此方法，实现具体的协议解析逻辑
        
        Args:
            hex_string: 16进制格式的协议数据包字符串
        
        Returns:
            解析后的字典，包含协议的各个字段信息
        """
        raise NotImplementedError("子类必须实现parse_packet方法")
    
    def format_result(self, result):
        """格式化解析结果
        
        Args:
            result: 解析后的字典
        
        Returns:
            格式化后的字符串
        """
        if isinstance(result, str):
            return result
        
        formatted = f"=== {self.name}解析结果 ===\n"
        for key, value in result.items():
            formatted += f"{key}: {value}\n"
        return formatted
    
    def get_bit_value(self, byte, bit_position):
        """获取字节中指定位置的位值
        
        Args:
            byte: 要获取位值的字节
            bit_position: 位位置，从0开始（最低位）
        
        Returns:
            位值，0或1
        """
        return (byte >> bit_position) & 0x01
    
    def parse_bcd(self, bcd_bytes):
        """解析BCD码
        
        Args:
            bcd_bytes: BCD码字节流
        
        Returns:
            解析后的十进制数值
        """
        result = 0
        for byte in bcd_bytes:
            result = result * 100 + ((byte >> 4) & 0x0F) * 10 + (byte & 0x0F)
        return result
    
    def parse_time(self, time_bytes):
        """解析时间字段
        
        子类可以重写此方法，实现具体的时间格式解析
        
        Args:
            time_bytes: 时间字段字节流
        
        Returns:
            解析后的时间字符串
        """
        return f"{time_bytes.hex()}"  # 默认返回原始16进制字符串
    
    def parse_date(self, date_bytes):
        """解析日期字段
        
        子类可以重写此方法，实现具体的日期格式解析
        
        Args:
            date_bytes: 日期字段字节流
        
        Returns:
            解析后的日期字符串
        """
        return f"{date_bytes.hex()}"  # 默认返回原始16进制字符串