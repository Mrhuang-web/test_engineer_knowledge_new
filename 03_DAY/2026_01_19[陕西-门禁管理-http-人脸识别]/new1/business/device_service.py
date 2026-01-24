#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备管理业务逻辑模块
"""

from data.data_store import JSONDataStore
from business.logger import global_logger

class DeviceService:
    """设备管理业务逻辑类"""
    
    def __init__(self):
        self.data_store = JSONDataStore()
        self.logger = global_logger
    
    def verify_password(self, password):
        """验证设备密码"""
        return password == self.data_store.get_password()
    
    def set_password(self, old_pass, new_pass):
        """设置设备密码"""
        if not self.verify_password(old_pass):
            self.logger.warning(f"密码设置失败：旧密码错误")
            return False, "旧密码错误"
        
        if not new_pass:
            self.logger.warning(f"密码设置失败：新密码不能为空")
            return False, "新密码不能为空"
        
        success = self.data_store.set_password(new_pass)
        if success:
            self.logger.info(f"密码设置成功：{new_pass}")
            return True, "密码设置成功"
        else:
            self.logger.error(f"密码设置失败：保存失败")
            return False, "保存失败"
    
    def get_device_info(self):
        """获取设备信息"""
        self.logger.info(f"获取设备信息")
        return self.data_store.get_device_info()
    
    def open_door(self):
        """远程开门"""
        self.logger.info(f"远程开门操作")
        # 模拟开门操作
        return True, "开门成功"
    
    def get_door_sensor(self):
        """获取门磁状态"""
        status = self.data_store.get_door_sensor()
        self.logger.info(f"获取门磁状态：{status}")
        return status
    
    def set_callback(self, callback_type, url):
        """设置回调地址"""
        self.logger.info(f"设置回调地址：{callback_type} -> {url}")
        success = self.data_store.set_callback(callback_type, url)
        if success:
            return True, "设置成功"
        else:
            return False, "设置失败"
    
    def restart_device(self):
        """重启设备"""
        self.logger.info(f"重启设备操作")
        return True, "操作成功，设备即将重启"
    
    def set_time(self):
        """设置时间"""
        self.logger.info(f"设置时间操作")
        return True, "设置成功"
    
    def set_language(self, language_type):
        """设置语言"""
        self.logger.info(f"设置语言：{language_type}")
        return True, "设置成功"
    
    def set_timezone(self, timezone):
        """设置时区"""
        self.logger.info(f"设置时区：{timezone}")
        return True, "设置成功"
    
    def set_signal_input(self, config):
        """设置信号输入"""
        self.logger.info(f"设置信号输入：{config}")
        return True, "设置成功"
    
    def meet_warn_set(self, params):
        """会议与关门告警设置"""
        self.logger.info(f"会议与关门告警设置：{params}")
        return True, "设置成功"
    
    def card_info_set(self, params):
        """卡片设置"""
        self.logger.info(f"卡片设置：{params}")
        return True, "设置成功"
