#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSU Mock Server 主程序
支持UDP和TCP协议，根据配置文件动态启动服务
"""

import os
import logging
import asyncio
import multiprocessing
from typing import Dict, Any, List

# 导入日志管理器
from utils.log_manager import LogManager

# 导入配置管理器
from utils.config_manager import FSUConfig, DeviceConfig

# 导入服务器管理器
from server.server_manager import run_udp_server, run_tcp_server

async def run_fsu_services(fsu_list: List[Dict[str, Any]], fsu_config: Any, log_config: Dict[str, Any], performance_mode: bool):
    """运行一组FSU服务
    
    Args:
        fsu_list: FSU服务列表
        fsu_config: FSU配置对象
        log_config: 日志配置
        performance_mode: 性能模式标志
    """
    # 启动所有FSU服务
    tasks = []
    for fsu in fsu_list:
        try:
            # 加载设备配置
            device_config = DeviceConfig(fsu["config_dir"])
            
            if fsu["protocol_type"] == "udp":
                # 启动UDP服务器
                logging.debug(f"启动UDP服务: {fsu['fsuname']}, 端口: {fsu['port']}")
                # 获取SC IoT中心配置
                sc_iot_center = fsu_config.config.get("sc_iot_center", {})
                sc_iot_config = {
                    "host": sc_iot_center.get("host"),
                    "port": sc_iot_center.get("port")
                }
                task = asyncio.create_task(run_udp_server(fsu, device_config, log_config, performance_mode, sc_iot_config))
                tasks.append(task)
            elif fsu["protocol_type"] == "tcp":
                # 启动TCP服务器
                logging.debug(f"启动TCP服务: {fsu['fsuname']}, 端口: {fsu['port']}")
                task = asyncio.create_task(run_tcp_server(fsu, device_config, log_config, performance_mode))
                tasks.append(task)
        except Exception as e:
            logging.error(f"启动{fsu['protocol_type'].upper()}服务失败: {fsu['fsuname']}, 错误: {e}")
    
    # 等待所有服务启动完成
    if tasks:
        await asyncio.gather(*tasks)
    
    # 保持运行
    logging.debug(f"进程 {os.getpid()} 已启动 {len(fsu_list)} 个服务")
    await asyncio.Event().wait()

def process_main(fsu_list: List[Dict[str, Any]], fsu_config: Any, log_config: Dict[str, Any], performance_mode: bool):
    """进程主函数
    
    Args:
        fsu_list: 分配给当前进程的FSU服务列表
        fsu_config: FSU配置对象
        log_config: 日志配置
        performance_mode: 性能模式标志
    """
    # 每个进程重新初始化日志，使用进程ID区分
    LogManager(log_config)
    logging.debug(f"进程 {os.getpid()} 启动，管理 {len(fsu_list)} 个服务")
    
    # 运行服务
    asyncio.run(run_fsu_services(fsu_list, fsu_config, log_config, performance_mode))

async def main():
    """主程序入口
    """
    # 初始化配置
    fsu_config = FSUConfig()
    log_config = fsu_config.get_log_config()
    performance_config = fsu_config.get_performance_config()
    performance_mode = performance_config.get("enabled", False)
    
    # 初始化日志
    LogManager(log_config)
    
    # 获取FSU列表
    fsu_list = fsu_config.get_fsu_list()
    if not fsu_list:
        logging.error("没有可用的FSU配置")
        return
    
    # 获取CPU核心数
    cpu_count = multiprocessing.cpu_count()
    logging.info(f"系统CPU核心数: {cpu_count}")
    
    # 根据CPU核心数分配FSU服务
    # 计算每个进程分配的服务数量
    services_per_process = len(fsu_list) // cpu_count
    remainder = len(fsu_list) % cpu_count
    
    # 分配FSU服务到不同的进程
    process_services = []
    start = 0
    for i in range(cpu_count):
        end = start + services_per_process
        if i < remainder:
            end += 1
        if start < end:
            process_services.append(fsu_list[start:end])
            start = end
    
    # 创建进程
    processes = []
    for services in process_services:
        p = multiprocessing.Process(
            target=process_main,
            args=(services, fsu_config, log_config, performance_mode)
        )
        processes.append(p)
        p.start()
    
    logging.debug(f"已启动 {len(processes)} 个进程")
    
    # 等待所有进程结束
    for p in processes:
        p.join()

if __name__ == "__main__":
    try:
        # 使用多进程模式
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("服务已停止")
    except Exception as e:
        logging.error(f"服务运行失败: {e}")
        raise
