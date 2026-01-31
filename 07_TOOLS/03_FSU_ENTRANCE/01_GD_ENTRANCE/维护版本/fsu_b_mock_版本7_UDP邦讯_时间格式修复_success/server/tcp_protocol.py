#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCP协议处理类
"""

import asyncio
from typing import Dict, Any
from codec.through_data_codec import ThroughDataCodec
from event.event_center import event_center
from .base_protocol import BaseProtocol
from utils.log_manager import LogManager


class TCPProtocol(BaseProtocol, asyncio.Protocol):
    """TCP协议处理类"""

    def __init__(self, fsu_config: Dict[str, Any], device_config: Any, log_config: Dict[str, Any],
                 performance_mode: bool):
        """初始化TCP协议处理器
        
        Args:
            fsu_config: FSU配置
            device_config: 设备配置
            log_config: 日志配置
            performance_mode: 性能模式标志
        """
        super().__init__()
        self.fsu_config = fsu_config
        self.device_config = device_config
        self.performance_mode = performance_mode
        self.transport = None
        self.logger = LogManager.get_device_logger(fsu_config["fsuname"], log_config, "TCP")

        # 加载设备协议模板和规则
        self.device_protocols = self.load_protocols()

    def connection_made(self, transport: asyncio.Transport):
        """建立连接时调用
        
        Args:
            transport: TCP传输对象
        """
        self.transport = transport
        self.logger.info(f"TCP连接已建立，客户端地址: {transport.get_extra_info('peername')}")

    def data_received(self, data: bytes):
        """收到数据时调用
        
        Args:
            data: 收到的数据
        """
        client_addr = self.transport.get_extra_info('peername')
        self.logger.info(f"收到TCP数据，来自: {client_addr}, 数据长度: {len(data)} 字节")

        # 检查配置是否更新，如果更新则重新加载（性能模式下跳过）
        if not self.performance_mode and self.device_config.check_for_updates():
            self.reload_protocols()

        # TCP协议直接处理透传数据，不需要B接口解码
        asyncio.create_task(self._handle_tcp_data(data))

    async def _handle_tcp_data(self, data: bytes):
        """处理TCP数据
        
        Args:
            data: TCP数据
        """
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
        success, parsed_result = through_codec.decode(data)

        # 记录解析结果
        self.logger.info(f"[ TCP数据] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}]")
        self.logger.info(through_codec.to_str(parsed_result))

        if not success:
            self.logger.error(f"透传数据解码失败: {parsed_result}")
            return

        self.logger.debug(f"解析结果: {parsed_result}")

        # 获取实际的解析数据（parsed字段的内容）
        parsed_data = parsed_result.get("parsed", {})

        # 生成响应
        self.logger.debug(f"生成响应，解析数据: {parsed_data}")
        response_data = self._generate_response(protocol_config, parsed_data)
        self.logger.debug(f"生成的响应数据: {response_data}")
        if not response_data:
            self.logger.error("生成的响应数据为空")
            return

        # 检查并更新响应数据（事件处理）
        response_data = event_center.check_and_update_response(parsed_data, response_data)

        # 编码响应
        encoded_response = through_codec.encode(parsed_data, response_data)
        self.logger.debug(f"编码后的响应数据: {encoded_response.hex().upper()}")
        if not encoded_response:
            self.logger.error("透传数据编码失败")
            return

        # 添加延迟（如果不是性能模式）
        delay = through_codec.get_response_delay({}, self.performance_mode)
        if delay > 0:
            await asyncio.sleep(delay / 1000.0)

        # 发送响应
        self.transport.write(encoded_response)

        # 记录发送的响应
        self.logger.info(f"[FSU向动环返回应答 ] fsu[{self.fsu_config['fsuname']}:{self.fsu_config['fsuid']}] ")
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
        # 添加调试日志
        resp_str = through_codec.to_str(resp_through_result)
        self.logger.info(resp_str)

    def connection_lost(self, exc):
        """连接关闭时调用
        
        Args:
            exc: 异常信息
        """
        self.logger.info(f"TCP连接已关闭: {exc}")
