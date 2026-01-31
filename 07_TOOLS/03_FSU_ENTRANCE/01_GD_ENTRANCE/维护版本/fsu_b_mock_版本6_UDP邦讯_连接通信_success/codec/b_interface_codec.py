#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B接口编解码器，用于处理UDP协议的外层协议封装和解析
"""

import logging
from typing import Dict, Any, Tuple, Optional

class BInterfaceCodec:
    """B接口编解码器"""
    
    # 协议常量
    P_HEADER = 0xFF
    P_TAILER = 0xFE
    ESCAPE_CHAR = 0xFD
    ESCAPE_MAP = {
        0xFF: b"\xFD\x00",
        0xFE: b"\xFD\x01",
        0xFD: b"\xFD\x02"
    }
    UNESCAPE_MAP = {
        0x00: 0xFF,
        0x01: 0xFE,
        0x02: 0xFD
    }
    
    def __init__(self):
        """初始化B接口编解码器"""
        self.logger = logging.getLogger("codec.b_interface")
    
    def decode(self, data: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """解码B接口数据
        
        Args:
            data: 原始数据
            
        Returns:
            (透传数据, 解析结果)
        """
        result = {
            "raw_data": data.hex().upper(),
            "parsed": {}
        }
        
        try:
            if len(data) < 4:  # 至少需要包含头、尾和校验
                self.logger.error("数据长度不足: %d", len(data))
                return b"", result["parsed"]
            
            # 检查包头
            if data[0] != self.P_HEADER:
                self.logger.error("包头错误: 0x%02X", data[0])
                return b"", result["parsed"]
            
            # 检查包尾
            if data[-1] != self.P_TAILER:
                self.logger.error("包尾错误: 0x%02X", data[-1])
                return b"", result["parsed"]
            
            # 反转义数据 (不包含包头和包尾)
            escaped_data = data[1:-1]
            unescaped_data = self._unescape(escaped_data)
            
            # 检查校验和
            if len(unescaped_data) < 1:
                self.logger.error("反转义后数据长度不足")
                return b"", result["parsed"]
            
            # 计算校验和 (异或校验)
            verify = unescaped_data[-1]
            calculated_verify = self._calculate_checksum(unescaped_data[:-1])
            
            if verify != calculated_verify:
                self.logger.error(f"校验和错误: 期望 0x%02X, 实际 0x%02X", calculated_verify, verify)
                return b"", result["parsed"]
            
            # 解析数据
            payload = unescaped_data[:-1]
            parsed = self._parse_payload(payload)
            result["parsed"] = parsed
            
            # 返回透传数据和解析结果（测试程序期望的格式）
            through_data = parsed.get("through_data", b"")
            return through_data, parsed
            
        except Exception as e:
            self.logger.error(f"解码失败: {str(e)}")
            return b"", result["parsed"]
    
    def encode(self, through_data: bytes, p_dest_addr: bytes, p_src_addr: bytes,
               p_subDevType: int, p_subDev_addr: int, comm_type: int = 0x0001,
               rtn_flag: int = 0x00) -> bytes:
        """编码B接口数据
        
        Args:
            through_data: 透传数据
            p_dest_addr: 目标地址
            p_src_addr: 源地址
            p_subDevType: 子设备类型
            p_subDev_addr: 子设备地址
            comm_type: 命令类型
            rtn_flag: 返回标志
            
        Returns:
            编码后的数据
        """
        try:
            # 构建解析数据字典（符合测试程序调用方式）
            parsed_data = {
                "P_dest_addr": p_dest_addr.hex().upper(),
                "P_src_addr": p_src_addr.hex().upper(),
                "P_subDevType": p_subDevType,
                "P_subDev_addr": p_subDev_addr,
                "P_pLen": 5 + len(through_data),  # 固定长度 + 透传数据长度
                "RtnFlag": rtn_flag,
                "CommType": comm_type,
                "through_data": through_data,
                "through_data_len": len(through_data)
            }
            
            # 根据命令类型设置不同的P_pLen，心跳消息没有透传数据，所以P_pLen固定为3
            if comm_type == 0x0002:  # 心跳包
                parsed_data["P_pLen"] = 3  # 心跳包固定P_pLen为3
            else:  # 普通包
                parsed_data["P_pLen"] = 5 + len(through_data)  # 固定长度 + 透传数据长度
            
            # 构建负载数据
            payload = self._build_payload(parsed_data)
            
            # 计算校验和
            verify = self._calculate_checksum(payload)
            payload_with_verify = payload + bytes([verify])
            
            # 转义数据
            escaped_data = self._escape(payload_with_verify)
            
            # 添加包头和包尾
            full_data = bytes([self.P_HEADER]) + escaped_data + bytes([self.P_TAILER])
            
            return full_data
            
        except Exception as e:
            self.logger.error(f"编码失败: {str(e)}")
            raise
    
    def _unescape(self, data: bytes) -> bytes:
        """反转义数据
        
        Args:
            data: 转义后的数据
            
        Returns:
            反转义后的数据
        """
        result = bytearray()
        i = 0
        while i < len(data):
            if data[i] == self.ESCAPE_CHAR and i + 1 < len(data):
                result.append(self.UNESCAPE_MAP.get(data[i+1], data[i+1]))
                i += 2
            else:
                result.append(data[i])
                i += 1
        return bytes(result)
    
    def _escape(self, data: bytes) -> bytes:
        """转义数据
        
        Args:
            data: 原始数据
            
        Returns:
            转义后的数据
        """
        result = bytearray()
        for b in data:
            if b in self.ESCAPE_MAP:
                result.extend(self.ESCAPE_MAP[b])
            else:
                result.append(b)
        return bytes(result)
    
    def _calculate_checksum(self, data: bytes) -> int:
        """计算校验和 (异或校验)
        
        Args:
            data: 数据
            
        Returns:
            校验和
        """
        checksum = 0
        for b in data:
            checksum ^= b
        return checksum
    
    def _parse_payload(self, payload: bytes) -> Dict[str, Any]:
        """解析负载数据
        
        Args:
            payload: 负载数据
            
        Returns:
            解析结果
        """
        parsed = {
            "P_dest_addr": "",
            "P_src_addr": "",
            "P_subDevType": 0,
            "P_subDev_addr": 0,
            "P_pLen": 0,
            "RtnFlag": 0,
            "CommType": 0,
            "through_data_len": 0,
            "through_data": b""
        }
        
        # 先解析命令类型（如果能解析到的话）
        comm_type = 0
        if len(payload) >= 35:
            comm_type = int.from_bytes(payload[33:35], byteorder="little")
        parsed["CommType"] = comm_type
        
        # 解析方向：SC发送给FSU(mock)
        # 编码顺序：目的地址(8字节，SC地址) + 源地址(20字节，FSU ID)
        # 源地址：FSU ID，20字节，左对齐，右补零
        # 目的地址：SC，8字节，填充00
        
        # 解析目的地址 (8字节，SC地址)
        if len(payload) >= 8:
            parsed["P_dest_addr"] = payload[0:8].hex().upper()
        
        # 解析源地址 (20字节，FSU ID)
        if len(payload) >= 28:
            parsed["P_src_addr"] = payload[8:28].hex().upper()
        
        # 解析子设备类型 (1字节)
        if len(payload) >= 29:
            parsed["P_subDevType"] = payload[28]
        
        # 解析子设备地址 (1字节)
        if len(payload) >= 30:
            parsed["P_subDev_addr"] = payload[29]
        
        # 解析数据长度 (2字节，小端)
        if len(payload) >= 32:
            parsed["P_pLen"] = int.from_bytes(payload[30:32], byteorder="little")
        
        # 解析返回标志 (1字节)
        if len(payload) >= 33:
            parsed["RtnFlag"] = payload[32]
                
        # 只有非心跳包（CommandType != 0x0002）才包含透传数据长度和透传数据字段
        if comm_type != 0x0002:
            # 解析透传数据长度 (2字节，小端)
            if len(payload) >= 37:
                parsed["through_data_len"] = int.from_bytes(payload[35:37], byteorder="little")
            
            # 解析透传数据
            if len(payload) >= 37 + parsed["through_data_len"]:
                parsed["through_data"] = payload[37:37 + parsed["through_data_len"]]
            # 如果小端解析失败，尝试用大端序重新解析
            elif len(payload) >= 37:
                parsed["through_data_len"] = int.from_bytes(payload[35:37], byteorder="big")
                if len(payload) >= 37 + parsed["through_data_len"]:
                    parsed["through_data"] = payload[37:37 + parsed["through_data_len"]]
        
        return parsed
    
    def _build_payload(self, parsed_data: Dict[str, Any]) -> bytes:
        """构建负载数据
        
        Args:
            parsed_data: 解析后的数据
            
        Returns:
            负载数据
        """
        payload = bytearray()
        
        # 获取命令类型
        comm_type = parsed_data.get("CommType", 0)
        
        # 根据B接口地址通用原则构建地址
        # 1. 目的地址：
        #    - 不管什么情况，目的地址都是8字节（SC地址），填充00
        # 2. 源地址：
        #    - 不管什么情况，源地址都是20字节（FSU ID），左对齐，右补零
        
        # 目的地址 (8字节，SC地址，填充00)
        dest_addr = parsed_data.get("P_dest_addr", "")
        if dest_addr:
            # 如果提供了目的地址，取前16个字符（8字节）
            payload.extend(bytes.fromhex(dest_addr.ljust(16, '0')[:16]))
        else:
            payload.extend(b'\x00' * 8)
        
        # 源地址 (20字节，FSU ID，左对齐，右补零)
        src_addr = parsed_data.get("P_src_addr", "")
        if src_addr:
            # 如果提供了源地址，取前40个字符（20字节），左对齐，右补零
            payload.extend(bytes.fromhex(src_addr.ljust(40, '0')[:40]))
        else:
            payload.extend(b'\x00' * 20)
        
        # 子设备类型 (1字节)
        payload.append(parsed_data.get("P_subDevType", 0))
        
        # 子设备地址 (1字节)
        payload.append(parsed_data.get("P_subDev_addr", 0))
        
        # 数据长度 (2字节，小端)
        p_len = parsed_data.get("P_pLen", 0)
        payload.extend(p_len.to_bytes(2, byteorder="little"))
        
        # 返回标志 (1字节)
        payload.append(parsed_data.get("RtnFlag", 0))
        
        # 命令类型 (2字节，小端)
        payload.extend(comm_type.to_bytes(2, byteorder="little"))
        
        # 只有非心跳包（CommandType != 0x0002）才包含透传数据长度和透传数据字段
        if comm_type != 0x0002:
            # 透传数据长度 (2字节，小端)
            through_len = len(parsed_data.get("through_data", b""))
            payload.extend(through_len.to_bytes(2, byteorder="little"))
            
            # 透传数据
            payload.extend(parsed_data.get("through_data", b""))
        
        return bytes(payload)
    
    def to_str(self, result: Dict[str, Any]) -> str:
        """将解析结果转换为字符串
        
        Args:
            result: 解析结果
            
        Returns:
            格式化的字符串
        """
        raw_data = result.get("raw_data", "")
        parsed = result.get("parsed", {})
        
        # 计算数据包长度字节数
        data_length = len(raw_data) // 2  # 每两个字符代表一个字节
        
        # 格式化原始HEX，每两个字符添加一个空格
        formatted_hex = ' '.join(raw_data[i:i+2] for i in range(0, len(raw_data), 2))
        lines = [f"数据包长度: {data_length} 字节", f"HEX: {formatted_hex}", "Parsed:"]
        
        # 添加B接口协议字段
        fields = [
            ("P_header", "0xFF"),
            ("P_dest_addr", parsed.get("P_dest_addr", "")),
            ("P_src_addr", parsed.get("P_src_addr", "")),
            ("P_subDevType", f"0x{parsed.get('P_subDevType', 0):02X}"),
            ("P_subDev_addr", f"0x{parsed.get('P_subDev_addr', 0):02X}"),
            ("P_pLen", f"0x{parsed.get('P_pLen', 0):04X}"),
            ("RtnFlag", f"0x{parsed.get('RtnFlag', 0):02X}"),
            ("CommType", f"0x{parsed.get('CommType', 0):04X}")
        ]
        
        # 只有非心跳包（CommandType != 0x0002）才添加透传数据长度和透传数据字段
        comm_type = parsed.get('CommType', 0)
        if comm_type != 0x0002:
            fields.extend([
                ("透传数据长度", f"0x{parsed.get('through_data_len', 0):04X}"),
                ("透传数据", parsed.get('through_data', b"").hex().upper())
            ])
        
        fields.extend([
            ("P_verify", f"0x{parsed.get('P_verify', 0):02X}"),
            ("P_tailer", "0xFE")
        ])
        
        for key, value in fields:
            lines.append(f"    {key}: {value}")
        
        return "\n".join(lines)
    
    def build_heartbeat(self, fsu_config: Dict[str, Any]) -> bytes:
        """构建心跳包
        
        Args:
            fsu_config: FSU配置
            
        Returns:
            心跳包数据
        """
        # 构建心跳包数据，符合要求的格式
        through_data = b""  # 心跳包没有透传数据
        p_dest_addr = b"\x00" * 8  # 目标地址：SC的地址取值为0x00，8字节
        p_src_addr = bytes.fromhex(fsu_config.get("fsuid", "").ljust(40, '0')[:40])  # 源地址：FSU的ID，20字节
        p_subDevType = 1  # 子设备类型01
        p_subDev_addr = 1  # 子设备地址
        comm_type = 0x0002  # 心跳命令类型
        rtn_flag = 0xED  # 返回标志值为ED
        
        return self.encode(
            through_data=through_data,
            p_dest_addr=p_dest_addr,
            p_src_addr=p_src_addr,
            p_subDevType=p_subDevType,
            p_subDev_addr=p_subDev_addr,
            comm_type=comm_type,
            rtn_flag=rtn_flag
        )
