#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志处理模块
"""

import logging
import json
import os
from datetime import datetime

class Logger:
    """日志处理类"""
    
    def __init__(self, log_dir="logs", log_level=logging.INFO):
        self.log_dir = log_dir
        self.log_level = log_level
        self.ensure_log_dir_exists()
        self.logger = self.setup_logger()
    
    def ensure_log_dir_exists(self):
        """确保日志目录存在"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def setup_logger(self):
        """设置日志记录器"""
        # 创建日志记录器
        logger = logging.getLogger("face_access_control")
        logger.setLevel(self.log_level)
        
        # 防止重复添加处理器
        if logger.handlers:
            return logger
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        # 创建文件处理器
        log_file = os.path.join(self.log_dir, f"access_control_{datetime.now().strftime('%Y-%m-%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(self.log_level)
        
        # 设置日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def debug(self, message):
        """调试级别日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """信息级别日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告级别日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """错误级别日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """严重错误级别日志"""
        self.logger.critical(message)
    
    def log_request(self, request_method, request_path, client_address, params=None):
        """记录请求日志"""
        params_str = json.dumps(params, ensure_ascii=False) if params else ""
        self.info(f"请求: {request_method} {request_path} 客户端: {client_address} 参数: {params_str}")
    
    def log_response(self, request_method, request_path, status_code, response_time):
        """记录响应日志"""
        self.info(f"响应: {request_method} {request_path} 状态码: {status_code} 响应时间: {response_time}ms")

# 初始化日志记录器
global_logger = Logger()
