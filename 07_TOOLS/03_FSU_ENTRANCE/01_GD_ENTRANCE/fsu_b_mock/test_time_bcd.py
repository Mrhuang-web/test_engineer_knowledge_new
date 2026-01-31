#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试时间BCD格式转换功能
"""

from datetime import datetime

def test_time_bcd_conversion():
    """测试时间BCD格式转换"""
    print("=== 测试时间BCD格式转换 ===")
    
    # 模拟当前时间
    now = datetime.now()
    print(f"当前时间: {now}")
    
    # 测试年份转换
    year_str = "2026"
    print(f"\n测试年份转换: {year_str}")
    
    # 正确的BCD转换：2026 -> 0x20 0x26
    bcd_year_high = ((int(year_str[0]) << 4) | int(year_str[1]))
    bcd_year_low = ((int(year_str[2]) << 4) | int(year_str[3]))
    
    print(f"BCD高位: 0x{bcd_year_high:02X}")
    print(f"BCD低位: 0x{bcd_year_low:02X}")
    print(f"BCD字节: {bcd_year_high:02X} {bcd_year_low:02X}")
    
    # 测试月份转换
    month = now.month
    print(f"\n测试月份转换: {month:02d}")
    bcd_month = ((month // 10) << 4) | (month % 10)
    print(f"BCD值: 0x{bcd_month:02X}")
    
    # 测试日期转换
    day = now.day
    print(f"\n测试日期转换: {day:02d}")
    bcd_day = ((day // 10) << 4) | (day % 10)
    print(f"BCD值: 0x{bcd_day:02X}")
    
    # 测试小时转换
    hour = now.hour
    print(f"\n测试小时转换: {hour:02d}")
    bcd_hour = ((hour // 10) << 4) | (hour % 10)
    print(f"BCD值: 0x{bcd_hour:02X}")
    
    # 测试分钟转换
    minute = now.minute
    print(f"\n测试分钟转换: {minute:02d}")
    bcd_minute = ((minute // 10) << 4) | (minute % 10)
    print(f"BCD值: 0x{bcd_minute:02X}")
    
    # 测试秒转换
    second = now.second
    print(f"\n测试秒转换: {second:02d}")
    bcd_second = ((second // 10) << 4) | (second % 10)
    print(f"BCD值: 0x{bcd_second:02X}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_time_bcd_conversion()
