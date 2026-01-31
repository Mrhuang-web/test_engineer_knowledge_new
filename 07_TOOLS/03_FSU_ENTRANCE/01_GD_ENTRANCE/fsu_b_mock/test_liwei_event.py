#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试力维协议事件数据编码
"""

import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from codec.through_data_codec import ThroughDataCodec

def test_liwei_event_encoding():
    """测试力维协议事件数据编码"""
    print("=== 测试力维协议事件数据编码 ===")
    
    # 加载力维协议配置
    config_path = os.path.join(os.path.dirname(__file__), "config", "liwei", "liwei.json")
    with open(config_path, "r", encoding="utf-8") as f:
        protocol_config = json.load(f)
    
    # 创建编解码器
    codec = ThroughDataCodec(protocol_config)
    
    # 模拟事件数据
    event_data = {
        "event_source": "0303033333",
        "year": "2026",
        "month": "01",
        "day": "31",
        "hour": "13",
        "minute": "48",
        "second": "46",
        "status": "00",
        "remark": "03"
    }
    
    # 构建基础PDU
    base_pdu = {
        "through_pdu": {
            "data_frame_type": "4AF2E2"
        }
    }
    
    # 编码事件数据
    encoded_data = codec.encode(base_pdu, event_data)
    
    if encoded_data:
        print(f"编码结果: {encoded_data.hex().upper()}")
        print(f"响应长度: {len(encoded_data)}")
        
        # 提取数据部分
        if len(encoded_data) > 10:
            # 跳过7E + 版本 + 地址 + cid1 + cid2 + 长度，跳过校验和 + 0D
            data_part = encoded_data[6:-3]
            print(f"数据部分: {data_part.hex().upper()}")
            print(f"数据部分长度: {len(data_part)}")
            
            # 解析数据部分
            if len(data_part) >= 14:
                # 事件来源 (5字节)
                event_source = data_part[0:5]
                print(f"事件来源: {event_source.hex().upper()}")
                
                # 年份 (2字节 BCD)
                year = data_part[5:7]
                print(f"年份: {year.hex().upper()} -> {year[0]:02X} {year[1]:02X}")
                
                # 月份 (1字节 BCD)
                month = data_part[7:8]
                print(f"月份: {month.hex().upper()}")
                
                # 日期 (1字节 BCD)
                day = data_part[8:9]
                print(f"日期: {day.hex().upper()}")
                
                # 小时 (1字节 BCD)
                hour = data_part[9:10]
                print(f"小时: {hour.hex().upper()}")
                
                # 分钟 (1字节 BCD)
                minute = data_part[10:11]
                print(f"分钟: {minute.hex().upper()}")
                
                # 秒 (1字节 BCD)
                second = data_part[11:12]
                print(f"秒: {second.hex().upper()}")
                
                # 状态 (1字节)
                status = data_part[12:13]
                print(f"状态: {status.hex().upper()}")
                
                # 备注 (1字节)
                remark = data_part[13:14]
                print(f"备注: {remark.hex().upper()}")
    else:
        print("编码失败")

if __name__ == "__main__":
    test_liwei_event_encoding()
