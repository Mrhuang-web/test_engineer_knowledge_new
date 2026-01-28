#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器管理器，负责启动和管理UDP和TCP服务器
"""

import asyncio
from typing import Dict, Any
from codec.b_interface_codec import BInterfaceCodec
from .udp_protocol import UDPProtocol
from .tcp_protocol import TCPProtocol
from utils.log_manager import LogManager

async def run_udp_server(fsu_config: Dict[str, Any], device_config: Any, log_config: Dict[str, Any], performance_mode: bool, sc_iot_config: Dict[str, Any]):
    """运行UDP服务器
    
    Args:
        fsu_config: FSU配置
        device_config: 设备配置
        log_config: 日志配置
        performance_mode: 性能模式标志
        sc_iot_config: SC IoT中心配置
    """
    loop = asyncio.get_running_loop()
    b_interface_codec = BInterfaceCodec()
    
    # 创建UDP协议实例
    udp_protocol = UDPProtocol(fsu_config, device_config, b_interface_codec, log_config, performance_mode, sc_iot_config)
    
    # 启动UDP服务器
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: udp_protocol,
        local_addr=(fsu_config["host"], fsu_config["port"])
    )
    
    # 启动心跳发送任务（仅当heartbeat_enable为true时）
    heartbeat_enable = fsu_config.get("heartbeat_enable", False)
    if heartbeat_enable:
        heartbeat_interval = fsu_config.get("heartbeat_interval", 120)
        asyncio.create_task(heartbeat_task(udp_protocol, heartbeat_interval))
    
    # 启动事件轮询任务（仅当event_polling_enable为true时）
    # 从设备配置中读取事件轮询配置
    device_list = device_config.get_device_list()
    event_polling_enable = False
    event_polling_interval = 5
    
    if device_list:
        # 使用第一个设备的配置
        device_config_item = device_list[0]
        event_polling_enable = device_config_item.get("event_polling_enable", False)
        event_polling_interval = device_config_item.get("event_polling_interval", 5)
    
    if event_polling_enable:
        asyncio.create_task(udp_protocol.event_polling_task())
        logger = LogManager.get_device_logger(fsu_config["fsuname"], log_config, "UDP")
        logger.info(f"事件轮询任务已启动，轮询间隔: {event_polling_interval}秒")
    
    return transport, protocol

async def run_tcp_server(fsu_config: Dict[str, Any], device_config: Any, log_config: Dict[str, Any], performance_mode: bool):
    """运行TCP服务器
    
    Args:
        fsu_config: FSU配置
        device_config: 设备配置
        log_config: 日志配置
        performance_mode: 性能模式标志
    """
    loop = asyncio.get_running_loop()
    
    # 启动TCP服务器
    server = await loop.create_server(
        lambda: TCPProtocol(fsu_config, device_config, log_config, performance_mode),
        fsu_config["host"],
        fsu_config["port"]
    )

    logger = LogManager.get_device_logger(fsu_config["fsuname"], log_config, "TCP")
    logger.info(f"TCP服务已启动，监听端口: {fsu_config['port']}")
    
    return server

async def heartbeat_task(udp_protocol: UDPProtocol, interval: int):
    """心跳发送任务
    
    Args:
        udp_protocol: UDP协议实例
        interval: 心跳间隔（秒）
    """
    while True:
        await udp_protocol.send_heartbeat()
        await asyncio.sleep(interval)
