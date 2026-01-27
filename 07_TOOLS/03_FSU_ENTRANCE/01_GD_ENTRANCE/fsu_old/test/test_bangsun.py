#!/usr/bin/env python3
# Test client for Bangsun old protocol

import os
import sys
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
import struct
from datetime import datetime
from codec.b_interface_codec import BInterfaceCodec
from server.base_protocol import BaseProtocol

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def calculate_bangsun_checksum(data: bytes) -> int:
    """
    计算邦讯协议的校验和（异或校验）
    Args:
        data: 需要计算校验和的数据（不包含包头7E和包尾0D，以及校验和字段本身）
    Returns:
        校验和（2字节，小端序）
    """
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def build_bangsun_packet(address: int, func_type: int, data: bytes) -> bytes:
    """
    构建邦讯协议数据包
    格式：7E + address(2, 小端) + func_type(2, 小端) + data(26) + checksum(2, 小端) + 0D
    Args:
        address: 板地址
        func_type: 功能类型
        data: 数据（26字节）
    Returns:
        完整数据包
    """
    packet = bytearray()
    packet.append(0x7E)
    packet.extend(struct.pack('<H', address))
    packet.extend(struct.pack('<H', func_type))
    
    if len(data) < 26:
        data = data + b'\x00' * (26 - len(data))
    packet.extend(data[:26])
    
    checksum_data = packet[1:31]
    checksum = calculate_bangsun_checksum(checksum_data)
    packet.extend(struct.pack('<H', checksum))
    packet.append(0x0D)
    
    return bytes(packet)

codec = BInterfaceCodec()

SERVER_IP = 'localhost'
UDP_PORT = 10102
TCP_PORT = 10102
fsuid = '88888888'

p_dest_addr = bytes.fromhex(fsuid).ljust(20, b'\x00')
p_src_addr = b'\x00\x00\x00\x00\x00\x00\x00\x00'
p_subDevType = 1
p_subDev_addr = 1

def parse_bangsun_response(data: bytes) -> dict:
    """
    解析邦讯协议应答数据
    格式：7E + address(2, 小端) + func_type(2, 小端) + data(26) + checksum(2, 小端) + 0D
    Args:
        data: 邦讯协议数据包
    Returns:
        解析后的字段字典
    """
    if len(data) < 34:
        return {'error': f'数据长度不足，需要至少34字节，实际{len(data)}字节'}
    
    if data[0] != 0x7E:
        return {'error': f'包头错误，期望0x7E，实际0x{data[0]:02X}'}
    
    if data[-1] != 0x0D:
        return {'error': f'包尾错误，期望0x0D，实际0x{data[-1]:02X}'}
    
    address = struct.unpack('<H', data[1:3])[0]
    func_type = struct.unpack('<H', data[3:5])[0]
    payload = data[5:31]
    checksum = struct.unpack('<H', data[31:33])[0]
    
    calculated_checksum = calculate_bangsun_checksum(data[1:31])
    checksum_valid = checksum == calculated_checksum
    
    result = {
        'address': f'0x{address:04X}',
        'func_type': f'0x{func_type:04X}',
        'payload': payload.hex(),
        'checksum': f'0x{checksum:04X}',
        'calculated_checksum': f'0x{calculated_checksum:04X}',
        'checksum_valid': checksum_valid
    }
    
    if func_type == 0x108B and len(payload) >= 7:
        result['year'] = f'0x{payload[0]:02X} ({2000 + payload[0]})'
        result['month'] = f'0x{payload[1]:02X} ({payload[1]})'
        result['day'] = f'0x{payload[2]:02X} ({payload[2]})'
        result['week'] = f'0x{payload[3]:02X} ({payload[3]})'
        result['hour'] = f'0x{payload[4]:02X} ({payload[4]})'
        result['minute'] = f'0x{payload[5]:02X} ({payload[5]})'
        result['second'] = f'0x{payload[6]:02X} ({payload[6]})'
    
    if func_type == 0x1081 and len(payload) >= 21:  # 7个时间字段 + 3个record_count + 2个permission_count + 8个record_value + 1个relay_status = 21字节
        result['year'] = f'0x{payload[0]:02X} ({2000 + payload[0]})'
        result['month'] = f'0x{payload[1]:02X} ({payload[1]})'
        result['day'] = f'0x{payload[2]:02X} ({payload[2]})'
        result['week'] = f'0x{payload[3]:02X} ({payload[3]})'
        result['hour'] = f'0x{payload[4]:02X} ({payload[4]})'
        result['minute'] = f'0x{payload[5]:02X} ({payload[5]})'
        result['second'] = f'0x{payload[6]:02X} ({payload[6]})'
        result['record_count'] = f'0x{struct.unpack_from("<I", payload, 7)[0]:06X}'
        result['permission_count'] = f'0x{struct.unpack_from("<H", payload, 10)[0]:04X}'
        result['record_value'] = f'0x{struct.unpack_from("<Q", payload, 12)[0]:016X}'
        result['relay_status'] = f'0x{payload[20]:02X}'
    
    return result

