#!/usr/bin/env python3
import os
import sys
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
import struct
import binascii
import datetime
from codec.b_interface_codec import BInterfaceCodec

# 获取时间戳
def get_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

# CRC16计算函数
def calculate_crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

# 盈佳协议包构造
def yingjia_construct_packet(cid2, group, type_code, data=b''):
    # SOI - 帧起始符
    soi = b'\xFA\x55\xFA\x55\xFA\x55'
    
    # VER - 协议版本
    ver = b'\x10'
    
    # ADR - 地址
    adr = b'\xFD'
    
    # CID1 - 命令标识1
    cid1 = b'\x88'
    
    # CID2 - 命令标识2
    cid2 = bytes([cid2])
    
    # LENGTH - 长度（包括GROUP, TYPE, DATA, CRC16）
    length = struct.pack('!H', len(data) + 4)  # GROUP(1) + TYPE(1) + DATA + CRC16(2)
    
    # GROUP - 分组
    group = bytes([group])
    
    # TYPE - 类型
    type_code = bytes([type_code])
    
    # 计算CRC16
    crc_data = cid2 + length + group + type_code + data
    crc16 = calculate_crc16(crc_data)
    crc_bytes = struct.pack('!H', crc16)
    
    # EOI - 帧结束符
    eoi = b'\xFE'
    
    # 构造完整盈佳协议包
    packet = soi + ver + adr + cid1 + cid2 + length + group + type_code + data + crc_bytes + eoi
    
    return packet

# 盈佳协议解析
def yingjia_parse_packet(packet):
    if len(packet) < 18:  # 盈佳协议数据包最小长度
        return {"error": f"数据包长度不足，期望至少18字节，实际{len(packet)}字节"}
    
    try:
        # 提取各个字段
        soi = packet[0:6]
        ver = packet[6:7]
        adr = packet[7:8]
        cid1 = packet[8:9]
        cid2 = packet[9:10]
        length = struct.unpack('!H', packet[10:12])[0]
        group = packet[12:13]
        type_code = packet[13:14]
        data = packet[14:-3]  # 排除CRC16和EOI
        crc16 = packet[-3:-1]
        eoi = packet[-1:]
        
        # 验证CRC16
        crc_data = cid2 + packet[10:12] + group + type_code + data
        calculated_crc = calculate_crc16(crc_data)
        if calculated_crc != struct.unpack('!H', crc16)[0]:
            return {
                "error": f"CRC校验失败",
                "calculated_crc": f"0x{calculated_crc:04X}",
                "actual_crc": f"0x{struct.unpack('!H', crc16)[0]:04X}"
            }
        
        return {
            "soi": f"0x{soi.hex()}",
            "ver": f"0x{ver.hex()}",
            "adr": f"0x{adr.hex()}",
            "cid1": f"0x{cid1.hex()}",
            "cid2": f"0x{cid2.hex()}",
            "length": length,
            "group": f"0x{group.hex()}",
            "type": f"0x{type_code.hex()}",
            "data": f"0x{data.hex()}",
            "crc16": f"0x{crc16.hex()}",
            "eoi": f"0x{eoi.hex()}",
            "crc_valid": True
        }
    except Exception as e:
        return {"error": f"解析失败: {str(e)}"}

# 发送UDP测试请求

