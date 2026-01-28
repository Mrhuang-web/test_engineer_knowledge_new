#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件管理模块，负责事件轮询和事件发送
"""

import asyncio
import os
import json
from typing import Dict, Any, List
from codec.b_interface_codec import BInterfaceCodec
from codec.through_data_codec import ThroughDataCodec

class EventManager:
    """事件管理类"""
    
    def __init__(self, fsu_config: Dict[str, Any], device_config: Any, b_interface_codec: BInterfaceCodec, logger):
        """初始化事件管理器
        
        Args:
            fsu_config: FSU配置
            device_config: 设备配置
            b_interface_codec: B接口编解码器
            logger: 日志记录器
        """
        self.fsu_config = fsu_config
        self.device_config = device_config
        self.b_interface_codec = b_interface_codec
        self.logger = logger
        self.transport = None
        self.sc_iot_config = None
        
        # 事件轮询配置
        self.event_polling_enable = False
        self.event_polling_interval = 5  # 默认5秒轮询一次
        self.event_mode = "single"  # 默认模式：单次请求返回一个事件
        
        # 事件类型列表
        self.event_types = []
        
        # 事件指令列表
        self.event_commands = []
        
        # 事件规则配置
        self.event_rules_config = {}
        
        # 当前轮询的事件索引
        self.current_event_index = 0
        
        # 设备协议模板
        self.device_protocols = {}
        
        # 当前协议配置
        self.current_protocol_config = None
        
        # 加载配置
        self._load_config()
    
    def set_transport(self, transport):
        """设置传输对象
        
        Args:
            transport: 传输对象
        """
        self.transport = transport
    
    def set_sc_iot_config(self, sc_iot_config):
        """设置SC IoT中心配置
        
        Args:
            sc_iot_config: SC IoT中心配置
        """
        self.sc_iot_config = sc_iot_config
    
    def set_device_protocols(self, device_protocols):
        """设置设备协议模板
        
        Args:
            device_protocols: 设备协议模板
        """
        self.device_protocols = device_protocols
    
    def _load_config(self):
        """加载事件相关配置"""
        # 从设备配置中读取事件轮询配置
        device_list = self.device_config.get_device_list()
        if device_list:
            # 使用第一个设备的配置
            device_config = device_list[0]
            self.event_polling_enable = device_config.get("event_polling_enable", False)
            self.event_polling_interval = device_config.get("event_polling_interval", 5)
            self.event_mode = device_config.get("event_mode", "single")  # 事件模式：single或batch
        
        # 只有当event_polling_enable为true时，才加载事件配置文件
        if self.event_polling_enable:
            # 从配置文件中读取事件类型
            self.event_types = self._load_event_types()
            
            # 从配置文件中读取事件规则配置
            self.event_rules_config = self._load_event_rules_config()
        else:
            self.logger.debug("事件轮询未启用，跳过加载事件配置文件")
    
    def _load_event_types(self):
        """从配置文件中读取事件类型和事件指令
        
        Returns:
            事件类型列表
        """
        event_types = []
        try:
            # 构建事件类型配置文件路径
            device_list = self.device_config.get_device_list()
            if device_list:
                # 获取配置目录
                config_dir = self.fsu_config.get("config_dir", "./config/bangsun_old")
                event_types_path = os.path.join(config_dir, "event_types.json")
                
                # 读取事件类型配置文件
                if os.path.exists(event_types_path):
                    with open(event_types_path, "r", encoding="utf-8") as f:
                        event_config = json.load(f)
                        event_types = event_config.get("event_types", [])
                        self.event_commands = event_config.get("event_commands", [])
                        self.logger.info(f"从配置文件加载了 {len(event_types)} 个事件类型和 {len(self.event_commands)} 个事件指令")
                else:
                    self.logger.warning(f"事件类型配置文件不存在: {event_types_path}")
        except Exception as e:
            self.logger.error(f"读取事件类型配置文件失败: {e}")
        
        return event_types
    
    def _load_event_rules_config(self):
        """从配置文件中读取事件规则配置
        
        Returns:
            事件规则配置字典
        """
        event_rules_config = {}
        try:
            # 构建事件规则配置文件路径
            device_list = self.device_config.get_device_list()
            if device_list:
                # 获取配置目录
                config_dir = self.fsu_config.get("config_dir", "./config/bangsun_old")
                event_rules_path = os.path.join(config_dir, "rules", "event.json")
                
                # 读取事件规则配置文件
                if os.path.exists(event_rules_path):
                    with open(event_rules_path, "r", encoding="utf-8") as f:
                        event_rules_config = json.load(f)
                        self.logger.info("从配置文件加载了事件规则配置")
                else:
                    self.logger.warning(f"事件规则配置文件不存在: {event_rules_path}")
        except Exception as e:
            self.logger.error(f"读取事件规则配置文件失败: {e}")
        
        return event_rules_config
    
    async def handle_event_polling(self, addr: tuple, protocol_config: Dict[str, Any]):
        """处理事件轮询
        
        Args:
            addr: 发送方地址
            protocol_config: 协议配置
        """
        if self.event_polling_enable:
            # 保存当前协议配置，以便在send_event中使用
            self.current_protocol_config = protocol_config
            
            if self.event_mode == "batch":
                # 模式1：接收到1条请求后就轮询发送所有事件
                await self._handle_batch_mode(addr, protocol_config)
            else:
                # 模式2：接收到1条请求后只回一个事件，下次再请求就回下一个事件类型
                await self._handle_single_event(addr, protocol_config)
    
    async def _handle_batch_mode(self, addr: tuple, protocol_config: Dict[str, Any]):
        """处理批量模式的请求
        
        Args:
            addr: 发送方地址
            protocol_config: 协议配置
        """
        self.logger.info(f"[BATCH MODE] 接收到请求，开始发送所有事件类型")
        
        # 发送所有事件类型
        for event_type in self.event_types:
            await self.send_event(event_type, addr)
            # 添加小延迟，避免发送过快
            await asyncio.sleep(0.1)
        
        # 重置轮询索引
        self.current_event_index = 0
        self.logger.info(f"[BATCH MODE] 所有事件类型发送完成，重置索引")
    
    async def _handle_single_event(self, addr: tuple, protocol_config: Dict[str, Any]):
        """处理单事件模式的请求
        
        Args:
            addr: 发送方地址
            protocol_config: 协议配置
        """
        # 获取当前事件类型
        if self.current_event_index < len(self.event_types):
            event_type = self.event_types[self.current_event_index]
            self.logger.info(f"[SINGLE MODE] 接收到请求，返回事件类型: {event_type['description']} (状态码: {event_type['status']})")
            
            # 发送事件
            await self.send_event(event_type, addr)
            
            # 移动到下一个事件类型
            self.current_event_index += 1
            if self.current_event_index >= len(self.event_types):
                # 重置轮询索引
                self.current_event_index = 0
                self.logger.info(f"[SINGLE MODE] 所有事件类型已返回，重置索引重新开始")
        else:
            # 重置轮询索引
            self.current_event_index = 0
            self.logger.info(f"[SINGLE MODE] 事件索引超出范围，重置索引")
    
    async def send_event(self, event_type, addr):
        """发送事件数据包
        
        Args:
            event_type: 事件类型字典，包含status和description
            addr: 发送方地址，事件将发送回此地址
        """
        if not self.transport:
            return
        
        # 使用原始发送方地址作为目标地址
        target_addr = addr
        
        # 使用当前协议配置或默认协议模板
        if hasattr(self, 'current_protocol_config') and self.current_protocol_config:
            protocol_config = self.current_protocol_config
        else:
            # 使用第一个设备的协议模板作为默认
            device_id, protocol_config = next(iter(self.device_protocols.items()), ("", {}))
            if not protocol_config:
                self.logger.error("没有可用的设备协议模板，无法发送事件")
                return
        
        # 创建透传数据编解码器
        through_codec = ThroughDataCodec(protocol_config)
        
        # 从配置文件中获取事件规则配置
        # 根据协议类型自动选择事件规则配置
        protocol_name = protocol_config.get("protocol", {}).get("name", "")
        vendor = protocol_config.get("vendor", "")
        
        # 优先使用协议特定的事件规则配置
        event_rules = {}
        
        # 尝试按协议名称和厂商获取配置
        if protocol_name:
            event_rules = self.event_rules_config.get(protocol_name, {})
        if not event_rules and vendor:
            event_rules = self.event_rules_config.get(vendor, {})
        if not event_rules:
            # 尝试使用通用事件配置
            event_rules = self.event_rules_config.get("event", {})
        if not event_rules:
            # 最后使用默认配置
            event_rules = {"data": {}}
        
        event_data = event_rules.get("data", {})
        
        # 构建事件数据包
        event_data = {
            "card_id": event_data.get("card_id", "7152"),
            "vendor_id": event_data.get("vendor_id", "B3"),
            "status": event_type["status"]
        }
        
        # 添加时间配置
        import time
        event_data.update({
            "year": time.strftime("%y"),
            "month": time.strftime("%m"),
            "day": time.strftime("%d"),
            "hour": time.strftime("%H"),
            "minute": time.strftime("%M"),
            "second": time.strftime("%S")
        })
        
        # 编码透传数据
        # 根据协议类型构建正确的基础PDU结构
        base_pdu = {
            "through_pdu": {
                "start": "7E",
                "ver": "10",
                "adr": "01",
                "cid1": "80",
                "cid2": "4A",  # 力维事件响应使用4A
                "length": "20",  # 固定长度
                "checksum": "00",
                "end": "0D"
            }
        }
        
        # 力维协议特殊处理：构建正确的事件数据结构
        if protocol_config.get("vendor_type") == "liwei":
            # 力维协议事件数据结构
            liwei_event_data = {
                "group": "F2",
                "type": "EE",
                "dataf": "00",
                "event_source": event_data.get("event_source", "0000000000"),
                "year": event_data.get("year", time.strftime("%y")),
                "month": event_data.get("month", time.strftime("%m")),
                "day": event_data.get("day", time.strftime("%d")),
                "hour": event_data.get("hour", time.strftime("%H")),
                "minute": event_data.get("minute", time.strftime("%M")),
                "second": event_data.get("second", time.strftime("%S")),
                "status": event_type["status"],
                "remark": event_data.get("remark", "00")
            }
            encoded_response = through_codec.encode(base_pdu, liwei_event_data)
        else:
            # 其他协议使用默认结构
            base_pdu["through_pdu"]["data_frame_type"] = "108D"
            encoded_response = through_codec.encode(base_pdu, event_data)
        if not encoded_response:
            self.logger.error("事件数据编码失败")
            return
        
        # 编码B接口响应
        event_packet = self.b_interface_codec.encode(
            encoded_response,  # 透传数据
            b"\x00" * 8,  # 目标地址：SC的地址取值为0x00，8字节
            bytes.fromhex(self.fsu_config["fsuid"]).ljust(20, b"\x00"),  # 源地址：FSU的ID，20字节
            1,  # subDevType
            1,  # subDevAddr
            comm_type=0x0001,  # 命令类型
            rtn_flag=0x00  # 返回标志
        )
        
        # 发送事件包到原始发送方地址
        self.transport.sendto(event_packet, target_addr)
        
        # 记录事件包
        self.logger.info(f"[SEND] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] 发送事件: {event_type['description']} (状态码: {event_type['status']}) 到原始发送方: {target_addr}")
        
        # 记录B接口解析结果
        event_parsed = {
            "P_dest_addr": bytes.fromhex(self.fsu_config["fsuid"]).ljust(20, b"\x00").hex().upper(),
            "P_src_addr": (b"\x00" * 8).hex().upper(),
            "P_subDevType": 1,
            "P_subDev_addr": 1,
            "P_pLen": 5 + len(encoded_response),  # 固定长度 + 透传数据长度
            "RtnFlag": 0x00,
            "CommType": 0x0001,
            "through_data_len": len(encoded_response),
            "through_data": encoded_response,
            "event_info": event_type
        }
        self.logger.debug(self.b_interface_codec.to_str({"raw_data": event_packet.hex().upper(), "parsed": event_parsed}))
    
    def is_event_command(self, command):
        """检查某个指令是否是事件指令
        
        Args:
            command: 指令类型，如 "F0EE" 或 "EE"
            
        Returns:
            bool: 是否是事件指令
        """
        # 只检查完整指令匹配，避免后缀匹配导致的误判
        for event_cmd in self.event_commands:
            if event_cmd.get("command") == command:
                return True
        
        return False
    
    async def event_polling_task(self):
        """事件轮询任务"""
        while True:
            # 检查事件轮询开关
            if not self.event_polling_enable:
                await asyncio.sleep(self.event_polling_interval)
                continue
            
            # 新的轮询逻辑由请求触发，这里保持兼容性
            # 可以根据需要添加其他定期任务
            
            # 等待下一次轮询
            await asyncio.sleep(self.event_polling_interval)