def send_udp_test(func_type_hex: str, test_data: bytes, description: str):
    """发送UDP测试请求（使用B接口协议）"""
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: UDP")
    print(f"[{get_timestamp()}] 功能类型: {func_type_hex}")
    print(f"[{get_timestamp()}] 邦讯数据包: {test_data.hex()}")
    
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
                print(f"[{get_timestamp()}] through_data_len: {decoded_response.get('through_data_len', 'N/A')}")
                print(f"[{get_timestamp()}] 透传数据: {through_data.hex()}")
                
                bangsun_resp = parse_bangsun_response(through_data)
                if 'error' in bangsun_resp:
                    print(f"[{get_timestamp()}] 邦讯解析错误: {bangsun_resp['error']}")
                else:
                    print(f"[{get_timestamp()}] --- 邦讯协议响应 ---")
                    print(f"[{get_timestamp()}] 地址: {bangsun_resp.get('address', 'N/A')}")
                    print(f"[{get_timestamp()}] 功能类型: {bangsun_resp.get('func_type', 'N/A')}")
                    print(f"[{get_timestamp()}] 校验和: {bangsun_resp.get('checksum', 'N/A')} (有效: {bangsun_resp.get('checksum_valid', False)})")
                    
                    if func_type_hex == '108B' or func_type_hex == '1081':
                        print(f"[{get_timestamp()}] 年: {bangsun_resp.get('year', 'N/A')}")
                        print(f"[{get_timestamp()}] 月: {bangsun_resp.get('month', 'N/A')}")
                        print(f"[{get_timestamp()}] 日: {bangsun_resp.get('day', 'N/A')}")
                        print(f"[{get_timestamp()}] 星期: {bangsun_resp.get('week', 'N/A')}")
                        print(f"[{get_timestamp()}] 时: {bangsun_resp.get('hour', 'N/A')}")
                        print(f"[{get_timestamp()}] 分: {bangsun_resp.get('minute', 'N/A')}")
                        print(f"[{get_timestamp()}] 秒: {bangsun_resp.get('second', 'N/A')}")
                    
                    if func_type_hex == '1081':
                        print(f"[{get_timestamp()}] 记录数量: {bangsun_resp.get('record_count', 'N/A')}")
                        print(f"[{get_timestamp()}] 权限数量: {bangsun_resp.get('permission_count', 'N/A')}")
                        print(f"[{get_timestamp()}] 记录值: {bangsun_resp.get('record_value', 'N/A')}")
                        print(f"[{get_timestamp()}] 继电器状态: {bangsun_resp.get('relay_status', 'N/A')}")
                
            except Exception as e:
                print(f"[{get_timestamp()}] 解码错误: {str(e)}")
                
        except socket.timeout:
            print(f"[{get_timestamp()}] 超时未收到响应")
        except Exception as e:
            print(f"[{get_timestamp()}] 接收响应错误: {str(e)}")

def send_tcp_test(func_type_hex: str, test_data: bytes, description: str):
    """发送TCP测试请求（直接透传，不需要B接口协议）"""
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: TCP")
    print(f"[{get_timestamp()}] 功能类型: {func_type_hex}")
    print(f"[{get_timestamp()}] 邦讯数据包: {test_data.hex()}")
    
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
                    bangsun_resp = parse_bangsun_response(response)
                    if 'error' in bangsun_resp:
                        print(f"[{get_timestamp()}] 邦讯解析错误: {bangsun_resp['error']}")
                    else:
                        print(f"[{get_timestamp()}] --- 邦讯协议响应 ---")
                        print(f"[{get_timestamp()}] 地址: {bangsun_resp.get('address', 'N/A')}")
                        print(f"[{get_timestamp()}] 功能类型: {bangsun_resp.get('func_type', 'N/A')}")
                        print(f"[{get_timestamp()}] 校验和: {bangsun_resp.get('checksum', 'N/A')} (有效: {bangsun_resp.get('checksum_valid', False)})")
                        
                        if func_type_hex == '108B' or func_type_hex == '1081':
                            print(f"[{get_timestamp()}] 年: {bangsun_resp.get('year', 'N/A')}")
                            print(f"[{get_timestamp()}] 月: {bangsun_resp.get('month', 'N/A')}")
                            print(f"[{get_timestamp()}] 日: {bangsun_resp.get('day', 'N/A')}")
                            print(f"[{get_timestamp()}] 星期: {bangsun_resp.get('week', 'N/A')}")
                            print(f"[{get_timestamp()}] 时: {bangsun_resp.get('hour', 'N/A')}")
                            print(f"[{get_timestamp()}] 分: {bangsun_resp.get('minute', 'N/A')}")
                            print(f"[{get_timestamp()}] 秒: {bangsun_resp.get('second', 'N/A')}")
                        
                        if func_type_hex == '1081':
                            print(f"[{get_timestamp()}] 记录数量: {bangsun_resp.get('record_count', 'N/A')}")
                            print(f"[{get_timestamp()}] 权限数量: {bangsun_resp.get('permission_count', 'N/A')}")
                            print(f"[{get_timestamp()}] 记录值: {bangsun_resp.get('record_value', 'N/A')}")
                            print(f"[{get_timestamp()}] 继电器状态: {bangsun_resp.get('relay_status', 'N/A')}")
                except Exception as e:
                    print(f"[{get_timestamp()}] 解码错误: {str(e)}")
            except socket.timeout:
                print(f"[{get_timestamp()}] 超时未收到响应")
            except Exception as e:
                print(f"[{get_timestamp()}] 接收响应错误: {str(e)}")
        except Exception as e:
                    print(f"[{get_timestamp()}] 连接服务器错误: {str(e)}")