def send_udp_test(cid2, group, type_code, data=b'', description="测试"):
    """发送UDP测试请求（使用B接口协议）"""
    # 配置参数
    SERVER_IP = '127.0.0.1'
    UDP_PORT = 10105
    
    # B接口参数
    p_dest_addr = b'12345678'.ljust(8, b'\x00')
    p_src_addr = b'30000000000000000000000000000000'.ljust(20, b'\x00')
    p_subDevType = 1
    p_subDev_addr = 0
    
    # 创建B接口编解码器
    codec = BInterfaceCodec()
    
    print(f"\n[{get_timestamp()}] === {description} ===")
    print(f"[{get_timestamp()}] 协议类型: UDP")
    print(f"[{get_timestamp()}] 服务器: {SERVER_IP}:{UDP_PORT}")
    print(f"[{get_timestamp()}] CID2: 0x{cid2:02X}, 组: 0x{group:02X}, 类型: 0x{type_code:02X}")
    
    # 构建盈佳协议包
    yingjia_packet = yingjia_construct_packet(cid2, group, type_code, data)
    print(f"[{get_timestamp()}] 盈佳数据包: 0x{yingjia_packet.hex()}")
    
    # B接口封装
    packet = codec.encode(
        yingjia_packet,
        p_dest_addr,
        p_src_addr,
        p_subDevType,
        p_subDev_addr,
        comm_type=0x0001,
        rtn_flag=0xED
    )
    
    print(f"[{get_timestamp()}] B接口数据包长度: {len(packet)} 字节")
    print(f"[{get_timestamp()}] B接口数据包: 0x{packet.hex()}")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            print(f"[{get_timestamp()}] 发送数据包...")
            sock.sendto(packet, (SERVER_IP, UDP_PORT))
            
            sock.settimeout(5)
            try:
                response, addr = sock.recvfrom(1024)
                print(f"[{get_timestamp()}] 从 {addr} 收到响应: 0x{response.hex()}")
                print(f"[{get_timestamp()}] 响应长度: {len(response)} 字节")
                
                try:
                    # 解析B接口响应
                    through_data, decoded_response = codec.decode(response)
                    print(f"[{get_timestamp()}] --- B接口响应 ---" )
                    print(f"[{get_timestamp()}] P_header: {decoded_response.get('P_header', 'N/A')}")
                    print(f"[{get_timestamp()}] P_dest_addr: {decoded_response.get('P_dest_addr', 'N/A')}")
                    print(f"[{get_timestamp()}] P_src_addr: {decoded_response.get('P_src_addr', 'N/A')}")
                    print(f"[{get_timestamp()}] P_subDevType: {decoded_response.get('P_subDevType', 'N/A')}")
                    print(f"[{get_timestamp()}] P_subDev_addr: {decoded_response.get('P_subDev_addr', 'N/A')}")
                    print(f"[{get_timestamp()}] P_pLen: {decoded_response.get('P_pLen', 'N/A')}")
                    print(f"[{get_timestamp()}] RtnFlag: {decoded_response.get('RtnFlag', 'N/A')}")
                    print(f"[{get_timestamp()}] CommType: {decoded_response.get('CommType', 'N/A')}")
                    print(f"[{get_timestamp()}] through_data_len: {decoded_response.get('through_data_len', 'N/A')}")
                    print(f"[{get_timestamp()}] 透传数据: 0x{through_data.hex()}")
                    
                    # 解析盈佳协议响应
                    yingjia_resp = yingjia_parse_packet(through_data)
                    if 'error' in yingjia_resp:
                        print(f"[{get_timestamp()}] 盈佳解析错误: {yingjia_resp['error']}")
                        if 'calculated_crc' in yingjia_resp:
                            print(f"[{get_timestamp()}] 计算CRC: {yingjia_resp['calculated_crc']}")
                            print(f"[{get_timestamp()}] 实际CRC: {yingjia_resp['actual_crc']}")
                    else:
                        print(f"[{get_timestamp()}] --- 盈佳协议响应 ---" )
                        print(f"[{get_timestamp()}] SOI: {yingjia_resp.get('soi', 'N/A')}")
                        print(f"[{get_timestamp()}] VER: {yingjia_resp.get('ver', 'N/A')}")
                        print(f"[{get_timestamp()}] ADR: {yingjia_resp.get('adr', 'N/A')}")
                        print(f"[{get_timestamp()}] CID1: {yingjia_resp.get('cid1', 'N/A')}")
                        print(f"[{get_timestamp()}] CID2: {yingjia_resp.get('cid2', 'N/A')}")
                        print(f"[{get_timestamp()}] 长度: {yingjia_resp.get('length', 'N/A')}")
                        print(f"[{get_timestamp()}] 组: {yingjia_resp.get('group', 'N/A')}")
                        print(f"[{get_timestamp()}] 类型: {yingjia_resp.get('type', 'N/A')}")
                        print(f"[{get_timestamp()}] 数据: {yingjia_resp.get('data', 'N/A')}")
                        print(f"[{get_timestamp()}] CRC16: {yingjia_resp.get('crc16', 'N/A')} (有效: {yingjia_resp.get('crc_valid', False)})")
                        print(f"[{get_timestamp()}] EOI: {yingjia_resp.get('eoi', 'N/A')}")
                except Exception as e:
                    print(f"[{get_timestamp()}] 解码错误: {str(e)}")
                    import traceback
                    traceback.print_exc()
            except socket.timeout:
                print(f"[{get_timestamp()}] 超时未收到响应")
            except Exception as e:
                print(f"[{get_timestamp()}] 接收响应错误: {str(e)}")
                import traceback
                traceback.print_exc()
    except Exception as e:
        print(f"[{get_timestamp()}] 发送数据包错误: {str(e)}")
        import traceback
        traceback.print_exc()

# 主测试函数
def main():
    print(f"[{get_timestamp()}] ========================================")
    print(f"[{get_timestamp()}]         盈佳协议测试套件")
    print(f"[{get_timestamp()}] ========================================")
    
    # 测试取消权限命令（CID2=48H, GROUP=F0H, TYPE=E1H）
    send_udp_test(
        cid2=0x48, 
        group=0xF0, 
        type_code=0xE1, 
        data=b'',
        description="测试取消权限命令"
    )
    
    # 测试获取权限命令（CID2=48H, GROUP=F0H, TYPE=E0H）
    # send_udp_test(
    #     cid2=0x48, 
    #     group=0xF0, 
    #     type_code=0xE0, 
    #     data=b'\x00\x00\x00\x00\x00',
    #     description="测试获取权限命令"
    # )
    
    print(f"\n[{get_timestamp()}] ========================================")
    print(f"[{get_timestamp()}]         测试套件完成")
    print(f"[{get_timestamp()}] ========================================")

if __name__ == "__main__":
    main()
