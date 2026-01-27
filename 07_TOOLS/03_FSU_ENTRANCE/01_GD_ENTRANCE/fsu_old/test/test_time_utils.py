#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间函数工具类测试脚本
"""

import os
import sys
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.time_utils import TimeFunctionUtils

# 测试时间函数工具类
def test_time_utils():
    print("=== 测试时间函数工具类 ===")
    
    time_utils = TimeFunctionUtils()
    
    # 测试单个函数调用
    test_cases = [
        ("${year()}$", "两位数年份"),
        ("${year(yyyy)}$", "四位数年份"),
        ("${month()}$", "月份"),
        ("${day()}$", "日期"),
        ("${week()}$", "星期"),
        ("${hour()}$", "小时"),
        ("${minute()}$", "分钟"),
        ("${second()}$", "秒"),
        ("${datetime()}$", "默认格式日期时间"),
        ("${datetime(yy-MM-dd HH:mm:ss)}$", "自定义格式日期时间"),
    ]
    
    for expr, desc in test_cases:
        result = time_utils.evaluate(expr)
        print(f"{desc}: {expr} -> {result}")
    
    # 测试字典中的函数调用
    test_dict = {
        "year": "${year()}$",
        "month": "${month()}$",
        "day": "${day()}$",
        "time": {
            "hour": "${hour()}$",
            "minute": "${minute()}$",
            "second": "${second()}$"
        }
    }
    
    print("\n=== 测试字典中的时间函数 ===")
    result_dict = time_utils.evaluate(test_dict)
    print(f"原始字典: {test_dict}")
    print(f"评估结果: {result_dict}")
    
    # 测试列表中的函数调用
    test_list = [
        "${year()}$",
        "${month()}$",
        "${day()}$"
    ]
    
    print("\n=== 测试列表中的时间函数 ===")
    result_list = time_utils.evaluate(test_list)
    print(f"原始列表: {test_list}")
    print(f"评估结果: {result_list}")
    
    # 测试Bangsun规则文件中的时间函数
    print("\n=== 测试Bangsun规则文件中的时间函数 ===")
    bangsun_rule = {
        "108B": {
            "delay_ms": 500,
            "data": {
                "year": "${year()}$",
                "month": "${month()}$",
                "day": "${day()}$",
                "week": "${week()}$",
                "hour": "${hour()}$",
                "minute": "${minute()}$",
                "second": "${second()}$"
            }
        }
    }
    
    result_rule = time_utils.evaluate(bangsun_rule)
    print(f"原始规则: {bangsun_rule}")
    print(f"评估结果: {result_rule}")

if __name__ == "__main__":
    test_time_utils()
