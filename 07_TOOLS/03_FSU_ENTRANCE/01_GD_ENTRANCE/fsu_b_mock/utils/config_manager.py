#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理工具类，负责加载和管理系统配置、设备配置、协议模板和规则文件
"""

import os
import json
import logging
import time
from typing import Dict, Any, List, Optional

# 导入时间函数工具类
from utils.time_utils import TimeFunctionUtils

class FSUConfig:
    """FSU配置管理"""
    
    def __init__(self, config_path: str = "./config/sys_config.json"):
        """初始化配置管理
        
        Args:
            config_path: 系统配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_config()
        self._last_modified = self._get_last_modified_time()
        
    def _get_last_modified_time(self) -> float:
        """获取配置文件最后修改时间
        
        Returns:
            最后修改时间（时间戳）
        """
        try:
            return os.path.getmtime(self.config_path)
        except Exception as e:
            logging.error(f"获取配置文件修改时间失败: {e}")
            return 0.0
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件
        
        Returns:
            配置字典
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")
            raise
    
    def check_for_updates(self) -> bool:
        """检查配置文件是否更新
        
        Returns:
            如果配置文件已更新返回True，否则返回False
        """
        current_mtime = self._get_last_modified_time()
        if current_mtime > self._last_modified:
            return True
        return False
    
    def reload_config(self) -> bool:
        """重新加载配置文件
        
        Returns:
            如果重新加载成功返回True，否则返回False
        """
        try:
            self.config = self._load_config()
            self._last_modified = self._get_last_modified_time()
            logging.info(f"配置文件已更新: {self.config_path}")
            return True
        except Exception as e:
            logging.error(f"重新加载配置文件失败: {e}")
            return False
    
    def get_log_config(self) -> Dict[str, Any]:
        """获取日志配置
        
        Returns:
            日志配置字典
        """
        return self.config.get("log", {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """获取性能配置
        
        Returns:
            性能配置字典
        """
        return self.config.get("performance", {})
    
    def get_fsu_list(self) -> List[Dict[str, Any]]:
        """获取FSU列表
        
        Returns:
            FSU配置列表
        """
        return self.config.get("fsu_list", [])
    
    def get_sc_iot_center_config(self) -> Dict[str, Any]:
        """获取SC IoT中心配置
        
        Returns:
            SC IoT中心配置字典
        """
        sc_iot_center = self.config.get("sc_iot_center", {})
        return {
            "host": sc_iot_center.get("host"),
            "port": sc_iot_center.get("port")
        }

class DeviceConfig:
    """设备配置管理"""
    
    def __init__(self, config_dir: str):
        """初始化设备配置管理
        
        Args:
            config_dir: 设备配置目录
        """
        self.config_dir = config_dir
        self.devices = self._load_devices()
        self._last_modified = {
            "devices": self._get_file_mtime("fsu_devices.json"),
            "protocols": {},  # 记录协议模板的修改时间
            "rules": {}       # 记录规则文件的修改时间
        }
    
    def _get_file_mtime(self, filename: str) -> float:
        """获取文件最后修改时间
        
        Args:
            filename: 文件名
        
        Returns:
            最后修改时间（时间戳）
        """
        try:
            file_path = os.path.join(self.config_dir, filename)
            return os.path.getmtime(file_path)
        except Exception as e:
            logging.error(f"获取文件修改时间失败: {filename}, 错误: {e}")
            return 0.0
    
    def _load_devices(self) -> Dict[str, Any]:
        """加载设备配置
        
        Returns:
            设备配置字典
        """
        devices_path = os.path.join(self.config_dir, "fsu_devices.json")
        try:
            with open(devices_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载设备配置失败: {e}")
            return {}
    
    def check_for_updates(self) -> bool:
        """检查设备配置是否更新
        
        Returns:
            如果配置已更新返回True，否则返回False
        """
        # 检查设备配置文件
        devices_mtime = self._get_file_mtime("fsu_devices.json")
        if devices_mtime > self._last_modified["devices"]:
            return True
        
        # 检查所有协议模板和规则文件
        device_list = self.get_device_list()
        for device in device_list:
            protocol_template_path = device.get("protocol_template", "")
            if protocol_template_path:
                # 检查协议模板文件本身
                template_mtime = self._get_file_mtime(protocol_template_path)
                if protocol_template_path not in self._last_modified["protocols"] or template_mtime > self._last_modified["protocols"][protocol_template_path]:
                    return True
                
                # 加载协议模板，检查其中的规则文件
                try:
                    protocol_template = self.load_protocol_template(protocol_template_path)
                    rule_file_list = protocol_template.get("rule_file_list", [])
                    
                    # 检查规则文件
                    for rule_file in rule_file_list:
                        rule_mtime = self._get_file_mtime(rule_file)
                        if rule_file not in self._last_modified["rules"] or rule_mtime > self._last_modified["rules"][rule_file]:
                            return True
                except Exception as e:
                    logging.error(f"检查协议模板更新失败: {protocol_template_path}, 错误: {e}")
        
        return False
    
    def reload_config(self) -> bool:
        """重新加载设备配置
        
        Returns:
            如果重新加载成功返回True，否则返回False
        """
        try:
            # 重新加载设备配置
            self.devices = self._load_devices()
            self._last_modified["devices"] = self._get_file_mtime("fsu_devices.json")
            
            # 更新所有协议模板和规则文件的修改时间记录
            device_list = self.get_device_list()
            for device in device_list:
                protocol_template_path = device.get("protocol_template", "")
                if protocol_template_path:
                    # 更新协议模板文件的修改时间
                    template_mtime = self._get_file_mtime(protocol_template_path)
                    self._last_modified["protocols"][protocol_template_path] = template_mtime
                    
                    # 加载协议模板，获取规则文件列表
                    protocol_template = self.load_protocol_template(protocol_template_path)
                    rule_file_list = protocol_template.get("rule_file_list", [])
                    
                    # 更新规则文件的修改时间
                    for rule_file in rule_file_list:
                        rule_mtime = self._get_file_mtime(rule_file)
                        self._last_modified["rules"][rule_file] = rule_mtime
            
            logging.info(f"设备配置已更新: {self.config_dir}")
            return True
        except Exception as e:
            logging.error(f"重新加载设备配置失败: {e}")
            return False
    
    def get_device_list(self) -> List[Dict[str, Any]]:
        """获取设备列表
        
        Returns:
            设备列表
        """
        return self.devices.get("device_list", [])
    
    def load_protocol_template(self, template_path: str) -> Dict[str, Any]:
        """加载协议模板
        
        Args:
            template_path: 协议模板路径
        
        Returns:
            协议模板字典
        """
        full_path = os.path.join(self.config_dir, template_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载协议模板失败: {e}")
            return {}
    
    def load_rules_with_separate_objects(self, rule_path: str, fsuid: str = "", dynamic_time_enabled: bool = False) -> Dict[str, Dict[str, Any]]:
        """加载规则文件，分别存储到fsu_rule和default_rule对象
        
        Args:
            rule_path: 规则文件路径
            fsuid: FSU设备ID
            dynamic_time_enabled: 是否启用动态时间评估
        
        Returns:
            包含fsu_rule和default_rule的字典
        """
        # 初始化规则对象
        fsu_rule = {}
        default_rule = {}
        
        # 初始化时间函数工具类
        time_utils = TimeFunctionUtils()
        
        # 如果rule_path是目录路径，直接使用它作为规则目录
        if os.path.isdir(rule_path):
            rule_dir = rule_path
        # 否则，取其所在目录作为规则目录
        else:
            rule_dir = os.path.dirname(rule_path)
        
        # 1. 尝试加载fsuid.json到fsu_rule对象
        if fsuid:
            fsuid_rule_path = os.path.join(rule_dir, f"{fsuid}.json")
            try:
                with open(fsuid_rule_path, "r", encoding="utf-8") as f:
                    fsu_rule = json.load(f)
                    # 根据dynamic_time_enabled决定是否评估时间函数
                    if not dynamic_time_enabled:
                        fsu_rule = time_utils.evaluate(fsu_rule)
                    logging.debug(f"通过fsuid: {fsuid}，匹配到{fsuid_rule_path}文件，加载到fsu_rule对象")
            except Exception:
                logging.debug(f"未找到fsuid: {fsuid}对应的规则文件，跳过加载fsu_rule对象")
        
        # 2. 尝试加载default.json到default_rule对象
        default_rule_path = os.path.join(rule_dir, "default.json")
        try:
            with open(default_rule_path, "r", encoding="utf-8") as f:
                default_rule = json.load(f)
                # 根据dynamic_time_enabled决定是否评估时间函数
                if not dynamic_time_enabled:
                    default_rule = time_utils.evaluate(default_rule)
                logging.debug(f"加载{default_rule_path}文件到default_rule对象")
        except Exception:
            logging.error(f"未找到{default_rule_path}文件，default_rule对象为空")
        
        # 3. 尝试加载event.json到default_rule对象
        event_rule_path = os.path.join(rule_dir, "event.json")
        try:
            with open(event_rule_path, "r", encoding="utf-8") as f:
                event_rule = json.load(f)
                # 根据dynamic_time_enabled决定是否评估时间函数
                if not dynamic_time_enabled:
                    event_rule = time_utils.evaluate(event_rule)
                # 合并event.json到default_rule，event配置优先级高于default
                default_rule.update(event_rule)
                logging.debug(f"加载{event_rule_path}文件，合并到default_rule对象")
        except Exception:
            logging.debug(f"未找到{event_rule_path}文件，跳过加载event_rule对象")
        
        return {
            "fsu_rule": fsu_rule,
            "default_rule": default_rule
        }
    
    def match_rule_by_data_frame_type(self, rules_obj: Dict[str, Dict[str, Any]], data_frame_type: str) -> Dict[str, Any]:
        """根据data_frame_type匹配规则
        
        Args:
            rules_obj: 包含fsu_rule和default_rule的字典
            data_frame_type: 数据帧类型
        
        Returns:
            匹配到的规则字典
        
        Raises:
            Exception: 未找到匹配的规则
        """
        fsu_rule = rules_obj.get("fsu_rule", {})
        default_rule = rules_obj.get("default_rule", {})
        
        # 1. 优先从fsu_rule中匹配
        if data_frame_type in fsu_rule:
            logging.info(f"从fsu_rule中匹配到data_frame_type: {data_frame_type}的规则")
            return fsu_rule[data_frame_type]
        
        # 2. 从default_rule中匹配
        if data_frame_type in default_rule:
            logging.info(f"从default_rule中匹配到data_frame_type: {data_frame_type}的规则")
            return default_rule[data_frame_type]
        
        # 3. 未匹配到规则，抛出异常
        logging.error(f"未找到data_frame_type: {data_frame_type}的规则")
        raise Exception(f"未找到data_frame_type: {data_frame_type}的规则")
    
    def load_rule_file(self, rule_path: str, fsuid: str = "") -> Dict[str, Any]:
        """加载规则文件
        
        Args:
            rule_path: 规则文件路径
            fsuid: FSU设备ID
        
        Returns:
            规则文件字典
        """
        # 兼容旧版本，使用原有逻辑
        # 解析规则文件目录和文件名
        rule_dir = os.path.dirname(rule_path)
        base_name = os.path.basename(rule_path)
        
        # 加载所有规则文件
        all_rules = []
        
        # 1. 尝试加载default.json
        default_rule_path = os.path.join(rule_dir, "default.json")
        full_path = os.path.join(self.config_dir, default_rule_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                all_rules.append(json.load(f))
        except Exception:
            pass
        
        # 2. 尝试加载原始规则文件
        full_path = os.path.join(self.config_dir, rule_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                all_rules.append(json.load(f))
        except Exception:
            pass
        
        # 3. 优先尝试加载fsuid.json，放在最后，以便覆盖前面的规则
        if fsuid:
            fsuid_rule_path = os.path.join(rule_dir, f"{fsuid}.json")
            full_path = os.path.join(self.config_dir, fsuid_rule_path)
            logging.info(f"通过fsuid: {fsuid}，匹配到{fsuid_rule_path}文件，加载fsu返回规则文件文件")
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    all_rules.append(json.load(f))
            except Exception:
                pass
        
        # 合并规则，后面的规则覆盖前面的规则
        merged_rules = {}
        for rules in all_rules:
            merged_rules.update(rules)
        
        return merged_rules
