#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UDP协议处理类
"""

import asyncio
import os
import json
from typing import Dict, Any, Tuple
from codec.b_interface_codec import BInterfaceCodec
from codec.through_data_codec import ThroughDataCodec
from .base_protocol import BaseProtocol
from utils.log_manager import LogManager
from event.event_manager import EventManager

class UDPProtocol(BaseProtocol, asyncio.DatagramProtocol):
    """UDP协议处理类"""
    
    def __init__(self, fsu_config: Dict[str, Any], device_config: Any, b_interface_codec: BInterfaceCodec, log_config: Dict[str, Any], performance_mode: bool, sc_iot_config: Dict[str, Any]):
        """初始化UDP协议处理器
        
        Args:
            fsu_config: FSU配置
            device_config: 设备配置
            b_interface_codec: B接口编解码器
            log_config: 日志配置
            performance_mode: 性能模式标志
            sc_iot_config: SC IoT中心配置
        """
        super().__init__()
        self.fsu_config = fsu_config
        self.device_config = device_config
        self.b_interface_codec = b_interface_codec
        self.performance_mode = performance_mode
        self.sc_iot_config = sc_iot_config  # 保存SC IoT中心配置
        self.transport = None
        self.logger = LogManager.get_device_logger(fsu_config["fsuname"], log_config, "UDP")

        # 被规则标记为关闭的SC地址集合（timeout=true）
        self.closed_sc_addrs = set()

        # 创建事件管理器
        self.event_manager = EventManager(fsu_config, device_config, b_interface_codec, self.logger)
        self.event_manager.set_sc_iot_config(sc_iot_config)

        # 加载设备协议模板和规则
        self.device_protocols = self.load_protocols()
        self.event_manager.set_device_protocols(self.device_protocols)
        

    
    def connection_made(self, transport: asyncio.DatagramTransport):
        """建立连接时调用
        
        Args:
            transport: UDP传输对象
        """
        self.transport = transport
        self.event_manager.set_transport(transport)
        self.logger.info(f"UDP服务已启动，监听端口: {self.fsu_config['port']}")
    
    def datagram_received(self, data: bytes, addr: tuple):
        """收到数据报时调用
        
        Args:
            data: 收到的数据
            addr: 发送方地址
        """
        # 如果该SC地址已被规则标记为关闭，则忽略后续请求
        if addr in self.closed_sc_addrs:
            self.logger.info(f"[DROP] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] SC地址 {addr} 已被标记为关闭，忽略请求")
            return

        # 接收到数据增加打印客户端ip和端口
        self.logger.info(f"[收到UDP数据，来自: {addr}，数据长度: {len(data)} 字节] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] ")

        # 检查配置是否更新，如果更新则重新加载（性能模式下跳过）
        if not self.performance_mode and self.device_config.check_for_updates():
            self.reload_protocols()
        
        # 解码B接口数据
        through_data, b_interface_result = self.b_interface_codec.decode(data)
        

        # 详细的B接口解析结果
        self.logger.info(self.b_interface_codec.to_str({'raw_data': data.hex().upper(), 'parsed': b_interface_result}))
        
        # 处理透传数据
        asyncio.create_task(self._handle_through_data(through_data, addr, b_interface_result))
    

    
    async def _handle_through_data(self, through_data: bytes, addr: tuple, b_interface_result: Dict[str, Any]):
        """处理透传数据
        
        Args:
            through_data: 透传数据
            addr: 发送方地址
            b_interface_result: B接口解析结果
        """
        if not through_data:
            return
        
        # 使用第一个设备的协议模板
        # self.logger.debug(f"设备协议模板: {self.device_protocols}")
        device_id, protocol_config = next(iter(self.device_protocols.items()), ("", {}))
        if not protocol_config:
            self.logger.error("没有可用的设备协议模板")
            return
        self.logger.debug(f"使用的设备协议配置: {protocol_config}")
        
        # 创建透传数据编解码器
        through_codec = ThroughDataCodec(protocol_config)
        
        # 解码透传数据
        success, parsed_result = through_codec.decode(through_data)
        if not success:
            self.logger.error(f"透传数据解码失败: {parsed_result}")
            return
        
        # 打印透传数据解析结果
        self.logger.info(through_codec.to_str(parsed_result))
        
        # 获取实际的解析数据（parsed字段的内容）
        parsed_data = parsed_result.get("parsed", {})
        self.logger.debug(f"parsed_data: {parsed_data}")
        
        # 生成响应
        rule_response = self._generate_response(protocol_config, parsed_data)
        if not rule_response:
            return
        
        # 检查是否需要超时关闭连接
        if rule_response.get("timeout", False):
            self.logger.info(f"[SEND] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] 规则配置timeout=true，标记SC地址 {addr} 为已关闭")
            # 标记SC地址为已关闭，后续请求将被忽略
            self.closed_sc_addrs.add(addr)
            return
        
        # 获取响应数据
        response_data = rule_response.get("data", {})
        
        if not response_data:
            return
        
        # 编码响应
        encoded_response = through_codec.encode(parsed_data, response_data)
        if not encoded_response:
            self.logger.error("透传数据编码失败")
            return
        
        # 添加延迟（如果不是性能模式）
        delay = rule_response.get("delay_ms", 0)
        if not self.performance_mode and delay > 0:
            await asyncio.sleep(delay / 1000.0)
        
        # 编码B接口响应
        # 当SC向mock发送请求时，生成的响应包中：   --> 响应中P_dest_addr与P_src_addr需要切换位置
        # P_dest_addr：目标设备地址，FSU的ID（20字节）
        # P_src_addr：源设备地址，SC的地址取值为0x00（8字节）
        resp_packet = self.b_interface_codec.encode(
            encoded_response,
            b"\x00" * 8,
            bytes.fromhex(self.fsu_config["fsuid"]).ljust(20, b"\x00"),
            1,  # subDevType
            1,  # subDevAddr
            comm_type=0x0001,
            rtn_flag=0x00
        )
        
        # 发送响应
        self.transport.sendto(resp_packet, addr)
        
        # 记录发送的响应
        self.logger.info(f"[######## FSU 向动环发送数据，目的地址：{addr}] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] ")
        
        # 记录B接口解析结果
        resp_parsed = {
            "P_dest_addr": bytes.fromhex(self.fsu_config["fsuid"]).ljust(20, b"\x00").hex().upper(),
            "P_src_addr": (b"\x00" * 8).hex().upper(),
            "P_subDevType": 1,
            "P_subDev_addr": 1,
            "P_pLen": 5 + len(encoded_response),  # 固定长度 + 透传数据长度
            "RtnFlag": 0x00,
            "CommType": 0x0001,
            "through_data_len": len(encoded_response),
            "through_data": encoded_response
        }
        self.logger.info(self.b_interface_codec.to_str({'raw_data': resp_packet.hex().upper(), 'parsed': resp_parsed}) )
        
        # 记录透传数据层的格式化信息
        # 直接构建响应的解析结果，避免解码失败
        resp_through_pdu = parsed_data.get("through_pdu", {})
        try:
            resp_success, resp_decoded = through_codec.decode(encoded_response)
            if resp_success:
                resp_parsed = resp_decoded.get("parsed", {})
                if isinstance(resp_parsed, dict):
                    resp_through_pdu = resp_parsed.get("through_pdu", resp_through_pdu)
        except Exception:
            pass
        resp_through_result = {
            "raw_data": encoded_response.hex().upper(),
            "parsed": {
                "through_pdu": resp_through_pdu,
                "through_sdu": response_data
            }
        }
        self.logger.info(through_codec.to_str(resp_through_result))
        
        # 只有当收到事件查询指令时才触发事件轮询
        # 构建完整的指令类型（如 F0EE）
        group = parsed_data.get("through_pdu", {}).get("group", "")
        current_type = parsed_data.get("through_pdu", {}).get("type", "")
        full_command = f"{group}{current_type}" if group else current_type
        
        # 检查是否是事件查询指令（只检查完整命令）
        if self.event_manager.is_event_command(full_command):
            # 使用事件管理器处理事件轮询
            await self.event_manager.handle_event_polling(addr, protocol_config)
    

    

    
    async def send_heartbeat(self):
        """发送心跳包
        """
        # 检查心跳开关
        heartbeat_enable = self.fsu_config.get("heartbeat_enable", False)
        if not heartbeat_enable:
            self.logger.debug(f"[SEND] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] 心跳发送开关已关闭，跳过发送心跳包")
            return
        
        if not self.transport:
            return
        
        # 从SC IoT中心配置获取目标地址
        sc_target_addr = (self.sc_iot_config["host"], self.sc_iot_config["port"])
        
        # 构建心跳包的解析数据，明确设置P_pLen为3
        parsed_data = {
            "P_dest_addr": (b"\x00" * 8).hex().upper(),  # SC地址为0x00，8字节
            "P_src_addr": bytes.fromhex(self.fsu_config["fsuid"]).ljust(20, b"\x00").hex().upper(),  # FSU的ID，20字节
            "P_subDevType": 1,  # 子设备类型01
            "P_subDev_addr": 1,  # 子设备地址
            "P_pLen": 3,  # 协议族数据包长度，值为3
            "RtnFlag": 0xED,  # 返回标志值为ED
            "CommType": 0x0002,  # 心跳命令类型
            "through_data": b""  # 透传数据为空
        }
        
        # 构建心跳包
        heartbeat_packet = self.b_interface_codec.encode(
            b"",  # 透传数据为空
            b"\x00" * 8,  # 目标地址：SC的地址取值为0x00，8字节
            bytes.fromhex(self.fsu_config["fsuid"]).ljust(20, b"\x00"),  # 源地址：FSU的ID，20字节
            1,  # subDevType
            1,  # subDevAddr
            comm_type=0x0002,  # 心跳命令类型
            rtn_flag=0xED  # 返回标志值为ED
        )
        
        # 发送心跳包到SC IoT中心
        self.transport.sendto(heartbeat_packet, sc_target_addr)
        
        # 记录心跳包
        self.logger.debug(f"[SEND] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] 发送心跳包到SC IoT中心: {sc_target_addr}")
        # 使用构建的解析结果记录日志
        self.logger.debug(self.b_interface_codec.to_str({"raw_data": heartbeat_packet.hex().upper(), "parsed": parsed_data}))
    

    

    
    async def event_polling_task(self):
        """事件轮询任务
        
        注意：根据新的需求，轮询逻辑已经移到了事件管理器中，
        该方法现在主要用于保持兼容性，实际的轮询逻辑由请求触发。
        """
        while True:
            # 检查事件轮询开关
            if not getattr(self.event_manager, 'event_polling_enable', False):
                await asyncio.sleep(getattr(self.event_manager, 'event_polling_interval', 5))
                continue
            
            # 新的轮询逻辑由请求触发，这里保持兼容性
            # 可以根据需要添加其他定期任务
            
            # 等待下一次轮询
            await asyncio.sleep(getattr(self.event_manager, 'event_polling_interval', 5))
