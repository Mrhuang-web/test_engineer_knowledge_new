#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础协议类，包含TCP和UDP共用的方法
"""

import os
import copy
import re
from typing import Dict, Any, Optional



class BaseProtocol:
    """基础协议类，包含TCP和UDP共用的方法"""
    
    _REQUEST_FIELD_PLACEHOLDER_RE = re.compile(r"^#\{(.+?)\}#$")
    
    def __init__(self):
        """初始化基础协议类"""
        # 这些属性会在子类中被赋值
        self.fsu_config = None
        self.device_config = None
        self.logger = None
    
    def load_protocols(self):
        """加载设备协议模板
        
        Returns:
            设备协议字典
        """
        protocols = {}
        for device in self.device_config.get_device_list():
            protocol_template = device.get("protocol_template", "")
            if protocol_template:
                # 加载协议模板
                protocol_config = self.device_config.load_protocol_template(protocol_template)
                # 加载规则文件，分别存储到fsu_rule和default_rule对象
                all_rules_obj = {
                    "fsu_rule": {},
                    "default_rule": {}
                }
                
                # 处理rule_file_list配置
                rule_file_list = protocol_config.get("rule_file_list", [])
                for rule_file in rule_file_list:
                    # 确保rule_file是正确的字符串，处理可能的空值
                    if not rule_file:
                        continue
                    # 如果rule_file是相对路径，添加配置目录前缀
                    if not os.path.isabs(rule_file):
                        # 手动拼接路径，确保添加斜杠
                        if self.device_config.config_dir.endswith(os.sep) or rule_file.startswith(os.sep):
                            full_rule_file = self.device_config.config_dir + rule_file
                        else:
                            full_rule_file = self.device_config.config_dir + os.sep + rule_file
                        # 处理路径中的混合分隔符
                        full_rule_file = os.path.normpath(full_rule_file)
                    else:
                        full_rule_file = rule_file
                    # 从协议配置中获取dynamic_time_enabled配置
                    protocol = protocol_config.get("protocol", {})
                    dynamic_time_enabled = protocol.get("dynamic_time_enabled", False)
                    rules_obj = self.device_config.load_rules_with_separate_objects(full_rule_file, self.fsu_config.get("fsuid", ""), dynamic_time_enabled)
                    # 合并规则对象
                    all_rules_obj["fsu_rule"].update(rules_obj["fsu_rule"])
                    all_rules_obj["default_rule"].update(rules_obj["default_rule"])
                    
                if all_rules_obj["fsu_rule"] or all_rules_obj["default_rule"]:
                    protocol_config["rules_obj"] = all_rules_obj
                # 使用设备索引作为键，确保至少有一个有效的键
                protocols[str(len(protocols))] = protocol_config
        # self.logger.debug(f"加载的设备协议模板: {protocols}")
        return protocols
    
    def reload_protocols(self):
        """重新加载设备协议模板和规则
        
        Returns:
            如果重新加载成功返回True，否则返回False
        """
        try:
            # 重新加载设备配置
            if self.device_config.reload_config():
                # 重新加载协议和规则
                self.device_protocols = self.load_protocols()
                self.logger.info("设备协议配置已热加载")
                return True
            return False
        except Exception as e:
            self.logger.error(f"重新加载协议配置失败: {e}")
            return False

    def _render_rule_data_placeholders(self, rule: Dict[str, Any], parsed_result: Dict[str, Any]) -> Dict[str, Any]:
        rendered_rule: Dict[str, Any] = copy.deepcopy(rule)

        data = rendered_rule.get("data")
        if isinstance(data, (dict, list, str)):
            rendered_rule["data"] = self._render_placeholders(value=data, parsed_result=parsed_result)

        return rendered_rule

    def _render_placeholders(self, value: Any, parsed_result: Dict[str, Any]) -> Any:
        if isinstance(value, dict):
            return {k: self._render_placeholders(v, parsed_result) for k, v in value.items()}
        if isinstance(value, list):
            return [self._render_placeholders(v, parsed_result) for v in value]
        if isinstance(value, str):
            match = self._REQUEST_FIELD_PLACEHOLDER_RE.match(value)
            if not match:
                return value
            key_path = match.group(1).strip()
            resolved = self._resolve_request_field(parsed_result, key_path)
            return "" if resolved is None else resolved
        return value

    def _resolve_request_field(self, parsed_result: Dict[str, Any], key_path: str) -> Optional[Any]:
        if not key_path:
            return None

        through_pdu = parsed_result.get("through_pdu", {})
        through_sdu = parsed_result.get("through_sdu", {})
        legacy_through = parsed_result.get("透传数据", {})
        legacy_frame = parsed_result.get("数据帧", {})

        sources: Dict[str, Any] = {
            "through_pdu": through_pdu,
            "through_sdu": through_sdu,
            "透传数据": legacy_through,
            "数据帧": legacy_frame,
        }

        parts = [p for p in key_path.split(".") if p]
        if not parts:
            return None

        if parts[0] in sources:
            current: Any = sources.get(parts[0], {})
            parts = parts[1:]
        else:
            merged: Dict[str, Any] = {}
            if isinstance(through_pdu, dict):
                merged.update(through_pdu)
            if isinstance(through_sdu, dict):
                merged.update(through_sdu)
            if isinstance(legacy_through, dict):
                merged.update(legacy_through)
            if isinstance(legacy_frame, dict):
                merged.update(legacy_frame)
            current = merged

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current
    
    def _generate_response(self, protocol_config: Dict[str, Any], parsed_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成响应数据
        
        Args:
            protocol_config: 协议配置
            parsed_result: 解析结果
        
        Returns:
            完整的规则信息，包括data、delay_ms、timeout等字段
        """
        # 获取数据帧类型
        # 优先从透传数据（pdu_left）中查找，匹配不到再到数据帧（data_frame）中查找
        # 取请求的协议数据单元
        request_through_data = parsed_result.get("through_pdu", {})
        # 取请求包的 数据帧
        request_through_data_frame = parsed_result.get("through_sdu", {})


        data_frame_type_flag = protocol_config.get("protocol", {}).get("data_frame_type_flag", "data_frame_type")
        vendor = protocol_config.get("vendor", "")
        
        # 处理data_frame_type_flag是列表的情况
        if isinstance(data_frame_type_flag, list):
            # 从请求包收集所有数据
            all_data = {**request_through_data, **request_through_data_frame}

            # 生成数据帧类型标识
            data_frame_type_parts = []
            for flag in data_frame_type_flag:
                if flag in all_data:
                    value = all_data[flag]
                    # 确保value是字符串类型
                    if isinstance(value, list):
                        # 如果是列表，取第一个元素并转换为字符串
                        if value:
                            first_value = value[0]
                            if isinstance(first_value, int):
                                data_frame_type_parts.append(f"{first_value:02X}")
                            else:
                                data_frame_type_parts.append(str(first_value))
                    elif isinstance(value, int):
                        # 如果是数字，转换为十六进制字符串
                        data_frame_type_parts.append(f"{value:02X}")
                    elif isinstance(value, bytes):
                        # 如果是字节，转换为十六进制字符串
                        data_frame_type_parts.append(value.hex().upper())
                    else:
                        # 其他类型直接转换为字符串
                        data_frame_type_parts.append(str(value))
            # 使用下划线连接各部分（用于日志）
            data_frame_type = "".join(data_frame_type_parts)
            # 直接生成不带下划线的规则键（用于匹配规则）
            actual_type = data_frame_type
        else:
            # 处理字符串类型的data_frame_type_flag
            data_frame_type = request_through_data.get(data_frame_type_flag, "")
            # 如果透传数据中没有，从数据帧中查找
            if not data_frame_type and data_frame_type_flag in request_through_data_frame:
                data_frame_type = request_through_data_frame[data_frame_type_flag]
            # 直接使用数据帧类型作为规则键，移除可能存在的下划线
            actual_type = data_frame_type
        
        self.logger.debug(f"返回规则中的数据帧类型: {actual_type}")
        
        # 调试输出数据帧类型
        self.logger.debug(f"生成的数据帧类型: {data_frame_type}, 返回规则中的数据帧类型: {actual_type}")
        
        # 获取规则对象
        rules_obj = protocol_config.get("rules_obj", {"fsu_rule": {}, "default_rule": {}})
        
        try:
            # 根据data_frame_type匹配规则
            frame_rule = self.device_config.match_rule_by_data_frame_type(rules_obj, actual_type)
            if isinstance(frame_rule, dict):
                # 渲染请求字段占位符
                rendered_rule = self._render_rule_data_placeholders(frame_rule, parsed_result)
                
                # 检查是否需要动态评估时间函数
                # 1. 检查性能模式，性能模式下关闭动态时间评估
                performance_mode = getattr(self, 'performance_mode', False)
                
                # 2. 检查协议配置中的动态时间开关
                dynamic_time_enabled = protocol_config.get("protocol", {}).get("dynamic_time_enabled", False)
                
                # 3. 综合判断是否需要动态评估
                should_evaluate_time = dynamic_time_enabled and not performance_mode
                
                if should_evaluate_time:
                    # 评估时间函数
                    from utils.time_utils import TimeFunctionUtils
                    time_utils = TimeFunctionUtils()
                    data = rendered_rule.get("data", {})
                    if data:
                        rendered_rule["data"] = time_utils.evaluate(data)
                        # 检查logger是否存在
                        if hasattr(self, 'logger') and self.logger is not None and hasattr(self.logger, 'debug'):
                            self.logger.debug(f"动态评估时间函数，data_frame_type={actual_type}, 结果={rendered_rule['data']}")
                else:
                    # 检查logger是否存在
                    if hasattr(self, 'logger') and self.logger is not None and hasattr(self.logger, 'debug'):
                        self.logger.debug(f"跳过动态评估时间函数，data_frame_type={actual_type}, performance_mode={performance_mode}, is_event_type={is_event_type}, dynamic_time_enabled={dynamic_time_enabled}")
                return rendered_rule
            return frame_rule
        except Exception as e:
            # 异常处理，使用空规则
            self.logger.error(f"匹配规则失败: {e}")
            return {"data": {}}
