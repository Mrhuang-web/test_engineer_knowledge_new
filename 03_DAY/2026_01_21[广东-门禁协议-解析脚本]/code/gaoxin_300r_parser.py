#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高新兴300R门禁控制器协议解析脚本
用于解析高新兴300R门禁控制器协议的16进制码流
"""

class Gaoxin300RParser:
    """高新兴300R门禁控制器协议解析器"""
    
    def __init__(self):
        self.name = "高新兴300R门禁控制器协议"
        self.header = 0xFF
        self.tailer = 0xFE
    
    def calculate_checksum(self, data):
        """计算校验和（异或校验）"""
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum
    
    def parse_packet(self, hex_string):
        """解析高新兴300R门禁控制器协议数据包"""
        # 将16进制字符串转换为字节流
        try:
            data = bytes.fromhex(hex_string.replace(' ', ''))
        except ValueError as e:
            return f"解析错误：无效的16进制字符串 - {e}"
        
        # 检查数据包长度
        if len(data) < 40:  # 最小数据包长度
            return "解析错误：数据包长度不足"
        
        # 检查包头和包尾
        if data[0] != self.header or data[-1] != self.tailer:
            return "解析错误：包头或包尾不正确"
        
        # 固定字段位置，根据高新兴300R协议的标准格式
        # 下行方向（SC→FSU）格式：
        # 0: P_header (1 byte)
        # 1-20: P_dest_addr (20 bytes)
        # 21-28: P_src_addr (8 bytes)
        # 29: P_subDevType (1 byte)
        # 30: P_subDev_addr (1 byte)
        # 31-32: P_pLen (2 bytes)
        # 33: RtnFlag (1 byte)
        # 34-35: CommType (2 bytes)
        # 36-37: 数据流长度 (2 bytes)
        # 38-(38+N-1): 数据流 (N bytes)
        # 38+N: P_verify (1 byte)
        # 39+N: P_tailer (1 byte)
        
        # 上行方向（FSU→SC）格式：
        # 0: P_header (1 byte)
        # 1-8: P_dest_addr (8 bytes)
        # 9-28: P_src_addr (20 bytes)
        # 29: P_subDevType (1 byte)
        # 30: P_subDev_addr (1 byte)
        # 31-32: P_pLen (2 bytes)
        # 33: RtnFlag (1 byte)
        # 34-35: CommType (2 bytes)
        # 36-37: 数据流长度 (2 bytes)
        # 38-(38+N-1): 数据流 (N bytes)
        # 38+N: P_verify (1 byte)
        # 39+N: P_tailer (1 byte)
        
        # 提取RtnFlag字段判断方向
        rtn_flag = data[33]
        if rtn_flag == 0xEE:  # 下行方向（SC→FSU）
            return self._parse_downlink(data)
        elif rtn_flag == 0x00:  # 上行方向（FSU→SC）
            return self._parse_uplink(data)
        else:
            return f"解析错误：未知的RtnFlag值（0x{rtn_flag:02X}）"
    
    def _parse_downlink(self, data):
        """解析下行方向（SC→FSU）数据包"""
        # 下行方向（SC→FSU）格式：
        # 0: P_header (1 byte)
        # 1-20: P_dest_addr (20 bytes)
        # 21-28: P_src_addr (8 bytes)
        # 29: P_subDevType (1 byte)
        # 30: P_subDev_addr (1 byte)
        # 31-32: P_pLen (2 bytes)
        # 33: RtnFlag (1 byte)
        # 34-35: CommType (2 bytes)
        # 36-37: 数据流长度 (2 bytes)
        # 38-(38+N-1): 数据流 (N bytes)
        # 38+N: P_verify (1 byte)
        # 39+N: P_tailer (1 byte)
        
        # 计算数据流长度，尝试使用little-endian字节序
        stream_data_len_big = int.from_bytes(data[36:38], byteorder='big')
        stream_data_len_little = int.from_bytes(data[36:38], byteorder='little')
        
        # 计算实际的数据流长度（从38字节到倒数第二个字节）
        actual_stream_data_len = len(data) - 38 - 2  # 总长度 - 固定部分(38) - 校验和(1) - 包尾(1)
        
        result = {
            "方向": "下行（SC→FSU）",
            "包头": f"0x{data[0]:02X}",
            "目标设备地址": data[1:21].decode('ascii', errors='replace').strip('\x00'),
            "目标设备地址（十六进制）": data[1:21].hex(),
            "源设备地址": data[21:29].decode('ascii', errors='replace').strip('\x00'),
            "源设备地址（十六进制）": data[21:29].hex(),
            "子设备类型": data[29],
            "子设备类型描述": self._get_subdev_type_desc(data[29]),
            "子设备地址号": f"0x{data[30]:02X}",
            "协议族数据包长度": int.from_bytes(data[31:33], byteorder='big'),
            "设置/应答类型": f"0x{data[33]:02X}",
            "设置/应答类型描述": self._get_rtn_flag_desc(data[33]),
            "命令编号": int.from_bytes(data[34:36], byteorder='big'),
            "命令编号描述": self._get_command_desc(int.from_bytes(data[34:36], byteorder='big')),
            "数据流长度（大端）": stream_data_len_big,
            "数据流长度（小端）": stream_data_len_little,
            "数据流长度（实际）": actual_stream_data_len,
            "数据流": data[38:-2].hex(),
            "校验和": f"0x{data[-2]:02X}",
            "包尾": f"0x{data[-1]:02X}"
        }
        
        # 验证校验和
        checksum_data = data[1:-2]  # 不包含包头和包尾
        calculated_checksum = self.calculate_checksum(checksum_data)
        result["校验和验证"] = "通过" if calculated_checksum == data[-2] else "失败"
        
        return result
    
    def _parse_uplink(self, data):
        """解析上行方向（FSU→SC）数据包"""
        # 上行方向（FSU→SC）格式：
        # 0: P_header (1 byte)
        # 1-8: P_dest_addr (8 bytes)
        # 9-28: P_src_addr (20 bytes)
        # 29: P_subDevType (1 byte)
        # 30: P_subDev_addr (1 byte)
        # 31-32: P_pLen (2 bytes)
        # 33: RtnFlag (1 byte)
        # 34-35: CommType (2 bytes)
        # 36-37: 数据流长度 (2 bytes)
        # 38-(38+N-1): 数据流 (N bytes)
        # 38+N: P_verify (1 byte)
        # 39+N: P_tailer (1 byte)
        
        # 计算数据流长度，尝试使用little-endian字节序
        stream_data_len_big = int.from_bytes(data[36:38], byteorder='big')
        stream_data_len_little = int.from_bytes(data[36:38], byteorder='little')
        
        # 计算实际的数据流长度（从38字节到倒数第二个字节）
        actual_stream_data_len = len(data) - 38 - 2  # 总长度 - 固定部分(38) - 校验和(1) - 包尾(1)
        
        result = {
            "方向": "上行（FSU→SC）",
            "包头": f"0x{data[0]:02X}",
            "目标设备地址": data[1:9].decode('ascii', errors='replace').strip('\x00'),
            "目标设备地址（十六进制）": data[1:9].hex(),
            "源设备地址": data[9:29].decode('ascii', errors='replace').strip('\x00'),
            "源设备地址（十六进制）": data[9:29].hex(),
            "子设备类型": data[29],
            "子设备类型描述": self._get_subdev_type_desc(data[29]),
            "子设备地址号": f"0x{data[30]:02X}",
            "协议族数据包长度": int.from_bytes(data[31:33], byteorder='big'),
            "设置/应答类型": f"0x{data[33]:02X}",
            "设置/应答类型描述": self._get_rtn_flag_desc(data[33]),
            "命令编号": int.from_bytes(data[34:36], byteorder='big'),
            "命令编号描述": self._get_command_desc(int.from_bytes(data[34:36], byteorder='big')),
            "数据流长度（大端）": stream_data_len_big,
            "数据流长度（小端）": stream_data_len_little,
            "数据流长度（实际）": actual_stream_data_len,
            "数据流": data[38:-2].hex(),
            "校验和": f"0x{data[-2]:02X}",
            "包尾": f"0x{data[-1]:02X}"
        }
        
        # 验证校验和
        checksum_data = data[1:-2]  # 不包含包头和包尾
        calculated_checksum = self.calculate_checksum(checksum_data)
        result["校验和验证"] = "通过" if calculated_checksum == data[-2] else "失败"
        
        return result
    
    def _get_subdev_type_desc(self, subdev_type):
        """获取子设备类型描述"""
        type_map = {
            1: "串口设备",
            2: "USB设备",
            3: "IP网络设备（一体化设备也为3）"
        }
        return type_map.get(subdev_type, f"未知类型（0x{subdev_type:02X}")
    
    def _get_rtn_flag_desc(self, rtn_flag):
        """获取设置/应答类型描述"""
        flag_map = {
            0xEE: "设置类型（SC→FSU）",
            0x00: "应答类型（FSU→SC）"
        }
        return flag_map.get(rtn_flag, f"未知类型（0x{rtn_flag:02X}")
    
    def _get_command_desc(self, command):
        """获取命令编号描述"""
        command_map = {
            0x0001: "传输数据包",
            0x0002: "FSU透传通道心跳"
        }
        return command_map.get(command, f"未知命令（0x{command:04X}")

# 示例用法
if __name__ == "__main__":
    parser = Gaoxin300RParser()
    
    # 示例上行数据包
    uplink_example = "FF0000000000000000FSU1234567890ABCDEF012345678901000800000100020102000001000205060BFE"
    
    print("=== 高新兴300R门禁控制器协议解析示例 ===")
    result = parser.parse_packet(uplink_example)
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print(result)