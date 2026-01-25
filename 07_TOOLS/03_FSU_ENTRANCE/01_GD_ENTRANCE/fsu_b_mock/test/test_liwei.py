#!/usr/bin/env python3
# Test client for Liwei protocol

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


def to_bcd(value: int) -> int:
    """
    将十进制数转换为BCD码
    Args:
        value: 十进制数（0-99）
    Returns:
        BCD码
    """
    return ((value // 10) << 4) | (value % 10)


def calculate_liwei_checksum(data: bytes) -> int:
    """
    计算力维协议的校验和（求和校验）
    Args:
        data: 需要计算校验和的数据（不包含校验和字段本身）
    Returns:
        校验和（2字节）
    """
    checksum = 0
    for byte in data:
        checksum += byte
    return checksum & 0xFFFF


def build_liwei_packet(cid2: int, group: int, type_code: int, data: bytes) -> bytes:
    """
    构建力维协议数据包（完全按照力维类方式编码）
    格式：7E + ASCII编码的hex字符串 + 0D
    中间的ASCII编码的hex字符串包括：ver + adr + cid1 + cid2 + length + group + type + data + checksum
    
    力维协议编码规则：
    1. SOI（起始符）和EOI（结束符）按单字节直接发送
    2. 其余字段按字节拆分为高4位、低4位，以ASCII码形式发送（先高后低）
    3. 校验和计算基于ASCII编码后的字节值
    4. 十六进制字符使用大写
    
    Args:
        cid2: 命令ID2
        group: 功能组
        type_code: 功能类型
        data: 数据
    Returns:
        完整数据包
    """
    # 构建中间数据部分（二进制）
    binary_data = bytearray()
    binary_data.append(0x10)  # 版本
    binary_data.append(0x01)  # 地址
    binary_data.append(0x80)  # 命令ID1
    binary_data.append(cid2)   # 命令ID2
    
    # 构建数据帧部分
    data_frame = bytearray()
    data_frame.append(group)  # 功能组
    data_frame.append(type_code)  # 功能类型
    data_frame.extend(data)  # 数据
    
    # 计算L.TH（参数长度校验 + 长度标示码）
    # 数据信息部分字节长度为L，ASCII码个数LENID=2L
    L = len(data_frame)  # INFO部分字节长度
    LENID = 2 * L  # ASCII码个数
    
    # 将LENID按4位分组，4组4位数累加后模16取补，作为LCHKSUM（高4位）
    lenid_bytes = LENID.to_bytes(2, byteorder='big')  # 转换为2字节大端
    
    # 拆分每组4位数
    group1 = (lenid_bytes[0] >> 4) & 0x0F  # 第一组（最高4位）
    group2 = lenid_bytes[0] & 0x0F         # 第二组
    group3 = (lenid_bytes[1] >> 4) & 0x0F  # 第三组
    group4 = lenid_bytes[1] & 0x0F         # 第四组（最低4位）
    
    # 4组4位数累加后模16取补
    sum_groups = group1 + group2 + group3 + group4
    lchksum = (16 - (sum_groups % 16)) % 16
    
    # 构建L.TH：高字节为lchksum，低字节为LENID的低字节
    l_th = bytes([((lchksum << 4) | (LENID >> 8)) & 0xFF, LENID & 0xFF])
    binary_data.extend(l_th)
    
    # 添加数据帧
    binary_data.extend(data_frame)
    
    # 计算CHK-SUM（帧校验）
    # 从VER到INFO最后字节，按发送的ASCII码累加求和（双字节），模65536后取补运算
    # 1. 将二进制数据转换为ASCII编码的十六进制字符串（大写）
    ascii_hex = binary_data.hex().upper()
    
    # 2. 计算ASCII码累加和
    chk_sum = 0
    for c in ascii_hex:
        chk_sum += ord(c)
    
    # 3. 模65536后取补运算
    chk_sum = (~chk_sum + 1) & 0xFFFF
    
    # 4. 将校验和转换为二进制
    chk_sum_bytes = chk_sum.to_bytes(2, byteorder='big')
    
    # 5. 添加校验和到二进制数据
    binary_data.extend(chk_sum_bytes)
    
    # 6. 构建完整数据包：7E + ASCII编码的hex字符串（大写） + 0D
    ascii_hex_full = binary_data.hex().upper().encode('ascii')
    packet = bytes([0x7E]) + ascii_hex_full + bytes([0x0D])
    
    return bytes(packet)


def parse_liwei_response(data: bytes) -> dict:
    """
    解析力维协议应答数据
    支持两种格式：
    1. ASCII编码的十六进制字符串：7E + ASCII_HEX + 0D
    2. 二进制格式：直接二进制数据
    
    Args:
        data: 力维协议数据包
    Returns:
        解析后的字段字典
    """
    binary_data = data
    
    # 检查是否为ASCII编码的十六进制字符串格式
    if len(data) >= 2 and data[0] == 0x7E and data[-1] == 0x0D:
        try:
            # 提取中间的ASCII十六进制字符串部分
            ascii_hex = data[1:-1].decode('ascii')
            # 转换为二进制数据
            binary_data = bytes.fromhex(ascii_hex)
        except:
            # 如果转换失败，使用原始数据
            pass
    
    # 检查二进制数据长度
    if len(binary_data) < 10:
        return {'error': f'二进制数据长度不足，需要至少10字节，实际{len(binary_data)}字节'}
    
    # 解析二进制数据
    version = binary_data[0]
    address = binary_data[1]
    cid1 = binary_data[2]
    cid2 = binary_data[3]
    
    # 对于二进制格式，不需要检查包头包尾
    
    # 数据帧部分（从第4字节开始，跳过版本、地址、CID1、CID2）
    data_frame = binary_data[4:]
    
    # 解析响应数据
    result = {
        'version': f'0x{version:02X}',
        'address': f'0x{address:02X}',
        'cid1': f'0x{cid1:02X}',
        'cid2': f'0x{cid2:02X}',
        'raw_binary': binary_data.hex()
    }
    
    # 根据数据帧长度解析具体字段
    if len(data_frame) >= 8:
        # 解析日期时间响应
        result['year'] = f'0x{data_frame[0]:02X}{data_frame[1]:02X}'
        result['month'] = f'0x{data_frame[2]:02X}'
        result['day'] = f'0x{data_frame[3]:02X}'
        result['week'] = f'0x{data_frame[4]:02X}'
        result['hour'] = f'0x{data_frame[5]:02X}'
        result['minute'] = f'0x{data_frame[6]:02X}'
        result['second'] = f'0x{data_frame[7]:02X}'
    
    return result


def send_udp_test(cid2: int, group: int, type_code: int, test_data: bytes, description: str):
    """发送UDP测试请求（使用B接口协议）"""
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: UDP")
    print(f"[{get_timestamp()}] CID2: 0x{cid2:02X}")
    print(f"[{get_timestamp()}] 功能组: 0x{group:02X}")
    print(f"[{get_timestamp()}] 功能类型: 0x{type_code:02X}")
    print(f"[{get_timestamp()}] 测试数据: {test_data.hex()}")
    
    # 构建力维协议数据包
    liwei_packet = build_liwei_packet(cid2, group, type_code, test_data)
    print(f"[{get_timestamp()}] 力维数据包: {liwei_packet.hex()}")
    print(f"[{get_timestamp()}] 力维数据包长度: {len(liwei_packet)} 字节")
    
    # 使用B接口编码
    packet = codec.encode(
        liwei_packet,
        p_dest_addr,
        p_src_addr,
        p_subDevType,
        p_subDev_addr
    )
    
    print(f"[{get_timestamp()}] B接口数据包长度: {len(packet)} 字节")
    print(f"[{get_timestamp()}] B接口数据包: {packet.hex()}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        print(f"[{get_timestamp()}] 发送数据包到 {SERVER_IP}:{UDP_PORT}...")
        sock.sendto(packet, (SERVER_IP, UDP_PORT))
        
        sock.settimeout(5)
        try:
            response, addr = sock.recvfrom(1024)
            print(f"[{get_timestamp()}] 从 {addr} 收到响应: {response.hex()}")
            print(f"[{get_timestamp()}] 响应长度: {len(response)} 字节")
            
            try:
                through_data, decoded_response = codec.decode(response)
                print(f"[{get_timestamp()}] --- B接口响应 ---\n[{get_timestamp()}] P_header: {decoded_response.get('P_header', 'N/A')}")
                print(f"[{get_timestamp()}] P_dest_addr: {decoded_response.get('P_dest_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_src_addr: {decoded_response.get('P_src_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_subDevType: {decoded_response.get('P_subDevType', 'N/A')}")
                print(f"[{get_timestamp()}] P_subDev_addr: {decoded_response.get('P_subDev_addr', 'N/A')}")
                print(f"[{get_timestamp()}] P_pLen: {decoded_response.get('P_pLen', 'N/A')}")
                print(f"[{get_timestamp()}] RtnFlag: {decoded_response.get('RtnFlag', 'N/A')}")
                print(f"[{get_timestamp()}] CommType: {decoded_response.get('CommType', 'N/A')}")
                print(f"[{get_timestamp()}] 透传数据长度: {decoded_response.get('through_data_len', 'N/A')}")
                print(f"[{get_timestamp()}] 透传数据: {through_data.hex()}")
                
                liwei_resp = parse_liwei_response(through_data)
                if 'error' in liwei_resp:
                    print(f"[{get_timestamp()}] 力维解析错误: {liwei_resp['error']}")
                else:
                    print(f"[{get_timestamp()}] --- 力维协议响应 ---\n[{get_timestamp()}] 版本: {liwei_resp.get('version', 'N/A')}")
                    print(f"[{get_timestamp()}] adr: {liwei_resp.get('address', 'N/A')}")
                    print(f"[{get_timestamp()}] CID1: {liwei_resp.get('cid1', 'N/A')}")
                    print(f"[{get_timestamp()}] CID2: {liwei_resp.get('cid2', 'N/A')}")
                    print(f"[{get_timestamp()}] group: {liwei_resp.get('group', 'N/A')}")
                    print(f"[{get_timestamp()}] type: {liwei_resp.get('type_code', 'N/A')}")
                    print(f"[{get_timestamp()}] checksun: {liwei_resp.get('checksum', 'N/A')} (有效: {liwei_resp.get('checksum_valid', False)})")
                    print(f"[{get_timestamp()}] 负载: {liwei_resp.get('payload', 'N/A')}")
                
            except Exception as e:
                print(f"[{get_timestamp()}] 解码错误: {str(e)}")
                
        except socket.timeout:
            print(f"[{get_timestamp()}] 超时未收到响应")
        except Exception as e:
            print(f"[{get_timestamp()}] 接收响应错误: {str(e)}")


def send_tcp_test(cid2: int, group: int, type_code: int, test_data: bytes, description: str):
    """发送TCP测试请求（直接透传，不需要B接口协议）"""
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: TCP")
    print(f"[{get_timestamp()}] CID2: 0x{cid2:02X}")
    print(f"[{get_timestamp()}] 功能组: 0x{group:02X}")
    print(f"[{get_timestamp()}] 功能类型: 0x{type_code:02X}")
    print(f"[{get_timestamp()}] 测试数据: {test_data.hex()}")
    
    # 构建力维协议数据包
    liwei_packet = build_liwei_packet(cid2, group, type_code, test_data)
    print(f"[{get_timestamp()}] 力维数据包: {liwei_packet.hex()}")
    print(f"[{get_timestamp()}] 力维数据包长度: {len(liwei_packet)} 字节")
    
    # TCP协议包直接通过fsu端口透传到设备，不需要经过B接口外层协议编码
    packet = liwei_packet
    
    print(f"[{get_timestamp()}] TCP数据包长度: {len(packet)} 字节")
    print(f"[{get_timestamp()}] TCP数据包: {packet.hex()}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"[{get_timestamp()}] 连接到 {SERVER_IP}:{TCP_PORT}...")
        try:
            sock.connect((SERVER_IP, TCP_PORT))
            print(f"[{get_timestamp()}] 连接成功")
            
            print(f"[{get_timestamp()}] 发送数据...")
            sock.sendall(packet)
            
            sock.settimeout(5)
            try:
                response = sock.recv(1024)
                print(f"[{get_timestamp()}] 收到响应: {response.hex()}")
                print(f"[{get_timestamp()}] 响应长度: {len(response)} 字节")
                
                try:
                    # TCP响应也不会经过B接口编码，直接解析透传数据
                    liwei_resp = parse_liwei_response(response)
                    if 'error' in liwei_resp:
                        print(f"[{get_timestamp()}] 力维解析错误: {liwei_resp['error']}")
                    else:
                        print(f"[{get_timestamp()}] --- 力维协议响应 ---\n[{get_timestamp()}] 版本: {liwei_resp.get('version', 'N/A')}")
                        print(f"[{get_timestamp()}] 地址: {liwei_resp.get('address', 'N/A')}")
                        print(f"[{get_timestamp()}] CID1: {liwei_resp.get('cid1', 'N/A')}")
                        print(f"[{get_timestamp()}] CID2: {liwei_resp.get('cid2', 'N/A')}")
                        print(f"[{get_timestamp()}] 功能组: {liwei_resp.get('group', 'N/A')}")
                        print(f"[{get_timestamp()}] 功能类型: {liwei_resp.get('type_code', 'N/A')}")
                        print(f"[{get_timestamp()}] 校验和: {liwei_resp.get('checksum', 'N/A')} (有效: {liwei_resp.get('checksum_valid', False)})")
                        print(f"[{get_timestamp()}] 负载: {liwei_resp.get('payload', 'N/A')}")
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


def build_password_check_data() -> bytes:
    """
    构建获取权限（密码校验）测试数据
    """
    data = bytearray()
    # 5字节密码，这里使用0x0000000000作为测试数据
    data.extend(b'\x00\x00\x00\x00\x00')
    
    return bytes(data)


def build_cancel_permission_data() -> bytes:
    """
    构建取消权限测试数据
    """
    # 取消权限不需要额外数据
    return b''


def build_modify_password_data() -> bytes:
    """
    构建修改密码测试数据
    """
    data = bytearray()
    # 5字节新密码
    data.extend(b'\x12\x34\x56\x78\x90')
    # 1字节校验码
    data.append(0xAA)
    
    return bytes(data)


def build_set_sys_params_data() -> bytes:
    """
    构建设置系统参数测试数据
    """
    data = bytearray()
    # 25字节系统参数，这里使用全0作为测试数据
    data.extend(b'\x00' * 25)
    
    return bytes(data)


def build_calibrate_datetime_data() -> bytes:
    """
    构建校准日期时间测试数据
    格式：年（2字节BCD）、月（1字节BCD）、日（1字节BCD）、星期（1字节BCD）、时（1字节BCD）、分（1字节BCD）、秒（1字节BCD），共8字节
    """
    now = datetime.now()
    data = bytearray()
    
    # 年（2字节BCD）：2000-2099
    year = now.year - 2000  # 取后两位
    data.append(to_bcd(year))  # 年（高位）
    data.append(0x00)  # 年（低位） - 力维协议使用2字节年份，高位为实际年份后两位的BCD码，低位为00
    
    # 月（1字节BCD）
    data.append(to_bcd(now.month))
    
    # 日（1字节BCD）
    data.append(to_bcd(now.day))
    
    # 星期（1字节BCD）：1-7（7代表星期日）
    weekday = now.isoweekday()  # 1-7（1代表星期一，7代表星期日）
    data.append(to_bcd(weekday))
    
    # 时（1字节BCD）
    data.append(to_bcd(now.hour))
    
    # 分（1字节BCD）
    data.append(to_bcd(now.minute))
    
    # 秒（1字节BCD）
    data.append(to_bcd(now.second))
    
    return bytes(data)

# 初始化B接口编解码器
codec = BInterfaceCodec()

# 配置参数
SERVER_IP = 'localhost'
UDP_PORT = 10107  # UDP端口
TCP_PORT = 10125  # TCP端口
fsuid = '313234313233313331323431'  # FSU ID，与mock server配置中的fsuid匹配

p_dest_addr = bytes.fromhex(fsuid).ljust(20, b'\x00')
p_src_addr = b'\x00\x00\x00\x00\x00\x00\x00\x00'
p_subDevType = 1
p_subDev_addr = 1

# 主测试流程
print(f"[{get_timestamp()}] ========================================")
print(f"[{get_timestamp()}]         Liwei Protocol Test Suite")
print(f"[{get_timestamp()}] ========================================")

# 测试1：获取权限（密码校验）
# test_password_check_data = build_password_check_data()
# send_udp_test(0x48, 0xF0, 0xE0, test_password_check_data, "Test 1: Get Permission (Password Check) - UDP")
# send_tcp_test(0x48, 0xF0, 0xE0, test_password_check_data, "Test 2: Get Permission (Password Check) - TCP")

# 测试3：取消权限
# test_cancel_permission_data = build_cancel_permission_data()
# send_udp_test(0x48, 0xF0, 0xE1, test_cancel_permission_data, "Test 3: Cancel Permission - UDP")
# send_tcp_test(0x48, 0xF0, 0xE1, test_cancel_permission_data, "Test 4: Cancel Permission - TCP")

# 测试5：修改密码
# test_modify_password_data = build_modify_password_data()
# send_udp_test(0x48, 0xF0, 0xE2, test_modify_password_data, "Test 5: Modify Password - UDP")
# # send_tcp_test(0x48, 0xF0, 0xE2, test_modify_password_data, "Test 6: Modify Password - TCP")

# 测试7：校准日期时间
# 根据Liwei协议文档，设置日期时间的COMMAND TYPE是0XE0
# CID2=49H（设置命令），COMMAND GROUP=F1，COMMAND TYPE=E0
# print(f"[{get_timestamp()}] 使用正确的参数调用校准日期时间测试")
# test_calibrate_datetime_data = build_calibrate_datetime_data()
# send_udp_test(0x49, 0xF1, 0xE0, test_calibrate_datetime_data, "Test 7: Calibrate Date Time - UDP")
# send_tcp_test(0x49, 0xF1, 0xE0, test_calibrate_datetime_data, "Test 8: Calibrate Date Time - TCP")

# # 测试9：读取SM的实时钟
# test_read_sys_params_data = b'\x00'  # 读取不需要额外数据，使用字节值0x00
# send_udp_test(0x4A, 0xF2, 0xE0, test_read_sys_params_data, "Test 9: Read System Parameters - UDP")
# send_tcp_test(0x4A, 0xF2, 0xE0, test_read_sys_params_data, "Test 10: Read System Parameters - TCP")

# 测试11：4AF2E5功能测试
test_4af2e5_data = b'\x00'  # 4AF2E5测试数据，使用字节值0x00
send_udp_test(0x4A, 0xF2, 0xE5, test_4af2e5_data, "测试11: 4AF2E5功能测试 - UDP")
send_tcp_test(0x4A, 0xF2, 0xE5, test_4af2e5_data, "测试12: 4AF2E5功能测试 - TCP")

# # 测试11：心跳包测试
# send_heartbeat_test("Test 11: Send Heartbeat - UDP")

print(f"\n[{get_timestamp()}] ========================================")
print(f"[{get_timestamp()}]         Test Suite Complete")
print(f"[{get_timestamp()}] ========================================")
