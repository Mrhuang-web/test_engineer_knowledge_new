#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志管理器
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any

class LogManager:
    """日志管理器"""
    
    def __init__(self, log_config: Dict[str, Any]):
        """初始化日志管理器
        
        Args:
            log_config: 日志配置
        """
        self.log_config = log_config
        self._init_logger()
    
    def _init_logger(self):
        """初始化日志系统"""
        # 获取日志配置
        level_str = self.log_config.get("level", "info").upper()
        level = getattr(logging, level_str, logging.INFO)
        log_dir = self.log_config.get("dir", "./logs")
        log_file = self.log_config.get("file", "system_%Y%m%d.log")
        
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
        # 生成日志文件名
        current_date = datetime.now().strftime("%Y%m%d")
        log_file = log_file.replace("%Y%m%d", current_date)
        log_file_path = os.path.join(log_dir, log_file)
        
        # 配置日志
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d %(message)s",
            handlers=[
                logging.FileHandler(log_file_path, encoding="utf-8"),
                logging.StreamHandler()
            ],
            force=True
        )
    
    @staticmethod
    def get_device_logger(fsuname: str, log_config: Dict[str, Any], protocol_type: str = "") -> logging.Logger:
        """获取设备日志记录器
        
        Args:
            fsuname: FSU名称
            log_config: 日志配置
            protocol_type: 协议类型（TCP/UDP）
        
        Returns:
            设备日志记录器
        """
        # 生成设备日志文件名
        log_dir = log_config.get("dir", "./logs")
        devices_log_dir = os.path.join(log_dir, "devices")
        os.makedirs(devices_log_dir, exist_ok=True)
        
        # 使用系统日期格式：年-月-日
        current_date = datetime.now().strftime("%Y%m%d")
        log_file_path = os.path.join(devices_log_dir, f"{fsuname}_{protocol_type}_{current_date}.log")
        
        # 创建设备日志记录器
        logger = logging.getLogger(f"device.{fsuname}")
        
        # 移除现有处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 从配置中获取日志级别
        level_str = log_config.get("level", "info").upper()
        level = getattr(logging, level_str, logging.INFO)
        logger.setLevel(level)
        
        # 阻止日志向上传播，避免重复打印
        logger.propagate = False
        
        # 添加文件处理器
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(message)s"))
        logger.addHandler(file_handler)
        
        # 添加流处理器，使用带行号的格式
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d %(message)s"))
        logger.addHandler(stream_handler)
        
        return logger
