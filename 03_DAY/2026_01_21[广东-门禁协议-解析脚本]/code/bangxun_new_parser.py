#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邦讯门禁控制器协议（202207新版）解析脚本
用于解析邦讯新版门禁控制器协议的16进制码流
"""

from base_parser import BaseParser

class BangxunNewParser(BaseParser):
    """邦讯门禁控制器协议（202207新版）解析器"""
    
    def __init__(self):
        super().__init__()
        self.name = "邦讯门禁控制器协议（202207新版）"
    
    def parse_packet(self, hex_string):
        """解析邦讯新版门禁控制器协议数据包"""
        # 将16进制字符串转换为字节流
        data, error = self.hex_to_bytes(hex_string)
        if data is None:
            return error
        
        # 检查数据包长度
        if len(data) < 10:  # 最小数据包长度
            return "解析错误：数据包长度不足"
        
        # 提取命令号（假设命令号为2字节，大端）
        command = int.from_bytes(data[0:2], byteorder='big')
        
        # 解析命令
        result = {
            "协议名称": self.name,
            "原始数据": hex_string,
            "数据长度": len(data),
            "命令号": f"0x{command:04X}",
            "命令描述": self._get_command_desc(command)
        }
        
        # 解析命令数据
        command_data = data[2:]
        if command == 0x1081:  # 读取运行状态信息
            result["运行状态信息"] = self._parse_running_status(command_data)
        elif command == 0x10FF:  # 格式化指令
            result["格式化指令"] = "恢复出厂化设置"
        elif 0x1000 <= command <= 0x10FF:  # 其他命令
            result["命令数据"] = command_data.hex()
        
        return result
    
    def _parse_running_status(self, data):
        """解析运行状态信息"""
        if len(data) < 20:  # 最小运行状态信息长度
            return "运行状态信息长度不足"
        
        # 提取基本信息
        status_info = {
            "控制器时间": self._parse_short_time(data[0:4]),  # 假设时间占4字节
            "刷卡记录数": int.from_bytes(data[4:6], byteorder='big'),
            "权限数": int.from_bytes(data[6:8], byteorder='big'),
            "最近刷卡记录": self._parse_record(data[8:15]),  # 假设记录占7字节
            "门磁状态": data[15],
            "按钮状态": data[16],
            "故障信息": data[17:]
        }
        
        return status_info
    
    def _parse_short_time(self, time_data):
        """解析短时间格式"""
        if len(time_data) < 4:
            return "时间数据长度不足"
        
        # 解析时分秒（假设时间数据为4字节）
        time_value = int.from_bytes(time_data, byteorder='big')
        
        # Time(HMS) 时分秒格式解析
        seconds_2 = (time_value >> 11) & 0x1F  # 2秒增量，0-29
        minutes = (time_value >> 5) & 0x3F  # 分钟，0-59
        hours = time_value & 0x1F  # 小时，0-23
        
        # 转换为实际时间
        seconds = seconds_2 * 2
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def _parse_record(self, record_data):
        """解析记录格式"""
        if len(record_data) < 7:  # 记录格式：卡号(4字节) + 刷卡年月日(2字节) + 刷卡时分秒(2字节) + 记录状态(1字节)
            return "记录数据长度不足"
        
        # 提取记录字段
        card_no = int.from_bytes(record_data[0:4], byteorder='big')
        card_area = (card_no >> 16) & 0xFFFF  # 区号
        card_id = card_no & 0xFFFF  # ID号
        
        # 解析年月日（2字节）
        date_value = int.from_bytes(record_data[4:6], byteorder='big')
        day = (date_value >> 11) & 0x1F  # 日，1-31
        month = (date_value >> 7) & 0x0F  # 月，1-12
        year = (date_value & 0x7F) + 2000  # 年，0-119 relative to 2000
        
        # 解析时分秒（2字节）
        time_value = int.from_bytes(record_data[6:8], byteorder='big') if len(record_data) >= 8 else 0
        seconds_2 = (time_value >> 11) & 0x1F  # 2秒增量，0-29
        minutes = (time_value >> 5) & 0x3F  # 分钟，0-59
        hours = time_value & 0x1F  # 小时，0-23
        seconds = seconds_2 * 2
        
        # 记录状态
        record_status = record_data[7] if len(record_data) >= 8 else 0
        
        return {
            "卡号": f"{card_no:08X}",
            "区号": card_area,
            "ID号": card_id,
            "刷卡时间": f"{year}-{month:02d}-{day:02d} {hours:02d}:{minutes:02d}:{seconds:02d}",
            "记录状态": record_status
        }
    
    def _get_command_desc(self, command):
        """获取命令描述"""
        command_map = {
            0x1081: "读取运行状态信息",
            0x10FF: "格式化指令（恢复出厂化设置）",
            0x1001: "远程开门指令"
        }
        return command_map.get(command, f"未知命令（0x{command:04X}）")

# 示例用法
if __name__ == "__main__":
    parser = BangxunNewParser()
    
    # 示例数据包（需要替换为实际的邦讯新版协议数据包）
    example_packet = "108100000000000000000000000000000000000000"
    
    print("=== 邦讯新版门禁控制器协议解析示例 ===")
    result = parser.parse_packet(example_packet)
    print(parser.format_result(result))