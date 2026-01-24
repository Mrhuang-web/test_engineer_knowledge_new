#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盈佳MJ200门禁协议解析脚本
用于解析盈佳MJ200门禁协议的16进制码流
"""

from base_parser import BaseParser

class YingJiaMJ200Parser(BaseParser):
    """盈佳MJ200门禁协议解析器"""
    
    def __init__(self):
        super().__init__()
        self.name = "盈佳MJ200门禁协议"
        self.soi = b'\xFA\x55\xFA\x55\xFA\x55'  # 6字节起始符
        self.eoi = b'\xFD\x22\xFD\x22'  # 4字节结束符
    
    def parse_packet(self, hex_string):
        """解析盈佳MJ200门禁协议数据包"""
        # 将16进制字符串转换为字节流
        data, error = self.hex_to_bytes(hex_string)
        if data is None:
            return error
        
        # 检查数据包长度
        if len(data) < 20:  # 最小数据包长度：6(SOI)+1(VER)+1(ADR)+1(CID1)+1(CID2)+2(LENGTH)+2(CHKSUM)+4(EOI)
            return "解析错误：数据包长度不足"
        
        # 检查起始符和结束符
        if not data.startswith(self.soi):
            return f"解析错误：起始符不正确，预期{self.soi.hex()}，实际{data[:6].hex()}"
        
        if not data.endswith(self.eoi):
            return f"解析错误：结束符不正确，预期{self.eoi.hex()}，实际{data[-4:].hex()}"
        
        # 提取字段
        soi = data[0:6]
        ver = data[6]
        adr = data[7]
        cid1 = data[8]
        cid2 = data[9]
        length = int.from_bytes(data[10:12], byteorder='big')
        command_info = data[12:-6]  # 去掉SOI、固定字段、CHKSUM和EOI
        chksum = int.from_bytes(data[-6:-4], byteorder='big')
        eoi = data[-4:]
        
        # 验证数据长度
        if len(command_info) != length:
            return f"解析错误：命令信息长度不符，预期{length}字节，实际{len(command_info)}字节"
        
        # 验证校验和
        checksum_data = data[6:-6]  # VER到COMMAND INFO的CRC16校验
        calculated_chksum = self.calculate_checksum(checksum_data, method="crc16")
        
        # 解析命令信息
        command_info_parsed = self._parse_command_info(command_info)
        
        result = {
            "协议名称": self.name,
            "原始数据": hex_string,
            "数据长度": len(data),
            "起始符": soi.hex(),
            "协议版本号": f"0x{ver:02X}",
            "门禁地址": f"0x{adr:02X}",
            "CID1": f"0x{cid1:02X}",
            "CID2": f"0x{cid2:02X}",
            "命令类别": self._get_command_category(cid2),
            "数据长度": length,
            "命令信息": command_info.hex(),
            "命令信息解析": command_info_parsed,
            "校验和": f"0x{chksum:04X}",
            "计算校验和": f"0x{calculated_chksum:04X}",
            "校验和验证": "通过" if calculated_chksum == chksum else "失败",
            "结束符": eoi.hex()
        }
        
        return result
    
    def _parse_command_info(self, command_info):
        """解析命令信息"""
        if len(command_info) < 2:
            return {"错误": "命令信息长度不足"}
        
        result = {
            "子集码": f"0x{command_info[0]:02X}",
            "命令号": f"0x{command_info[1]:02X}"
        }
        
        if len(command_info) > 2:
            result["命令参数"] = command_info[2:].hex()
        
        return result
    
    def _get_command_category(self, cid2):
        """获取命令类别"""
        category_map = {
            0x48: "获取、取消权限的命令",
            0x49: "设置(遥控)参数的命令",
            0x4A: "读取参数、记录信息的命令"
        }
        return category_map.get(cid2, f"未知命令类别（0x{cid2:02X}")

# 示例用法
if __name__ == "__main__":
    parser = YingJiaMJ200Parser()
    
    # 示例数据包（需要替换为实际的盈佳MJ200协议数据包）
    example_packet = "FA55FA55FA5500FF8048000200010000FD22FD22"
    
    print("=== 盈佳MJ200门禁协议解析示例 ===")
    result = parser.parse_packet(example_packet)
    print(parser.format_result(result))