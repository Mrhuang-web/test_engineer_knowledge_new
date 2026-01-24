#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试盈佳MJ200协议在B接口透传中的解析功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from b_interface_parser import BInterfaceParser
from yingjia_mj200_parser import YingJiaMJ200Parser

def test_yingjia_direct():
    """直接测试盈佳MJ200协议解析"""
    print("=== 直接测试盈佳MJ200协议解析 ===")
    parser = YingJiaMJ200Parser()
    
    # 示例盈佳MJ200协议数据包
    yingjia_packet = "FA55FA55FA5500FF8048000200010000FD22FD22"
    
    print(f"测试数据包: {yingjia_packet}")
    result = parser.parse_packet(yingjia_packet)
    print(parser.format_result(result))
    print("\n" + "="*50 + "\n")

def test_yingjia_in_b_interface():
    """测试B接口透传协议中包含盈佳MJ200协议"""
    print("=== 测试B接口透传协议中包含盈佳MJ200协议 ===")
    b_parser = BInterfaceParser()
    
    # 示例盈佳MJ200协议数据包
    yingjia_packet = "FA55FA55FA5500FF8048000200010000FD22FD22"
    
    # 构造B接口下行数据包
    # 格式：FF + 目标地址(20字节) + 源地址(8字节) + 子设备类型(1) + 子设备地址(1) + 
    #       协议族长度(2) + RtnFlag(1) + 命令类型(2) + 透传数据长度(2) + 透传数据 + 校验和(1) + FE
    
    # 目标地址（20字节，ASCII）
    dest_addr = "20250112".ljust(20, '\x00').encode('ascii')
    
    # 源地址（8字节，ASCII）
    src_addr = "3000000000000000".encode('ascii')
    
    # 子设备类型：1（串口设备）
    subdev_type = b'\x01'
    
    # 子设备地址：0
    subdev_addr = b'\x00'
    
    # 协议族长度：30（计算值，实际长度需要调整）
    p_len = b'\x00\x1E'
    
    # RtnFlag：EE（下行）
    rtn_flag = b'\xEE'
    
    # 命令类型：0100（透传串口数据）
    comm_type = b'\x01\x00'
    
    # 透传数据长度（2字节，little-endian）
    transparent_data = bytes.fromhex(yingjia_packet)
    transparent_data_len = len(transparent_data).to_bytes(2, byteorder='little')
    
    # 构建数据包主体
    packet_body = dest_addr + src_addr + subdev_type + subdev_addr + p_len + rtn_flag + comm_type + transparent_data_len + transparent_data
    
    # 计算校验和（异或校验，不包含包头和包尾）
    checksum = 0
    for byte in packet_body:
        checksum ^= byte
    checksum = bytes([checksum])
    
    # 完整的B接口数据包
    b_packet = b'\xFF' + packet_body + checksum + b'\xFE'
    b_packet_hex = b_packet.hex()
    
    print(f"构造的B接口数据包: {b_packet_hex}")
    print(f"数据包长度: {len(b_packet)} 字节")
    
    # 解析B接口数据包
    result = b_parser.parse_packet(b_packet_hex)
    
    if isinstance(result, dict):
        print("\n=== B接口协议解析结果 ===")
        for key, value in result.items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")
    else:
        print(f"解析错误: {result}")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_yingjia_direct()
    test_yingjia_in_b_interface()
