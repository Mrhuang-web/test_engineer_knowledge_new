#!/usr/bin/env python3
# Test client for Haineng protocol

import os
import sys
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
import struct
from datetime import datetime
from codec.b_interface_codec import BInterfaceCodec

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def calculate_haineng_checksum(data: bytes) -> int:
    """
    计算海能协议的校验和（异或校验）
    Args:
        data: 需要计算校验和的数据（不包含起始符68和结束符0D，以及校验和字段本身）
    Returns:
        校验和（1字节）
    """
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def build_haineng_packet(address: int, command: int, data: bytes) -> bytes:
    """
    构建海能协议数据包
    格式：68 + address(1) + length(1) + command(1) + data + checksum(1) + 0D
    Args:
        address: 地址
        command: 命令类型
        data: 数据
    Returns:
        完整数据包
    """
    packet = bytearray()
    packet.append(0x68)
    packet.append(address)
    
    # 计算长度：命令(1) + 数据长度 + 校验和(1)
    length = 1 + len(data) + 1
    packet.append(length)
    
    packet.append(command)
    packet.extend(data)
    
    # 计算校验和：address + length + command + data
    checksum_data = packet[1:]
    checksum = calculate_haineng_checksum(checksum_data)
    packet.append(checksum)
    
    packet.append(0x0D)
    
    return bytes(packet)

def parse_haineng_response(data: bytes) -> dict:
    """
    解析海能协议应答数据
    格式：68 + address(1) + length(1) + command(1) + data + checksum(1) + 0D
    Args:
        data: 海能协议数据包
    Returns:
        解析后的字段字典
    """
    if len(data) < 5:
        return {'error': f'数据长度不足，需要至少5字节，实际{len(data)}字节'}
    
    if data[0] != 0x68:
        return {'error': f'起始符错误，期望0x68，实际0x{data[0]:02X}'}
    
    if data[-1] != 0x0D:
        return {'error': f'结束符错误，期望0x0D，实际0x{data[-1]:02X}'}
    
    address = data[1]
    length = data[2]
    command = data[3]
    
    # 计算数据部分的长度
    data_length = length - 2  # 减去命令(1)和校验和(1)
    if data_length < 0:
        return {'error': f'长度字段错误，length={length}'}
    
    if len(data) < 4 + data_length + 1:
        return {'error': f'数据长度不足，期望{4 + data_length + 1}字节，实际{len(data)}字节'}
    
    payload = data[4:4 + data_length]
    checksum = data[4 + data_length]
    
    calculated_checksum = calculate_haineng_checksum(data[1:4 + data_length])
    checksum_valid = checksum == calculated_checksum
    
    result = {
        'address': f'0x{address:02X}',
        'length': f'0x{length:02X}',
        'command': f'0x{command:02X}',
        'payload': payload.hex(),
        'checksum': f'0x{checksum:02X}',
        'calculated_checksum': f'0x{calculated_checksum:02X}',
        'checksum_valid': checksum_valid
    }
    
    # 解析83命令的响应数据
    if command == 0x83 and len(payload) >= 3:
        result['group_no'] = f'0x{payload[0]:02X}'
        result['channel_no'] = f'0x{payload[1]:02X}'
        result['action'] = f'0x{payload[2]:02X}'
    
    # 解析89命令的响应数据
    if command == 0x89 and len(payload) >= 8:
        result['year'] = f'0x{payload[0]:02X}{payload[1]:02X}'
        result['month'] = f'0x{payload[2]:02X}'
        result['day'] = f'0x{payload[3]:02X}'
        result['week'] = f'0x{payload[4]:02X}'
        result['hour'] = f'0x{payload[5]:02X}'
        result['minute'] = f'0x{payload[6]:02X}'
        result['second'] = f'0x{payload[7]:02X}'
    
    return result

codec = BInterfaceCodec()

SERVER_IP = 'localhost'
UDP_PORT = 10113  # haineng_01的UDP端口
TCP_PORT = 10114  # haineng_02的TCP端口

# Haineng FSU ID
FSU_ID = 'haineng_01'
p_dest_addr = bytes(20)  # 目标地址设为全0
p_src_addr = bytes.fromhex('3230323530313237').ljust(20, b'\x00')  # 源地址设为海能 FSU ID
p_subDevType = 1  # 默认子设备类型
p_subDev_addr = 0  # 默认子设备地址

