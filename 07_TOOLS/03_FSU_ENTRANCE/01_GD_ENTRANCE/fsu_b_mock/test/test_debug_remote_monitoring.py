#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细调试远程监控(0XE7)功能
"""

import json
import os
import sys
import logging
from event.event_manager import EventManager
from codec.b_interface_codec import BInterfaceCodec

# 设置日志级别为DEBUG
logging.basicConfig(level=logging.DEBUG)

class MockDeviceConfig:
    """模拟设备配置类"""
    
    def get_device_list(self):
        """获取设备列表"""
        return [{
            "event_polling_enable": True,
            "event_polling_interval": 5,
            "event_mode": "single"
        }]

class MockLogger:
    """模拟日志类"""
    
    def debug(self, msg):
        """调试日志"""
        print(f"[DEBUG] {msg}")
    
    def info(self, msg):
        """信息日志"""
        print(f"[INFO] {msg}")
    
    def warning(self, msg):
        """警告日志"""
        print(f"[WARNING] {msg}")
    
    def error(self, msg):
        """错误日志"""
        print(f"[ERROR] {msg}")

class MockTransport:
    """模拟传输类"""
    
    def sendto(self, data, addr):
        """发送数据"""
        print(f"[SEND] 发送数据到 {addr}: {data.hex().upper()}")

def test_debug_remote_monitoring():
    """详细调试远程监控(0XE7)功能"""
    print("开始详细调试远程监控(0XE7)功能...")
    
    # 构建FSU配置
    fsu_config = {
        "fsuname": "TestFSU",
        "fsuid": "1234567890",
        "config_dir": "config"
    }
    
    # 创建模拟设备配置
    device_config = MockDeviceConfig()
    
    # 创建B接口编解码器
    b_interface_codec = BInterfaceCodec()
    
    # 创建模拟日志
    logger = MockLogger()
    
    # 创建事件管理器
    event_manager = EventManager(fsu_config, device_config, b_interface_codec, logger)
    
    # 设置传输
    event_manager.set_transport(MockTransport())
    
    # 设置设备协议模板
    device_protocols = {
        "test_device": {
            "protocol": {
                "name": "liwei",
                "pdu_left": [
                    {"name": "start", "length": 1, "value": "7E"},
                    {"name": "ver", "length": 1, "value": "10"},
                    {"name": "adr", "length": 1, "value": "01"},
                    {"name": "cid1", "length": 1, "value": "80"},
                    {"name": "cid2", "length": 1, "value": "4A"},
                    {"name": "length", "length": 2, "value": "1D"},
                    {"name": "checksum", "length": 2, "value": "0000"},
                    {"name": "end", "length": 1, "value": "0D"}
                ],
                "pdu_tailer": [
                    {"name": "checksum", "length": 2, "value": "0000"},
                    {"name": "end", "length": 1, "value": "0D"}
                ],
                "data_frame": [
                    {
                        "data_frame_type": "4A_F2_E7",
                        "req_data_list": [
                            {"name": "group", "length": 1, "value": "F2"},
                            {"name": "type", "length": 1, "value": "E7"},
                            {"name": "dataf", "length": 1, "value": "00"}
                        ],
                        "resp_data_list": [
                            {"name": "cid2", "length": 1, "value": "4A"}
                        ],
                        "data_frame_length": 3
                    }
                ],
                "dynamic_length": False,
                "total_length": 15,
                "data_frame_type_flag": ["cid2", "group", "type"]
            },
            "vendor": "liwei",
            "vendor_type": "liwei"
        }
    }
    event_manager.set_device_protocols(device_protocols)
    
    # 模拟远程监控事件类型
    remote_monitoring_event = {
        "status": "00",
        "description": "远程监控",
        "type": "E7",
        "group": "F2"
    }
    
    # 模拟地址
    mock_addr = ("127.0.0.1", 8080)
    
    # 模拟协议配置
    protocol_config = device_protocols["test_device"]
    
    # 打印配置信息
    print("\n=== 配置信息 ===")
    print(f"FSU配置: {fsu_config}")
    print(f"协议配置: {protocol_config}")
    print(f"事件类型: {remote_monitoring_event}")
    
    # 检查配置文件路径
    print("\n=== 配置文件检查 ===")
    config_dir = fsu_config.get("config_dir", "./config/bangsun_old")
    liwei_rules_path = os.path.join(config_dir, "liwei", "rules", "default.json")
    print(f"配置文件路径: {liwei_rules_path}")
    print(f"文件是否存在: {os.path.exists(liwei_rules_path)}")
    
    # 读取并显示配置文件内容
    if os.path.exists(liwei_rules_path):
        with open(liwei_rules_path, "r", encoding="utf-8") as f:
            liwei_rules = json.load(f)
            print(f"配置文件中4AF2E7的配置: {liwei_rules.get('4AF2E7', '未找到')}")
    
    # 测试发送远程监控事件
    print("\n=== 测试发送远程监控事件 ===")
    import asyncio
    asyncio.run(event_manager.send_event(remote_monitoring_event, mock_addr))
    
    print("\n详细调试远程监控(0XE7)功能完成！")

if __name__ == "__main__":
    test_debug_remote_monitoring()
