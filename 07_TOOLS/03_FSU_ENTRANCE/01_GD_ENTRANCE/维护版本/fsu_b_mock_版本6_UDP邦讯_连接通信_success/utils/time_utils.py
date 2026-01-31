#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间函数工具类，支持在配置文件中使用${function_name(args)}$语法动态生成日期时间值
"""

import re
import inspect
from datetime import datetime
from typing import Any, Dict, List

class TimeFunctionUtils:
    """时间函数工具类"""
    
    # 函数调用正则表达式
    FUNCTION_PATTERN = re.compile(r'\$\{\s*([a-zA-Z0-9_]+)\s*(?:\(([^)]*)\))?\s*\}')
    
    def __init__(self):
        """初始化时间函数工具类"""
        self.functions = {
            'year': self._get_year,
            'month': self._get_month,
            'day': self._get_day,
            'week': self._get_week,
            'hour': self._get_hour,
            'minute': self._get_minute,
            'second': self._get_second,
            'datetime': self._get_datetime,
        }
    
    def evaluate(self, value: Any) -> Any:
        """评估值中的函数调用
        
        Args:
            value: 输入值，可以是字符串、字典、列表等
            
        Returns:
            评估后的结果
        """
        if isinstance(value, str):
            # 检查是否包含函数调用格式
            if '${' in value and '}$' in value:
                # 检查是否完全匹配函数调用格式
                match = self.FUNCTION_PATTERN.match(value)
                if match:
                    function_name = match.group(1)
                    args_str = match.group(2)
                    
                    # 解析参数，处理None的情况
                    args = []
                    if args_str:
                        args_str = args_str.strip()
                        if args_str:
                            args = [arg.strip() for arg in args_str.split(',') if arg.strip()]
                    
                    # 调用函数，只传递一个参数或不传递参数
                    if function_name in self.functions:
                        func = self.functions[function_name]
                        # 根据函数接受的参数数量决定传递多少参数
                        try:
                            # 尝试传递一个参数
                            if args:
                                return func(args[0])
                            else:
                                return func()
                        except TypeError:
                            # 如果失败，尝试不传递参数
                            try:
                                return func()
                            except TypeError:
                                # 如果仍然失败，返回原始值
                                return value
                else:
                    # 尝试替换字符串中的所有函数调用
                    def replace_func(m):
                        func_name = m.group(1)
                        func_args = m.group(2)
                        args = []
                        if func_args:
                            func_args = func_args.strip()
                            if func_args:
                                args = [arg.strip() for arg in func_args.split(',') if arg.strip()]
                        
                        if func_name in self.functions:
                            func = self.functions[func_name]
                            try:
                                if args:
                                    return func(args[0])
                                else:
                                    return func()
                            except TypeError:
                                try:
                                    return func()
                                except TypeError:
                                    return m.group(0)
                        return m.group(0)
                    
                    return self.FUNCTION_PATTERN.sub(replace_func, value)
        elif isinstance(value, dict):
            # 递归处理字典
            return {k: self.evaluate(v) for k, v in value.items()}
        elif isinstance(value, list):
            # 递归处理列表
            return [self.evaluate(item) for item in value]
        
        return value
    
    def _get_year(self, format: str = 'yy') -> str:
        """获取年份
        
        Args:
            format: 格式，默认'yy'（两位数年份），可选'yyyy'（四位数年份）
            
        Returns:
            年份字符串
        """
        now = datetime.now()
        # 移除可能的引号
        format = format.strip('"').strip("'")
        if format == 'yyyy':
            return f"{now.year:04d}"
        elif format == 'yy':
            return f"{now.year % 100:02d}"
        # 支持直接返回两位数年份
        return f"{now.year % 100:02d}"
    
    def _get_month(self) -> str:
        """获取月份（两位数）
        
        Returns:
            月份字符串
        """
        now = datetime.now()
        return f"{now.month:02d}"
    
    def _get_day(self) -> str:
        """获取日期（两位数）
        
        Returns:
            日期字符串
        """
        now = datetime.now()
        return f"{now.day:02d}"
    
    def _get_week(self) -> str:
        """获取星期（1-7，周一为1，周日为7）
        
        Returns:
            星期字符串
        """
        now = datetime.now()
        # weekday()返回0-6，周一为0，周日为6
        return f"{now.weekday() + 1:02d}"
    
    def _get_hour(self, format: str = 'hh') -> str:
        """获取小时（24小时制，两位数）
        
        Args:
            format: 格式，默认'hh'（两位数小时）
            
        Returns:
            小时字符串
        """
        now = datetime.now()
        return f"{now.hour:02d}"
    
    def _get_minute(self, format: str = 'mm') -> str:
        """获取分钟（两位数）
        
        Args:
            format: 格式，默认'mm'（两位数分钟）
            
        Returns:
            分钟字符串
        """
        now = datetime.now()
        return f"{now.minute:02d}"
    
    def _get_second(self, format: str = 'ss') -> str:
        """获取秒（两位数）
        
        Args:
            format: 格式，默认'ss'（两位数秒）
            
        Returns:
            秒字符串
        """
        now = datetime.now()
        return f"{now.second:02d}"
    
    def _get_datetime(self, format: str = 'yyMMddHHmmss') -> str:
        """获取完整日期时间
        
        Args:
            format: 格式，默认'yyMMddHHmmss'，支持datetime.strftime的格式
            
        Returns:
            日期时间字符串
        """
        now = datetime.now()
        # 处理默认格式
        if format == 'yyMMddHHmmss':
            return f"{now.year % 100:02d}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}{now.second:02d}"
        # 处理自定义格式，移除引号
        format = format.strip('"').strip("'")
        try:
            return now.strftime(format)
        except:
            return format
