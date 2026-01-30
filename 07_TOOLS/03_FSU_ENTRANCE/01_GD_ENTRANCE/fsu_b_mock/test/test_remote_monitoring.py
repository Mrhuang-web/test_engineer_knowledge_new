#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试远程监控功能
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codec.through_data_codec import ThroughDataCodec


def test_remote_monitoring_e7():
    """测试远程监控(0XE7)功能"""
    print("=" * 60)
    print("测试远程监控(0XE7)功能")
    print("=" * 60)
    
    # 加载力维协议配置
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "liwei", "liwei.json")
    with open(config_path, "r", encoding="utf-8") as f:
        protocol_config = json.load(f)
    
    # 创建编解码器
    codec = ThroughDataCodec(protocol_config)
    
    # 模拟远程监控(0XE7)请求
    parsed_data = {
        "through_pdu": {
            "cid2": "4A"
        }
    }
    
    # 构建响应数据
    response_data = {
        "group": "F2",
        "type": "E7",
        "dataf": "00"
    }
    
    # 编码响应
    encoded_data = codec.encode(parsed_data, response_data)
    
    print(f"编码结果: {encoded_data.hex().upper()}")
    print(f"响应长度: {len(encoded_data)}")
    
    # 验证响应数据
    # 力维协议格式：7E + 版本 + 地址 + cid1 + cid2 + 长度 + 数据 + 校验和 + 0D
    if len(encoded_data) > 10:
        # 提取数据部分
        data_part = encoded_data[6:-3]  # 跳过7E + 版本 + 地址 + cid1 + cid2 + 长度，跳过校验和 + 0D
        print(f"数据部分: {data_part.hex().upper()}")
        
        # 验证数据长度
        if len(data_part) >= 3:
            # cid2 (1字节) + 工作状态 (1字节) + 线路状态 (1字节)
            cid2 = data_part[0]
            work_status = data_part[1]
            line_status = data_part[2]
            
            print(f"CID2: 0x{cid2:02X}")
            print(f"工作状态: 0x{work_status:02X}")
            print(f"线路状态: 0x{line_status:02X}")
            
            # 验证工作状态
            print("\n工作状态解析:")
            print(f"  D7 (实时钟IC): {'正常' if (work_status & 0x80) == 0 else '不正常'}")
            print(f"  D6 (存储器): {'正常' if (work_status & 0x40) == 0 else '不正常'}")
            print(f"  D5 (工作电源): {'正常' if (work_status & 0x20) == 0 else '不正常'}")
            print(f"  D3 (红外监控): {'不监视' if (work_status & 0x08) == 0 else '监视'}")
            print(f"  D2 (门开关监控): {'不监视' if (work_status & 0x04) == 0 else '监视'}")
            print(f"  D1 (门控电磁继电器): {'关闭' if (work_status & 0x02) == 0 else '加电驱动'}")
            print(f"  D0 (工作状态): {'正常' if (work_status & 0x01) == 0 else '报警状态'}")
            
            # 验证线路状态
            print("\n线路状态解析:")
            print(f"  D7 (紧急驱动输入): {'正常' if (line_status & 0x80) == 0 else '触发'}")
            print(f"  D6 (联动输入2): {'正常' if (line_status & 0x40) == 0 else '触发'}")
            print(f"  D5 (联动输入1): {'正常' if (line_status & 0x20) == 0 else '触发'}")
            print(f"  D4 (联动输出继电器): {'关闭' if (line_status & 0x10) == 0 else '加电驱动'}")
            print(f"  D3 (门状态): {'关闭' if (line_status & 0x08) == 0 else '开启'}")
            print(f"  D2 (红外输入): {'正常' if (line_status & 0x04) == 0 else '报警'}")
            print(f"  D1 (手动开门键): {'松开' if (line_status & 0x02) == 0 else '按下'}")
            print(f"  D0 (门控电磁继电器): {'关闭' if (line_status & 0x01) == 0 else '加电驱动'}")
        else:
            print("数据长度不足，无法解析")
    else:
        print("响应长度不足，无法解析")


def test_remote_monitoring_ed():
    """测试远程监控(0XED)功能"""
    print("\n" + "=" * 60)
    print("测试远程监控(0XED)功能")
    print("=" * 60)
    
    # 加载力维协议配置
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "liwei", "liwei.json")
    with open(config_path, "r", encoding="utf-8") as f:
        protocol_config = json.load(f)
    
    # 创建编解码器
    codec = ThroughDataCodec(protocol_config)
    
    # 模拟远程监控(0XED)请求
    parsed_data = {
        "through_pdu": {
            "cid2": "49"
        }
    }
    
    # 构建响应数据
    response_data = {
        "group": "F1",
        "type": "ED",
        "dataf": "00",
        "savep": 10,
        "loadp": 5,
        "mf": 0x81
    }
    
    # 编码响应
    encoded_data = codec.encode(parsed_data, response_data)
    
    print(f"编码结果: {encoded_data.hex().upper()}")
    print(f"响应长度: {len(encoded_data)}")
    
    # 验证响应数据
    if len(encoded_data) > 10:
        # 提取数据部分
        data_part = encoded_data[6:-3]  # 跳过7E + 版本 + 地址 + cid1 + cid2 + 长度，跳过校验和 + 0D
        print(f"数据部分: {data_part.hex().upper()}")
        
        # 验证数据长度
        if len(data_part) >= 8:
            # cid2 (1字节) + 控制状态 (1字节) + 感应头状态 (1字节) + SAVEP (2字节) + LOADP (2字节) + MF (1字节)
            cid2 = data_part[0]
            control_status = data_part[1]
            sensor_status = data_part[2]
            savep = (data_part[3] << 8) | data_part[4]
            loadp = (data_part[5] << 8) | data_part[6]
            mf = data_part[7]
            
            print(f"CID2: 0x{cid2:02X}")
            print(f"控制状态: 0x{control_status:02X}")
            print(f"感应头状态: 0x{sensor_status:02X}")
            print(f"SAVEP: {savep}")
            print(f"LOADP: {loadp}")
            print(f"MF: 0x{mf:02X}")
            
            # 验证控制状态
            print("\n控制状态解析:")
            print(f"  D7 (门常开): {'无效' if (control_status & 0x80) == 0 else '有效'}")
            print(f"  D6 (门常闭): {'无效' if (control_status & 0x40) == 0 else '有效'}")
            print(f"  D5 (第2继电器): {'未动作' if (control_status & 0x20) == 0 else '动作'}")
            print(f"  D4 (紧急输入): {'无效' if (control_status & 0x10) == 0 else '有效'}")
            print(f"  D3 (门磁监控): {'不监控' if (control_status & 0x08) == 0 else '监控'}")
            print(f"  D2 (红外监控): {'不监控' if (control_status & 0x04) == 0 else '监控'}")
            print(f"  D1 (门控继电器): {'未动作' if (control_status & 0x02) == 0 else '动作'}")
            print(f"  D0 (报警输出): {'无' if (control_status & 0x01) == 0 else '有'}")
        else:
            print("数据长度不足，无法解析")
    else:
        print("响应长度不足，无法解析")

if __name__ == "__main__":
    test_remote_monitoring_e7()
    test_remote_monitoring_ed()
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
