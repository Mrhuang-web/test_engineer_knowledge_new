#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海能门禁控制器协议解析脚本
用于解析海能门禁控制器协议的16进制码流
"""

from base_parser import BaseParser

class HainengParser(BaseParser):
    """海能门禁控制器协议解析器"""
    
    def __init__(self):
        super().__init__()
        self.name = "海能门禁控制器协议"
        self.soi = b'\x68'  # 1字节起始符
        self.eoi = b'\x0D'  # 1字节结束符
    
    def parse_packet(self, hex_string):
        """解析海能门禁控制器协议数据包"""
        # 将16进制字符串转换为字节流
        data, error = self.hex_to_bytes(hex_string)
        if data is None:
            return error
        
        # 检查数据包长度
        if len(data) < 5:  # 最小数据包长度：1(SOI)+1(地址)+1(长度)+1(命令)+1(校验和)+1(EOI)
            return "解析错误：数据包长度不足"
        
        # 检查起始符和结束符
        if not data.startswith(self.soi):
            return f"解析错误：起始符不正确，预期{self.soi.hex()}，实际{data[0:1].hex()}"
        
        if not data.endswith(self.eoi):
            return f"解析错误：结束符不正确，预期{self.eoi.hex()}，实际{data[-1:].hex()}"
        
        # 提取字段
        soi = data[0:1]
        address = data[1]
        length = data[2]
        packet_data = data[3:-2]  # 命令+参数/数据
        checksum = data[-2]
        eoi = data[-1:]
        
        # 验证数据长度
        if len(packet_data) != length:
            return f"解析错误：命令数据长度不符，预期{length}字节，实际{len(packet_data)}字节"
        
        # 验证校验和
        calculated_checksum = sum(packet_data) & 0xFF
        if calculated_checksum != checksum:
            return f"解析错误：校验和不符，预期{calculated_checksum:02X}，实际{checksum:02X}"
        
        # 解析命令
        command = packet_data[0] if len(packet_data) > 0 else 0
        command_params = packet_data[1:] if len(packet_data) > 1 else b''
        
        # 解析命令信息
        command_info_parsed = self._parse_command_info(command, command_params)
        
        result = {
            "协议名称": self.name,
            "原始数据": hex_string,
            "数据长度": len(data),
            "起始符": soi.hex(),
            "地址": f"0x{address:02X}",
            "长度": length,
            "命令": f"0x{command:02X}",
            "命令描述": self._get_command_desc(command),
            "命令参数": command_params.hex(),
            "命令参数解析": command_info_parsed,
            "校验和": f"0x{checksum:02X}",
            "计算校验和": f"0x{calculated_checksum:02X}",
            "校验和验证": "通过" if calculated_checksum == checksum else "失败",
            "结束符": eoi.hex()
        }
        
        return result
    
    def _parse_command_info(self, command, command_params):
        """解析命令信息"""
        result = {}
        
        if command == 0x81:  # 上报组信息
            if len(command_params) == 8:
                group_types = []
                for i in range(8):
                    group_type = command_params[i]
                    group_types.append(f"组{i+1}：{self._get_group_type_desc(group_type)}")
                result["组类型信息"] = group_types
        elif command == 0x82:  # 上报门禁运行数据
            if len(command_params) > 0:
                # 解析多个板数据
                board_data_list = []
                i = 0
                while i < len(command_params):
                    if i + 1 > len(command_params):
                        break
                    
                    board_id = command_params[i]
                    group_id = (board_id >> 4) & 0x0F
                    group_type = board_id & 0x0F
                    
                    board_data = {
                        "板识别字": f"0x{board_id:02X}",
                        "组号": group_id,
                        "组类型": self._get_group_type_desc(group_type)
                    }
                    
                    # 解析组数据
                    i += 1
                    if group_type == 0x02 and i + 16 <= len(command_params):  # AI组数据
                        # 8个通道×2字节/通道，低字节在前，高字节在后
                        channel_data = []
                        for j in range(8):
                            value = int.from_bytes(command_params[i+j*2:i+j*2+2], byteorder='little', signed=True)
                            channel_data.append(f"通道{j}：{value}")
                        board_data["AI组数据"] = channel_data
                        i += 16
                    elif group_type == 0x04 and i + 1 <= len(command_params):  # DI组数据
                        # 8路数字输入，每bit对应1个通道
                        di_data = command_params[i]
                        channel_status = []
                        for j in range(8):
                            status = (di_data >> j) & 0x01
                            channel_status.append(f"通道{j}：{status} ({'正常' if status else '告警'})")
                        board_data["DI组数据"] = channel_status
                        i += 1
                    elif group_type == 0x06 and i + 1 <= len(command_params):  # DO组数据
                        # 8路数字输出，每bit对应1个通道
                        do_data = command_params[i]
                        channel_status = []
                        for j in range(8):
                            status = (do_data >> j) & 0x01
                            channel_status.append(f"通道{j}：{status} ({'开启' if status else '关闭'})")
                        board_data["DO组数据"] = channel_status
                        i += 1
                    else:
                        break
                    
                    board_data_list.append(board_data)
                
                result["板数据"] = board_data_list
        
        return result
    
    def _get_command_desc(self, command):
        """获取命令描述"""
        command_map = {
            0x81: "上报组信息",
            0x82: "上报门禁运行数据",
            0x83: "示例命令（文档示例）"
        }
        return command_map.get(command, f"未知命令（0x{command:02X}）")