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
from event.record_manager import RecordManager

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
        
        # 协议事件配置
        self.protocol_event_config = {}
        
        # 按协议类型存储的事件类型列表
        self.protocol_event_types = {}
        
        # 按协议类型存储的事件指令列表
        self.protocol_event_commands = {}
        
        # 按协议类型存储的事件来源配置
        self.protocol_event_sources = {}
        
        # 按协议类型存储的当前轮询事件索引
        self.protocol_current_event_index = {}
        
        # 事件轮询默认配置
        self.event_polling_default_config = {
            "mode": "single",
            "interval": 5
        }
        
        # 设备协议模板
        self.device_protocols = {}
        
        # 当前协议配置
        self.current_protocol_config = None
        
        # 当前请求的卡号信息
        self.current_card_id = ""
        
        # 事件来源配置
        self.event_sources_config = {}
        
        # 记录区管理器，用于力维协议时间类型事件的记录管理
        self.record_manager = RecordManager(max_len=100)
        
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
        # 加载协议事件配置文件
        self._load_protocol_event_config_file()
        
        # 从设备配置中读取事件轮询配置
        device_list = self.device_config.get_device_list()
        if device_list:
            # 使用第一个设备的配置
            device_config = device_list[0]
            self.event_polling_enable = device_config.get("event_polling_enable", False)
            self.event_polling_interval = device_config.get("event_polling_interval", self.event_polling_default_config["interval"])
            self.event_mode = device_config.get("event_mode", self.event_polling_default_config["mode"])
        else:
            # 使用默认配置
            self.event_polling_enable = False
            self.event_polling_interval = self.event_polling_default_config["interval"]
            self.event_mode = self.event_polling_default_config["mode"]
    
    def _load_event_types(self):
        """从配置文件中读取事件类型和事件指令（兼容旧代码）
        
        Returns:
            事件类型列表
        """
        event_types = []
        try:
            # 尝试使用默认协议的事件类型配置
            default_protocol_config = {"vendor": "default"}
            protocol_key = self._get_protocol_key(default_protocol_config)
            
            # 检查是否已经加载了该协议的事件配置
            if protocol_key in self.protocol_event_types:
                return self.protocol_event_types[protocol_key]
            
            # 如果没有加载，尝试加载默认协议的事件配置
            self._load_protocol_event_config(default_protocol_config)
            return self.protocol_event_types.get(protocol_key, [])
        except Exception as e:
            self.logger.error(f"读取事件类型配置文件失败: {e}")
            return []
    
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
    
    def _load_protocol_event_config_file(self):
        """加载协议事件配置文件
        
        Returns:
            协议事件配置字典
        """
        try:
            # 构建协议事件配置文件路径（使用绝对路径）
            import os
            config_path = os.path.join(os.path.dirname(__file__), "..", "config", "protocol_event_config.json")
            config_path = os.path.abspath(config_path)
            
            # 读取协议事件配置文件
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.protocol_event_config = config.get("protocols", {})
                    
                    # 更新事件轮询默认配置
                    polling_config = config.get("event_polling_config", {})
                    self.event_polling_default_config["mode"] = polling_config.get("default_mode", "single")
                    self.event_polling_default_config["interval"] = polling_config.get("default_interval", 5)
                    
                    self.logger.info(f"从配置文件加载了协议事件配置: {config_path}")
                    self.logger.info(f"支持的协议: {list(self.protocol_event_config.keys())}")
            else:
                self.logger.warning(f"协议事件配置文件不存在: {config_path}")
                self.protocol_event_config = {}
        except Exception as e:
            self.logger.error(f"读取协议事件配置文件失败: {e}")
            self.protocol_event_config = {}
    
    def _get_protocol_key(self, protocol_config: Dict[str, Any]) -> str:
        """根据协议配置生成唯一的协议标识
        
        Args:
            protocol_config: 协议配置
            
        Returns:
            协议标识字符串
        """
        # 尝试从协议配置中获取唯一标识
        vendor = protocol_config.get("vendor", "")
        vendor_type = protocol_config.get("vendor_type", "")
        protocol_name = protocol_config.get("protocol", {}).get("name", "")
        
        # 生成协议标识
        # 优先使用 vendor_type，因为它通常是更通用的标识
        if vendor_type:
            protocol_key = vendor_type
        elif vendor:
            protocol_key = vendor
        elif protocol_name:
            protocol_key = protocol_name
        else:
            protocol_key = "default"
        
        # 检查协议标识是否在配置中存在
        if protocol_key not in self.protocol_event_config:
            # 尝试使用更通用的标识
            if "_" in protocol_key:
                base_key = protocol_key.split("_")[0]
                if base_key in self.protocol_event_config:
                    return base_key
            return "default"
        
        return protocol_key
    
    def _load_protocol_event_config(self, protocol_config: Dict[str, Any]):
        """为特定协议加载事件配置
        
        Args:
            protocol_config: 协议配置
        """
        protocol_key = self._get_protocol_key(protocol_config)
        
        try:
            # 从协议配置中获取事件配置
            protocol_info = self.protocol_event_config.get(protocol_key, {})
            event_config = protocol_info.get("event_config", {})
            
            # 加载事件类型配置
            event_types_file = event_config.get("event_types_file", "")
            
            # 如果没有配置文件路径，尝试使用默认路径
            if not event_types_file:
                import os
                if protocol_key == "liwei":
                    event_types_file = os.path.join(os.path.dirname(__file__), "..", "config", "liwei", "event_types.json")
                    event_types_file = os.path.abspath(event_types_file)
            
            if event_types_file and os.path.exists(event_types_file):
                with open(event_types_file, "r", encoding="utf-8") as f:
                    event_config_data = json.load(f)
                    event_types = event_config_data.get("event_types", [])
                    event_commands = event_config_data.get("event_commands", [])
                    self.protocol_event_types[protocol_key] = event_types
                    self.protocol_event_commands[protocol_key] = event_commands
                    self.logger.info(f"为协议 {protocol_key} 加载了 {len(event_types)} 个事件类型和 {len(event_commands)} 个事件指令")
            else:
                self.logger.warning(f"事件类型配置文件不存在: {event_types_file}")
                self.protocol_event_types[protocol_key] = []
                self.protocol_event_commands[protocol_key] = []
            
            # 加载事件来源配置
            event_sources_file = event_config.get("event_sources_file", "")
            
            # 如果没有配置文件路径，尝试使用默认路径
            if not event_sources_file:
                import os
                if protocol_key == "liwei":
                    event_sources_file = os.path.join(os.path.dirname(__file__), "..", "config", "liwei", "events", "event_sources.json")
                    event_sources_file = os.path.abspath(event_sources_file)
            
            if event_sources_file and os.path.exists(event_sources_file):
                with open(event_sources_file, "r", encoding="utf-8") as f:
                    event_sources_data = json.load(f)
                    self.protocol_event_sources[protocol_key] = event_sources_data
                    self.logger.info(f"为协议 {protocol_key} 加载了事件来源配置: {event_sources_file}")
            else:
                self.logger.warning(f"事件来源配置文件不存在: {event_sources_file}")
                self.protocol_event_sources[protocol_key] = {"event_sources": {}, "default_source": "0000000000"}
        except Exception as e:
            self.logger.error(f"加载协议事件配置失败: {e}")
            self.protocol_event_types[protocol_key] = []
            self.protocol_event_commands[protocol_key] = []
            self.protocol_event_sources[protocol_key] = {"event_sources": {}, "default_source": "0000000000"}
        
        # 初始化该协议的轮询索引
        if protocol_key not in self.protocol_current_event_index:
            self.protocol_current_event_index[protocol_key] = 0
    

    
    async def handle_event_polling(self, addr: tuple, protocol_config: Dict[str, Any], card_id: str = ""):
        """处理事件轮询
        
        Args:
            addr: 发送方地址
            protocol_config: 协议配置
            card_id: 卡号信息
        """
        if self.event_polling_enable:
            # 保存当前协议配置，以便在send_event中使用
            self.current_protocol_config = protocol_config
            # 保存当前请求的卡号信息
            self.current_card_id = card_id
            
            # 获取协议标识
            protocol_key = self._get_protocol_key(protocol_config)
            self.logger.info(f"[EVENT POLLING] 处理事件轮询，协议标识: {protocol_key}")
            
            # 打印协议配置信息
            self.logger.debug(f"[EVENT POLLING] 协议配置: {protocol_config}")
            
            # 确保该协议的事件类型已加载
            if protocol_key not in self.protocol_event_types:
                self.logger.info(f"[EVENT POLLING] 加载协议 {protocol_key} 的事件配置")
                self._load_protocol_event_config(protocol_config)
            
            # 打印当前轮询状态
            event_types = self.protocol_event_types.get(protocol_key, [])
            current_index = self.protocol_current_event_index.get(protocol_key, 0)
            self.logger.info(f"[EVENT POLLING] 当前轮询状态 - 事件类型数量: {len(event_types)}, 当前索引: {current_index}")
            
            # 打印事件类型列表
            for i, event_type in enumerate(event_types):
                self.logger.debug(f"[EVENT POLLING] 事件类型 {i}: {event_type}")
            
            if self.event_mode == "batch":
                # 模式1：接收到1条请求后就轮询发送所有事件
                await self._handle_batch_mode(addr, protocol_config, protocol_key)
            else:
                # 模式2：接收到1条请求后只回一个事件，下次再请求就回下一个事件类型
                await self._handle_single_event(addr, protocol_config, protocol_key)
    
    async def _handle_batch_mode(self, addr: tuple, protocol_config: Dict[str, Any], protocol_key: str):
        """处理批量模式的请求
        
        Args:
            addr: 发送方地址
            protocol_config: 协议配置
            protocol_key: 协议标识
        """
        self.logger.info(f"[BATCH MODE] 接收到请求，开始发送所有事件类型")
        
        # 获取该协议的事件类型列表
        event_types = self.protocol_event_types.get(protocol_key, [])
        
        # 发送所有事件类型
        for event_type in event_types:
            await self.send_event(event_type, addr)
            # 添加小延迟，避免发送过快
            await asyncio.sleep(0.1)
        
        # 重置该协议的轮询索引
        self.protocol_current_event_index[protocol_key] = 0
        self.logger.info(f"[BATCH MODE] 所有事件类型发送完成，重置索引")
    
    async def _handle_single_event(self, addr: tuple, protocol_config: Dict[str, Any], protocol_key: str):
        """处理单事件模式的请求
        
        Args:
            addr: 发送方地址
            protocol_config: 协议配置
            protocol_key: 协议标识
        """
        # 强制使用"liwei"作为协议标识，确保轮询索引能够正确维护
        protocol_key = "liwei"
        self.logger.info(f"[SINGLE MODE] 强制使用协议标识: {protocol_key}")
        
        # 强制加载事件类型配置
        import os
        event_types_file = os.path.join(os.path.dirname(__file__), "..", "config", "liwei", "event_types.json")
        event_types_file = os.path.abspath(event_types_file)
        
        self.logger.debug(f"[SINGLE MODE] 强制加载事件类型文件: {event_types_file}")
        
        # 直接从文件加载事件类型，不依赖缓存
        event_types = []
        if os.path.exists(event_types_file):
            try:
                with open(event_types_file, "r", encoding="utf-8") as f:
                    event_config_data = json.load(f)
                    event_types = event_config_data.get("event_types", [])
                    event_commands = event_config_data.get("event_commands", [])
                    self.protocol_event_types[protocol_key] = event_types
                    self.protocol_event_commands[protocol_key] = event_commands
                    self.logger.info(f"[SINGLE MODE] 强制加载了 {len(event_types)} 个事件类型和 {len(event_commands)} 个事件指令")
            except Exception as e:
                self.logger.error(f"[SINGLE MODE] 强制加载事件类型失败: {e}")
        
        # 确保事件类型列表不为空
        if not event_types:
            self.logger.warning(f"[SINGLE MODE] 协议 {protocol_key} 没有可用的事件类型")
            return
        
        
        # 初始化或获取当前轮询索引（使用全局变量确保状态持久化）
        if protocol_key not in self.protocol_current_event_index:
            self.logger.info(f"[SINGLE MODE] 轮询索引未初始化，初始化为 0")
            self.protocol_current_event_index[protocol_key] = 0
        
        # 打印当前轮询索引
        current_index = self.protocol_current_event_index[protocol_key]
        self.logger.info(f"[SINGLE MODE] 当前轮询索引: {current_index}")
        
        # 确保轮询索引在有效范围内
        if current_index >= len(event_types):
            self.logger.info(f"[SINGLE MODE] 轮询索引超出范围，重置为 0")
            current_index = 0
            self.protocol_current_event_index[protocol_key] = current_index
        
        # 获取当前事件类型
        event_type = event_types[current_index]
        self.logger.info(f"[SINGLE MODE] 接收到请求，返回事件类型: {event_type['description']} (状态码: {event_type['status']})")
        
        # 发送事件
        await self.send_event(event_type, addr)
        
        # 计算下一个轮询索引
        next_index = current_index + 1
        if next_index >= len(event_types):
            # 重置轮询索引
            next_index = 0
            self.logger.info(f"[SINGLE MODE] 所有事件类型已返回，重置索引重新开始")
        
        # 保存下一个轮询索引
        self.protocol_current_event_index[protocol_key] = next_index
        self.logger.info(f"[SINGLE MODE] 轮询索引已更新: {current_index} -> {next_index}")
        
        # 打印下次请求将返回的事件类型
        if next_index < len(event_types):
            next_event_type = event_types[next_index]
            self.logger.info(f"[SINGLE MODE] 下次请求将返回事件类型 {next_index}: {next_event_type['description']} (状态码: {next_event_type['status']})")
    
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
        
        # 检查event_rules_config属性是否存在，如果不存在则初始化
        if not hasattr(self, 'event_rules_config'):
            self.event_rules_config = {}
        
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
        # 为不同类型的事件设置不同的卡号和事件来源
        status = event_type["status"]
        
        # 生成动态卡号（基于状态码和当前时间）
        import time
        if hasattr(self, 'current_card_id') and self.current_card_id:
            # 如果有请求中的卡号，优先使用
            card_id = self.current_card_id
        else:
            # 生成动态卡号，格式为：状态码 + 时间戳后6位
            timestamp = str(int(time.time() * 1000))[-6:]
            card_id = f"{status}{timestamp}"
        
        event_data = {
            "card_id": card_id,
            "vendor_id": event_data.get("vendor_id", "B3"),
            "status": status
        }
        
        # 为不同类型的事件设置不同的事件来源
        if hasattr(self, 'current_card_id') and self.current_card_id:
            # 如果有请求中的卡号，优先使用
            event_data["event_source"] = self.current_card_id
        else:
            # 从当前协议的事件来源配置中获取
            protocol_key = ""
            if hasattr(self, 'current_protocol_config') and self.current_protocol_config:
                protocol_key = self._get_protocol_key(self.current_protocol_config)
            
            # 获取当前协议的事件来源配置
            event_sources_config = self.protocol_event_sources.get(protocol_key, {})
            event_sources = event_sources_config.get("event_sources", {})
            default_source = event_sources_config.get("default_source", "0000000000")
            
            if status in event_sources:
                source_config = event_sources[status]
                source = source_config.get("source", default_source)
                
                if source == "time_based":
                    # 使用当前时间作为事件来源
                    format_str = source_config.get("format", "%m%d%H%M%S")
                    event_data["event_source"] = time.strftime(format_str)
                else:
                    event_data["event_source"] = source
            else:
                # 使用默认事件来源
                event_data["event_source"] = default_source
        
        # 添加时间配置
        import time
        event_data.update({
            "year": time.strftime("%y"),
            "month": time.strftime("%m"),
            "day": time.strftime("%d"),
            "hour": time.strftime("%H"),
            "minute": time.strftime("%M"),
            "second": time.strftime("%S"),
            "remark": "00"
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
                "length": "00",  # 长度会在编码时自动计算
                "checksum": "00",
                "end": "0D"
            }
        }
        
        # 初始化protocol_key变量
        protocol_key = ""
        
        # 获取协议标识
        if hasattr(self, 'current_protocol_config') and self.current_protocol_config:
            protocol_key = self._get_protocol_key(self.current_protocol_config)
            
            # 强制检查是否是力维协议
            vendor = self.current_protocol_config.get("vendor", "")
            vendor_type = self.current_protocol_config.get("vendor_type", "")
            protocol_name = self.current_protocol_config.get("protocol", {}).get("name", "")
            
            if any(keyword in str(value).lower() for keyword in ["liwei", "力维"] for value in [vendor, vendor_type, protocol_name]):
                protocol_key = "liwei"
        
        # 力维协议特殊处理：构建正确的事件数据结构
        if protocol_config.get("vendor_type") == "liwei" or protocol_key == "liwei":
            # 构建事件记录
            event_record = {
                "status": event_type["status"],
                "description": event_type["description"],
                "year": event_data.get("year", time.strftime("%y")),
                "month": event_data.get("month", time.strftime("%m")),
                "day": event_data.get("day", time.strftime("%d")),
                "hour": event_data.get("hour", time.strftime("%H")),
                "minute": event_data.get("minute", time.strftime("%M")),
                "second": event_data.get("second", time.strftime("%S")),
                "event_source": event_data.get("event_source", "0000000000"),
                "remark": event_data.get("remark", "00"),
                "timestamp": time.time()
            }
            
            # 添加记录到记录区管理器
            self.record_manager.add_record(event_record)
            
            # 获取记录区信息
            record_info = self.record_manager.get_record_info()
            
            # 检查是否是远程监控(0XE7)请求
            is_remote_monitoring = event_type.get("type") == "E7" and event_type.get("group") == "F2"
            
            # 力维协议事件数据结构
            liwei_event_data = {
                "group": event_type.get("group", "F2"),
                "type": event_type.get("type", "EE"),
                "dataf": "00",
                "cid2": "71",
                "adr": "80"
            }
            
            # 如果不是远程监控请求，添加记录区信息
            if not is_remote_monitoring:
                liwei_event_data.update({
                    "savep": record_info["SAVEP"],
                    "loadp": record_info["LOADP"],
                    "mf": record_info["MF"]
                })
            
            # 如果不是远程监控请求，添加时间相关字段
            if not is_remote_monitoring:
                # 确保使用正确的事件类型状态码
                status = event_type["status"]
                
                # 根据状态码获取事件来源
                event_source = "0000000000"
                
                # 如果有请求中的卡号，优先使用
                if hasattr(self, 'current_card_id') and self.current_card_id:
                    event_source = self.current_card_id
                    self.logger.info(f"[SEND] 使用请求中的卡号作为事件来源: {event_source}")
                else:
                    # 从当前协议的事件来源配置中获取
                    event_sources_config = self.protocol_event_sources.get(protocol_key, {})
                    event_sources = event_sources_config.get("event_sources", {})
                    default_source = event_sources_config.get("default_source", "0000000000")
                    
                    if status in event_sources:
                        source_config = event_sources[status]
                        event_source = source_config.get("source", default_source)
                    else:
                        event_source = default_source
                    self.logger.info(f"[SEND] 使用配置中的事件来源: {event_source}")
                
                liwei_event_data.update({
                    "event_source": event_source,
                    "year": event_data.get("year", time.strftime("%y")),
                    "month": event_data.get("month", time.strftime("%m")),
                    "day": event_data.get("day", time.strftime("%d")),
                    "hour": event_data.get("hour", time.strftime("%H")),
                    "minute": event_data.get("minute", time.strftime("%M")),
                    "second": event_data.get("second", time.strftime("%S")),
                    "status": status,
                    "remark": event_data.get("remark", "00")
                })
                
                # 打印构建的力维协议事件数据
                self.logger.info(f"[SEND] 构建的力维协议事件数据: {liwei_event_data}")
            
            # 处理远程监控(0XE7)请求
            if is_remote_monitoring:
                # 从配置文件中直接加载4AF2E7的配置
                import os
                config_dir = self.fsu_config.get("config_dir", "./config/bangsun_old")
                # 力维协议的配置文件路径
                liwei_rules_path = os.path.join(config_dir, "liwei", "rules", "default.json")
                
                # 打印调试信息
                self.logger.debug(f"配置目录: {config_dir}")
                self.logger.debug(f"力维协议规则配置文件路径: {liwei_rules_path}")
                self.logger.debug(f"文件是否存在: {os.path.exists(liwei_rules_path)}")
                
                # 读取力维协议规则配置
                if os.path.exists(liwei_rules_path):
                    try:
                        with open(liwei_rules_path, "r", encoding="utf-8") as f:
                            liwei_rules = json.load(f)
                            self.logger.debug(f"读取到的配置: {liwei_rules}")
                            if "4AF2E7" in liwei_rules:
                                e7_config = liwei_rules["4AF2E7"].get("data", {})
                                self.logger.debug(f"4AF2E7配置: {e7_config}")
                                if "work_status" in e7_config:
                                    liwei_event_data["work_status"] = e7_config["work_status"]
                                    self.logger.debug(f"设置work_status: {e7_config['work_status']}")
                                if "line_status" in e7_config:
                                    liwei_event_data["line_status"] = e7_config["line_status"]
                                    self.logger.debug(f"设置line_status: {e7_config['line_status']}")
                            else:
                                self.logger.warning(f"配置文件中没有4AF2E7配置")
                    except Exception as e:
                        self.logger.error(f"读取力维协议规则配置失败: {e}")
                else:
                    self.logger.error(f"力维协议规则配置文件不存在: {liwei_rules_path}")
            
            # 打印构建的力维协议事件数据
            self.logger.info(f"[SEND] 构建的力维协议事件数据: {liwei_event_data}")
            
            # 编码响应数据
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
        self.logger.info(f"[######## FSU 向动环发送数据，目的地址：{target_addr}] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}]")
        self.logger.info(f"数据包长度: {len(event_packet)} 字节")
        self.logger.info(f"HEX: {event_packet.hex().upper()}")
        
        # 记录B接口解析结果
        event_parsed = {
            "P_header": "0xFF",
            "P_dest_addr": bytes.fromhex(self.fsu_config["fsuid"]).ljust(20, b"\x00").hex().upper(),
            "P_src_addr": (b"\x00" * 8).hex().upper(),
            "P_subDevType": 0x01,
            "P_subDev_addr": 0x01,
            "P_pLen": 5 + len(encoded_response),  # 固定长度 + 透传数据长度
            "RtnFlag": 0x00,
            "CommType": 0x0001,
            "透传数据长度": len(encoded_response),
            "透传数据": encoded_response.hex().upper(),
            "P_verify": "0x00",
            "P_tailer": "0xFE"
        }
        self.logger.info(f"Parsed: ")
        for key, value in event_parsed.items():
            self.logger.info(f"    {key}: {value}")
        
        # 记录透传数据层的格式化信息
        self.logger.info(f"[透传数据层]原始数据:")
        self.logger.info(f"    数据包长度: {len(encoded_response)} 字节")
        self.logger.info(f"    HEX: {encoded_response.hex().upper()}")
        
        # 构建透传数据解析结果
        resp_through_pdu = {}
        try:
            # 创建透传数据编解码器
            through_codec = ThroughDataCodec(protocol_config)
            resp_success, resp_decoded = through_codec.decode(encoded_response)
            if resp_success:
                resp_parsed = resp_decoded.get("parsed", {})
                if isinstance(resp_parsed, dict):
                    resp_through_pdu = resp_parsed.get("through_pdu", {})
        except Exception:
            pass
        
        self.logger.info("[透传数据层] 协议栈解析:")
        self.logger.info("    透传数据PDU:")
        for key, value in resp_through_pdu.items():
            self.logger.info(f"        {key}: {value}")
        
        # 记录发送事件信息
        self.logger.info(f"[SEND] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] 发送事件: {event_type['description']} (状态码: {event_type['status']}) 到原始发送方: {target_addr}")
    
    def is_event_command(self, command, protocol_config: Dict[str, Any] = None):
        """检查某个指令是否是事件指令
        
        Args:
            command: 指令类型，如 "F0EE" 或 "EE"
            protocol_config: 协议配置，用于确定协议类型
            
        Returns:
            bool: 是否是事件指令
        """
        # 如果提供了协议配置，使用该协议的事件指令
        if protocol_config:
            protocol_key = self._get_protocol_key(protocol_config)
            event_commands = self.protocol_event_commands.get(protocol_key, [])
            
            # 检查该协议的事件指令
            for event_cmd in event_commands:
                if event_cmd.get("command") == command:
                    return True
        
        # 检查默认事件指令（兼容旧代码）
        # 使用默认协议的事件指令
        default_event_commands = self.protocol_event_commands.get("default", [])
        for event_cmd in default_event_commands:
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