def send_udp_test(command_hex: str, test_data: bytes, description: str):
    """发送UDP测试请求（使用B接口协议）"""
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: UDP")
    print(f"[{get_timestamp()}] 命令: {command_hex}")
    print(f"[{get_timestamp()}] 海能数据包: {test_data.hex()}")
    
    packet = codec.encode(
        test_data,
        p_dest_addr,
        p_src_addr,
        p_subDevType,
        p_subDev_addr,
        comm_type=0x0001,
        rtn_flag=0x00
    )
    
    print(f"[{get_timestamp()}] B接口数据包长度: {len(packet)} 字节")
    print(f"[{get_timestamp()}] B接口数据包: {packet.hex()}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        print(f"[{get_timestamp()}] 发送数据包到 {SERVER_IP}:{UDP_PORT}...")
        sock.sendto(packet, (SERVER_IP, UDP_PORT))
        
        sock.settimeout(2)
        try:
            response, addr = sock.recvfrom(1024)
            print(f"[{get_timestamp()}] 从 {addr} 收到响应: {response.hex()}")
            print(f"[{get_timestamp()}] 响应长度: {len(response)} 字节")
            
            try:
                through_data, decoded_response = codec.decode(response)
                print(f"[{get_timestamp()}] --- B接口响应 ---")
                print(f"[{get_timestamp()}] P_header: {decoded_response.get('P_header', 'N/A')}")
                print(f"[{get_timestamp()}] P_dest_addr: {decoded_response.get('P_dest_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_src_addr: {decoded_response.get('P_src_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_subDevType: {decoded_response.get('P_subDevType', 'N/A')}")
                print(f"[{get_timestamp()}] P_subDev_addr: {decoded_response.get('P_subDev_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_pLen: {decoded_response.get('P_pLen', 'N/A')}")
                print(f"[{get_timestamp()}] RtnFlag: {decoded_response.get('RtnFlag', 'N/A')}")
                print(f"[{get_timestamp()}] CommType: {decoded_response.get('CommType', 'N/A')}")
                print(f"[{get_timestamp()}] 透传数据长度: {decoded_response.get('透传数据长度', 'N/A')}")
                print(f"[{get_timestamp()}] 透传数据: {through_data.hex()}")
                
                haineng_resp = parse_haineng_response(through_data)
                if 'error' in haineng_resp:
                    print(f"[{get_timestamp()}] 海能解析错误: {haineng_resp['error']}")
                else:
                    print(f"[{get_timestamp()}] --- 海能协议响应 ---")
                    print(f"[{get_timestamp()}] 地址: {haineng_resp.get('address', 'N/A')}")
                    print(f"[{get_timestamp()}] 命令: {haineng_resp.get('command', 'N/A')}")
                    print(f"[{get_timestamp()}] 校验和: {haineng_resp.get('checksum', 'N/A')} (有效: {haineng_resp.get('checksum_valid', False)})")
                    
                    if command_hex == '83':
                        print(f"[{get_timestamp()}] 组号: {haineng_resp.get('group_no', 'N/A')}")
                        print(f"[{get_timestamp()}] 通道号: {haineng_resp.get('channel_no', 'N/A')}")
                        print(f"[{get_timestamp()}] 动作: {haineng_resp.get('action', 'N/A')}")
                    elif command_hex == '89':
                        print(f"[{get_timestamp()}] 年: {haineng_resp.get('year', 'N/A')}")
                        print(f"[{get_timestamp()}] 月: {haineng_resp.get('month', 'N/A')}")
                        print(f"[{get_timestamp()}] 日: {haineng_resp.get('day', 'N/A')}")
                        print(f"[{get_timestamp()}] 星期: {haineng_resp.get('week', 'N/A')}")
                        print(f"[{get_timestamp()}] 时: {haineng_resp.get('hour', 'N/A')}")
                        print(f"[{get_timestamp()}] 分: {haineng_resp.get('minute', 'N/A')}")
                        print(f"[{get_timestamp()}] 秒: {haineng_resp.get('second', 'N/A')}")
                
            except Exception as e:
                print(f"[{get_timestamp()}] 解码错误: {str(e)}")
                
        except socket.timeout:
            print(f"[{get_timestamp()}] 超时未收到响应")
        except Exception as e:
            print(f"[{get_timestamp()}] 接收响应错误: {str(e)}")

def send_tcp_test(command_hex: str, test_data: bytes, description: str):
    """发送TCP测试请求（直接透传，不需要B接口协议）"""
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: TCP")
    print(f"[{get_timestamp()}] 命令: {command_hex}")
    print(f"[{get_timestamp()}] 海能数据包: {test_data.hex()}")
    
    # TCP协议包直接通过fsu端口透传到设备，不需要经过B接口外层协议编码
    packet = test_data
    
    print(f"[{get_timestamp()}] TCP数据包长度: {len(packet)} 字节")
    print(f"[{get_timestamp()}] TCP数据包: {packet.hex()}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"[{get_timestamp()}] 连接到 {SERVER_IP}:{TCP_PORT}...")
        try:
            sock.connect((SERVER_IP, TCP_PORT))
            print(f"[{get_timestamp()}] 连接成功")
            
            print(f"[{get_timestamp()}] 发送数据...")
            sock.sendall(packet)
            
            sock.settimeout(2)
            try:
                response = sock.recv(1024)
                print(f"[{get_timestamp()}] 收到响应: {response.hex()}")
                print(f"[{get_timestamp()}] 响应长度: {len(response)} 字节")
                
                try:
                    # TCP响应也不会经过B接口编码，直接解析透传数据
                    haineng_resp = parse_haineng_response(response)
                    if 'error' in haineng_resp:
                        print(f"[{get_timestamp()}] 海能解析错误: {haineng_resp['error']}")
                    else:
                        print(f"[{get_timestamp()}] --- 海能协议响应 ---")
                        print(f"[{get_timestamp()}] 地址: {haineng_resp.get('address', 'N/A')}")
                        print(f"[{get_timestamp()}] 命令: {haineng_resp.get('command', 'N/A')}")
                        print(f"[{get_timestamp()}] 校验和: {haineng_resp.get('checksum', 'N/A')} (有效: {haineng_resp.get('checksum_valid', False)})")
                        
                        if command_hex == '83':
                            print(f"[{get_timestamp()}] 组号: {haineng_resp.get('group_no', 'N/A')}")
                            print(f"[{get_timestamp()}] 通道号: {haineng_resp.get('channel_no', 'N/A')}")
                            print(f"[{get_timestamp()}] 动作: {haineng_resp.get('action', 'N/A')}")
                        elif command_hex == '89':
                            print(f"[{get_timestamp()}] 年: {haineng_resp.get('year', 'N/A')}")
                            print(f"[{get_timestamp()}] 月: {haineng_resp.get('month', 'N/A')}")
                            print(f"[{get_timestamp()}] 日: {haineng_resp.get('day', 'N/A')}")
                            print(f"[{get_timestamp()}] 星期: {haineng_resp.get('week', 'N/A')}")
                            print(f"[{get_timestamp()}] 时: {haineng_resp.get('hour', 'N/A')}")
                            print(f"[{get_timestamp()}] 分: {haineng_resp.get('minute', 'N/A')}")
                            print(f"[{get_timestamp()}] 秒: {haineng_resp.get('second', 'N/A')}")
                except Exception as e:
                    print(f"[{get_timestamp()}] 解码错误: {str(e)}")
            except socket.timeout:
                print(f"[{get_timestamp()}] 超时未收到响应")
            except Exception as e:
                print(f"[{get_timestamp()}] 接收响应错误: {str(e)}")
        except Exception as e:
            print(f"[{get_timestamp()}] 连接服务器错误: {str(e)}")

print(f"[{get_timestamp()}] ========================================")
print(f"[{get_timestamp()}]         海能协议测试套件")
print(f"[{get_timestamp()}] ========================================")

# 构建83命令数据包
# 83命令：group_no=00, channel_no=00, action=00
command_83 = 0x83
data_83 = b'\x00\x00\x00'
test_83_packet = build_haineng_packet(0x01, command_83, data_83)
print(f"[{get_timestamp()}] 83命令数据包: {test_83_packet.hex()}")

# 构建89命令数据包
# 89命令：无数据
command_89 = 0x89
data_89 = b''
test_89_packet = build_haineng_packet(0x01, command_89, data_89)
print(f"[{get_timestamp()}] 89命令数据包: {test_89_packet.hex()}")

# 构建90命令数据包
# 90命令：设置时间，数据格式：year(2字节) + month(1字节) + day(1字节) + hour(1字节) + minute(1字节) + second(1字节)
command_90 = 0x90
now = datetime.now()
# 年：2字节，大端序
year_bytes = struct.pack('>H', now.year)
# 月、日、时、分、秒：各1字节
time_data = year_bytes + \
            now.month.to_bytes(1, byteorder='big') + \
            now.day.to_bytes(1, byteorder='big') + \
            now.hour.to_bytes(1, byteorder='big') + \
            now.minute.to_bytes(1, byteorder='big') + \
            now.second.to_bytes(1, byteorder='big')
test_90_packet = build_haineng_packet(0x01, command_90, time_data)
print(f"[{get_timestamp()}] 90命令数据包: {test_90_packet.hex()}")

# 发送UDP测试
# send_udp_test("83", test_83_packet, "测试1: 海能命令83 - UDP")
# send_udp_test("89", test_89_packet, "测试2: 海能命令89 - UDP")
send_udp_test("90", test_90_packet, "测试3: 海能命令90 - 设置时间 - UDP")

# 发送TCP测试
# send_tcp_test("83", test_83_packet, "测试3: 海能命令83 - TCP")
# send_tcp_test("89", test_89_packet, "测试4: 海能命令89 - TCP")

print(f"\n[{get_timestamp()}] ========================================")
print(f"[{get_timestamp()}]         测试套件完成")
print(f"[{get_timestamp()}] ========================================")