def send_heartbeat_test(description: str):
    """
    发送心跳包测试（使用B接口协议）
    """
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: UDP")
    print(f"[{get_timestamp()}] 功能类型: 心跳包")
    print(f"[{get_timestamp()}] 命令类型: 0x0002")
    
    # 心跳包不需要透传数据，直接构建B接口数据包
    packet = codec.encode(
        b"",  # 透传数据为空
        p_dest_addr,
        p_src_addr,
        p_subDevType,
        p_subDev_addr,
        comm_type=0x0002,  # 心跳命令类型
        rtn_flag=0xEE
    )
    
    print(f"[{get_timestamp()}] B接口数据包长度: {len(packet)} 字节")
    print(f"[{get_timestamp()}] B接口数据包: {packet.hex()}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        print(f"[{get_timestamp()}] 发送心跳包到 {SERVER_IP}:{UDP_PORT}...")
        sock.sendto(packet, (SERVER_IP, UDP_PORT))
        
        sock.settimeout(2)
        try:
            response, addr = sock.recvfrom(1024)
            print(f"[{get_timestamp()}] 从 {addr} 收到响应: {response.hex()}")
            print(f"[{get_timestamp()}] 响应长度: {len(response)} 字节")
        except socket.timeout:
            print(f"[{get_timestamp()}] 超时未收到响应（心跳包正常）")
        except Exception as e:
            print(f"[{get_timestamp()}] 接收响应错误: {str(e)}")


def build_108b_data() -> bytes:
    """
    构建108B测试数据（设置门禁时间）
    """
    now = datetime.now()
    year = now.year - 2000
    # month = now.month
    month = now.month + 1
    day = now.day
    week = now.weekday()
    hour = now.hour
    minute = now.minute
    second = now.second
    
    data = bytearray()
    data.append(year)
    data.append(month)
    data.append(day)
    data.append(week)
    data.append(hour)
    data.append(minute)
    data.append(second)
    
    return bytes(data)


def test_rule_placeholder_rendering():
    proto = BaseProtocol()
    parsed_request = {
        "through_pdu": {},
        "through_sdu": {"datetime": "11223344556677"},
    }
    rule = {"delay_ms": 100, "data": {"datetime": "#{datetime}#"}}
    rendered = proto._render_rule_data_placeholders(rule, parsed_request)
    assert rendered["data"]["datetime"] == "11223344556677"
    assert rule["data"]["datetime"] == "#{datetime}#"

def build_1081_data() -> bytes:
    """
    构建1081测试数据（门禁记录查询）
    """
    data = bytearray()
    # 4字节的first字段，这里使用0x00000000作为测试数据
    data.extend(b'\x00\x00\x00\x00')
    
    return bytes(data)

print(f"[{get_timestamp()}] ========================================")
print(f"[{get_timestamp()}]         邦讯协议测试套件")
print(f"[{get_timestamp()}] ========================================")

test_108b_data = build_108b_data()
print(f"[{get_timestamp()}] 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"[{get_timestamp()}] 108B数据: {test_108b_data.hex()}")

test_108b_packet = build_bangsun_packet(0x0001, 0x108B, test_108b_data)
print(f"[{get_timestamp()}] 108B数据包: {test_108b_packet.hex()}")

test_rule_placeholder_rendering()

send_udp_test("108B", test_108b_packet, "测试1: 设置门禁时间 (108B) - UDP")
# send_tcp_test("108B", test_108b_packet, "测试2: 设置门禁时间 (108B) - TCP")

# # 添加1081测试
# test_1081_data = build_1081_data()
# print(f"[{get_timestamp()}] 1081数据: {test_1081_data.hex()}")

# test_1081_packet = build_bangsun_packet(0x0001, 0x1081, test_1081_data)
# print(f"[{get_timestamp()}] 1081数据包: {test_1081_packet.hex()}")
#
# send_udp_test("1081", test_1081_packet, "测试3: 门禁记录查询 (1081) - UDP")
# send_tcp_test("1081", test_1081_packet, "测试4: 门禁记录查询 (1081) - TCP")

# 添加心跳测试
# send_heartbeat_test("测试5: 发送心跳包 (0x0002) - UDP")

print(f"\n[{get_timestamp()}] ========================================")
print(f"[{get_timestamp()}]         测试套件完成")
print(f"[{get_timestamp()}] ========================================")
