#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析用户提供的下发指令
"""

import sys

def parse_liwei_command(command_hex):
    """解析力维协议指令
    
    Args:
        command_hex: 十六进制格式的指令
    """
    print("=" * 60)
    print("解析力维协议指令")
    print("=" * 60)
    
    # 提取力维协议部分（从7E开始到0D结束）
    command_bytes = bytes.fromhex(command_hex.replace(' ', ''))
    soi_index = command_bytes.find(b'\x7E')
    eoi_index = command_bytes.find(b'\x0D', soi_index)
    
    if soi_index != -1 and eoi_index != -1:
        liwei_command = command_bytes[soi_index:eoi_index+1]
        print(f"力维协议部分: {liwei_command.hex().upper()}")
        
        # 解析力维协议
        parse_liwei_frame(liwei_command)
    else:
        print("未找到力维协议部分")

def parse_liwei_frame(frame):
    """解析力维协议帧
    
    Args:
        frame: 力维协议帧
    """
    print(f"\n力维协议帧长度: {len(frame)}")
    
    # 提取各字段
    soi = frame[0]
    eoi = frame[-1]
    ascii_part = frame[1:-1]
    
    print(f"SOI: 0x{soi:02X}")
    print(f"EOI: 0x{eoi:02X}")
    print(f"ASCII部分: {ascii_part.decode('ascii')}")
    
    # 解析ASCII部分
    # VER (版本): 2个ASCII字符
    ver_ascii = ascii_part[0:2]
    ver = int(ver_ascii.decode('ascii'), 16)
    print(f"VER: 0x{ver:02X} ({ver_ascii.decode('ascii')})")
    
    # ADR (组内地址): 2个ASCII字符
    adr_ascii = ascii_part[2:4]
    adr = int(adr_ascii.decode('ascii'), 16)
    print(f"ADR: 0x{adr:02X} ({adr_ascii.decode('ascii')})")
    
    # CID1 (类码+组地址): 2个ASCII字符
    cid1_ascii = ascii_part[4:6]
    cid1 = int(cid1_ascii.decode('ascii'), 16)
    print(f"CID1: 0x{cid1:02X} ({cid1_ascii.decode('ascii')})")
    
    # CID2 (命令分类码): 2个ASCII字符
    cid2_ascii = ascii_part[6:8]
    cid2 = int(cid2_ascii.decode('ascii'), 16)
    print(f"CID2: 0x{cid2:02X} ({cid2_ascii.decode('ascii')})")
    
    # L.TH (长度+校验): 4个ASCII字符
    lth_ascii = ascii_part[8:12]
    lth = int(lth_ascii.decode('ascii'), 16)
    print(f"L.TH: 0x{lth:04X} ({lth_ascii.decode('ascii')})")
    
    # INFO (参数): 剩余ASCII字符
    info_ascii = ascii_part[12:]
    print(f"INFO长度: {len(info_ascii)} 字符")
    print(f"INFO: {info_ascii.decode('ascii')}")
    
    # 解析INFO部分
    if len(info_ascii) >= 6:
        # 解析group, type, dataf
        group_ascii = info_ascii[0:2]
        type_ascii = info_ascii[2:4]
        dataf_ascii = info_ascii[4:6]
        
        group = group_ascii.decode('ascii')
        type_code = type_ascii.decode('ascii')
        dataf = dataf_ascii.decode('ascii')
        
        print(f"\nINFO解析:")
        print(f"Group: {group}")
        print(f"Type: {type_code}")
        print(f"Dataf: {dataf}")
        
        # 根据group和type判断指令类型
        if group == "F2" and type_code == "E7":
            print("\n指令类型: 远程监控(0XE7)")
            print("功能: 读取控制器工作状态和监控线路状态")
            print("参数: Dataf=00")
        elif group == "F0" and type_code == "E0":
            print("\n指令类型: 获取权限(0XF0E0)")
            print("功能: 密码校验")
        else:
            print(f"\n指令类型: 未知 ({group}{type_code})")

if __name__ == "__main__":
    # 用户提供的指令
    command = "FF 31 32 34 31 32 33 31 33 31 32 34 31 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 1D 00 EE 01 00 18 00 7E 31 30 30 31 38 30 34 41 41 30 30 36 46 32 45 37 30 30 46 43 33 36 0D 97 FE"
    parse_liwei_command(command)
