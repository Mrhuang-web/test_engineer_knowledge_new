#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试所有协议解析器的导入功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试所有解析器的导入
modules_to_test = [
    "b_interface_parser",
    "bangxun_old_parser",
    "yingjia_mj200_parser",
    "yaa_parser",
    "liwei_parser",
    "haineng_parser",
    "vertiv_parser",
    "bangxun_new_parser",
    "tidi_es2200_parser",
    "gaoxin_260r_parser",
    "gaoxin_300r_parser",
    "zhongda_chd805_parser"
]

print("=== 测试所有协议解析器的导入功能 ===")

success_count = 0
failure_count = 0

for module_name in modules_to_test:
    try:
        # 动态导入模块
        __import__(module_name)
        print(f"✅ 成功导入：{module_name}")
        success_count += 1
    except Exception as e:
        print(f"❌ 导入失败：{module_name}")
        print(f"   错误信息：{e}")
        failure_count += 1

print("\n=== 测试结果 ===")
print(f"总模块数量：{len(modules_to_test)}")
print(f"成功导入：{success_count}")
print(f"导入失败：{failure_count}")

if failure_count == 0:
    print("🎉 所有模块均成功导入！")
else:
    print("⚠️  部分模块导入失败，请检查错误信息！")
