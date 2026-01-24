#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
维谛ES2000门禁控制器协议解析脚本
用于解析维谛ES2000门禁控制器协议的16进制码流
"""

from base_parser import BaseParser

class VertivParser(BaseParser):
    """维谛ES2000门禁控制器协议解析器"""
    
    def __init__(self):
        super().__init__()
        self.name = "维谛ES2000门禁控制器协议"
        self.soi = b'\x7E'  # 1字节起始符
        self.eoi = b'\x0D'  # 1字节结束符
    
    def parse_packet(self, hex_string):
        """解析维谛ES2000门禁控制器协议数据包"""
        # 将16进制字符串转换为字节流
        data, error = self.hex_to_bytes(hex_string)
        if data is None:
            return error
        
        # 检查数据包长度
        if len(data) < 10:  # 最小数据包长度：1(SOI)+1(VER)+1(ADR)+1(CID1)+1(CID2/RTN)+2(L.TH)+2(CHK-SUM)+1(EOI)
            return "解析错误：数据包长度不足"
        
        # 检查起始符和结束符
        if not data.startswith(self.soi):
            return f"解析错误：起始符不正确，预期{self.soi.hex()}，实际{data[0:1].hex()}"
        
        if not data.endswith(self.eoi):
            return f"解析错误：结束符不正确，预期{self.eoi.hex()}，实际{data[-1:].hex()}"
        
        # 提取字段
        soi = data[0:1]
        ver = data[1]
        adr = data[2]
        cid1 = data[3]
        cid2_rtn = data[4]
        l_th = int.from_bytes(data[5:7], byteorder='big')
        info = data[7:-3]  # 参数/数据
        checksum = int.from_bytes(data[-3:-1], byteorder='big')
        eoi = data[-1:]
        
        # 验证数据长度
        if len(info) != l_th:
            return f"解析错误：参数长度不符，预期{l_th}字节，实际{len(info)}字节"
        
        # 验证校验和
        checksum_data = data[1:-3]  # 从VER到INFO最后字节
        calculated_checksum = sum(checksum_data) & 0xFFFF
        if calculated_checksum != checksum:
            return f"解析错误：校验和不符，预期{calculated_checksum:04X}，实际{checksum:04X}"
        
        # 解析设备分类码和分组号
        device_type = (cid1 >> 4) & 0x0F
        group_id = cid1 & 0x0F
        
        result = {
            "协议名称": self.name,
            "原始数据": hex_string,
            "数据长度": len(data),
            "起始符": soi.hex(),
            "版本号": f"0x{ver:02X}",
            "设备地址": f"0x{adr:02X}",
            "CID1": f"0x{cid1:02X}",
            "设备分类码": f"0x{device_type:02X}",
            "设备分组号": group_id,
            "CID2/RTN": f"0x{cid2_rtn:02X}",
            "参数长度": f"0x{l_th:04X}",
            "参数/数据": info.hex(),
            "校验和": f"0x{checksum:04X}",
            "计算校验和": f"0x{calculated_checksum:04X}",
            "校验和验证": "通过" if calculated_checksum == checksum else "失败",
            "结束符": eoi.hex()
        }
        
        return result
    
    def _get_command_desc(self, command):
        """获取命令描述"""
        command_map = {
            0x48: "权限确认",
            0x49: "参数设置命令",
            0x4A: "信息读取命令"
        }
        return command_map.get(command, f"未知命令（0x{command:02X}）")

# 示例用法
if __name__ == "__main__":
    parser = VertivParser()
    
    # 示例数据包（需要替换为实际的维谛ES2000协议数据包）
    example_packet = "7E100180480002000112340D"
    
    print("=== 维谛ES2000门禁控制器协议解析示例 ===")
    result = parser.parse_packet(example_packet)
    print(parser.format_result(result))