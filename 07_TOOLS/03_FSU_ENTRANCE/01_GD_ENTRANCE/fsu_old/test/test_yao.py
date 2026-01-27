#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
江苏亚奥协议测试脚本
"""

import os
import sys
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
from datetime import datetime
from codec.b_interface_codec import BInterfaceCodec

def get_timestamp():
    """获取当前时间戳"""
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f]")[:-3]

# 创建B接口编解码器
codec = BInterfaceCodec()

# 江苏亚奥协议配置
JIANGSUYAO_UDP_PORT = 10111
# B接口地址规则：
# - 目的地址（P_dest_addr）：SC地址，8字节，填充00
# - 源地址（P_src_addr）：FSU ID，20字节，左对齐，右补零
JIANGSUYAO_P_DEST_ADDR = b'\x00\x00\x00\x00\x00\x00\x00\x00'  # SC地址，8字节00
JIANGSUYAO_P_SRC_ADDR = bytes.fromhex('3230323530313237').ljust(20, b'\x00')  # FSU ID，20字节
JIANGSUYAO_P_SUBDEV_TYPE = 1
JIANGSUYAO_P_SUBDEV_ADDR = 0x01
SERVER_IP = 'localhost'

def parse_jiangsuyao_response(data: bytes) -> dict:
    """
    解析江苏亚奥协议应答数据
    格式：55 + address(1) + length(1) + data_frame_type(1) + data + check(1) + AA
    Args:
        data: 江苏亚奥协议数据包
    Returns:
        解析后的字段字典
    """
    if len(data) < 5:
        return {'error': f'数据长度不足，需要至少5字节，实际{len(data)}字节'}
    
    if data[0] != 0x55:
        return {'error': f'起始符错误，期望0x55，实际0x{data[0]:02X}'}
    
    if data[-1] != 0xAA:
        return {'error': f'结束符错误，期望0xAA，实际0x{data[-1]:02X}'}
    
    address = data[1]
    length = data[2]
    data_frame_type = data[3]
    
    # 计算数据部分的长度
    data_length = len(data) - 5  # 减去起始符、地址、长度、数据帧类型、结束符和校验字段
    if data_length < 0:
        return {'error': f'长度字段错误，length={length}'}
    
    payload = data[4:-2]
    check = data[-2]
    
    result = {
        'address': f'0x{address:02X}',
        'length': f'0x{length:02X} (十进制: {length})',
        'data_frame_type': f'0x{data_frame_type:02X}',
        'payload': payload.hex(),
        'check': f'0x{check:02X}',
    }
    
    return result

def send_udp_test(data_frame_type_hex: str, test_data: bytes, description: str):
    """发送UDP测试请求（使用B接口协议）"""
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: UDP")
    print(f"[{get_timestamp()}] 数据帧类型: {data_frame_type_hex}")
    print(f"[{get_timestamp()}] 江苏亚奥数据包: {test_data.hex().upper()}")
    
    packet = codec.encode(
        test_data,
        JIANGSUYAO_P_DEST_ADDR,
        JIANGSUYAO_P_SRC_ADDR,
        JIANGSUYAO_P_SUBDEV_TYPE,
        JIANGSUYAO_P_SUBDEV_ADDR,
        comm_type=0x0001,
        rtn_flag=0x00
    )
    
    print(f"[{get_timestamp()}] B接口数据包长度: {len(packet)} 字节")
    print(f"[{get_timestamp()}] B接口数据包: {packet.hex().upper()}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        print(f"[{get_timestamp()}] 发送数据包到 {SERVER_IP}:{JIANGSUYAO_UDP_PORT}...")
        sock.sendto(packet, (SERVER_IP, JIANGSUYAO_UDP_PORT))
        
        sock.settimeout(5)
        try:
            response, addr = sock.recvfrom(1024)
            print(f"[{get_timestamp()}] 从 {addr} 收到响应: {response.hex().upper()}")
            print(f"[{get_timestamp()}] 响应长度: {len(response)} 字节")
            
            try:
                through_data, b_interface_result = codec.decode(response)
                print(f"[{get_timestamp()}] --- B接口响应 ---")
                print(f"[{get_timestamp()}] P_dest_addr: {b_interface_result.get('P_dest_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_src_addr: {b_interface_result.get('P_src_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_subDevType: {b_interface_result.get('P_subDevType', 'N/A')}")
                print(f"[{get_timestamp()}] P_subDev_addr: {b_interface_result.get('P_subDev_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_pLen: {b_interface_result.get('P_pLen', 'N/A')}")
                print(f"[{get_timestamp()}] RtnFlag: {b_interface_result.get('RtnFlag', 'N/A')}")
                print(f"[{get_timestamp()}] CommType: {b_interface_result.get('CommType', 'N/A')}")
                print(f"[{get_timestamp()}] through_data_len: {b_interface_result.get('through_data_len', 'N/A')}")
                print(f"[{get_timestamp()}] 透传数据: {through_data.hex().upper()}")
                
                jsu_resp = parse_jiangsuyao_response(through_data)
                if 'error' in jsu_resp:
                    print(f"[{get_timestamp()}] 江苏亚奥解析错误: {jsu_resp['error']}")
                else:
                    print(f"[{get_timestamp()}] --- 江苏亚奥协议响应 ---")
                    print(f"[{get_timestamp()}] Address: {jsu_resp.get('address', 'N/A')}")
                    print(f"[{get_timestamp()}] Length: {jsu_resp.get('length', 'N/A')}")
                    print(f"[{get_timestamp()}] Data Frame Type: {jsu_resp.get('data_frame_type', 'N/A')}")
                    print(f"[{get_timestamp()}] Check: {jsu_resp.get('check', 'N/A')}")
                    print(f"[{get_timestamp()}] Payload: {jsu_resp.get('payload', 'N/A')}")
                
            except Exception as e:
                print(f"[{get_timestamp()}] 解码错误: {str(e)}")
                
        except socket.timeout:
            print(f"[{get_timestamp()}] 超时未收到响应")
        except Exception as e:
            print(f"[{get_timestamp()}] 接收响应错误: {str(e)}")

if __name__ == "__main__":
    print(f"[{get_timestamp()}] ========================================")
    print(f"[{get_timestamp()}]      江苏亚奥协议测试套件")
    print(f"[{get_timestamp()}] ========================================")
    
    # 江苏亚奥协议测试包1：远程开门控制（命令类型03H）
    # 格式：55H + 地址 + 长度（04H）+ 命令字（03H）+ 组号 + 通道号 + 动作类型 + 校验 + AAH
    # 校验和：数据包所有字节的累加和，即03+02+01+01=07
    test_packet_03 = bytes.fromhex("5501040302010107AA")
    print(f"[{get_timestamp()}] 测试包03: {test_packet_03.hex().upper()}")
    
    # 发送UDP测试 - 远程开门控制
    send_udp_test("03", test_packet_03, "测试1: 江苏亚奥命令03（远程开门控制） - UDP")
    
    # 江苏亚奥协议测试包2：查询时间（命令类型09H）
    # 格式：55H + 地址 + 长度（01H）+ 命令字（09H）+ 校验（09H） + AAH
    # 校验和：数据包所有字节的累加和，即09=09
    test_packet_09 = bytes.fromhex("5501010909AA")
    print(f"[{get_timestamp()}] 测试包09: {test_packet_09.hex().upper()}")
    
    # 发送UDP测试 - 查询时间
    # send_udp_test("09", test_packet_09, "测试2: 江苏亚奥命令09（查询时间） - UDP")
    
    print(f"\n[{get_timestamp()}] ========================================")
    print(f"[{get_timestamp()}]         测试套件完成")
    print(f"[{get_timestamp()}] ========================================")
