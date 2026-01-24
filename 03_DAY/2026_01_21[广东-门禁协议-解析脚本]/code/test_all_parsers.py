#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有协议解析器是否能正常加载
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试所有解析器的导入和实例化
parsers_to_test = [
    ("B接口透传协议", "b_interface_parser", "BInterfaceParser"),
    ("邦讯门禁控制器协议（旧版）", "bangxun_old_parser", "BangxunOldParser"),
    ("盈佳MJ200门禁协议", "yingjia_mj200_parser", "YingJiaMJ200Parser"),
    ("亚奥门禁控制器协议", "yaa_parser", "YaaoParser"),
    ("力维ACUC3.0门禁控制器协议", "liwei_parser", "LiWeiParser"),
    ("海能门禁控制器协议", "haineng_parser", "HainengParser"),
    ("维谛ES2000门禁控制器协议", "vertiv_parser", "VertivParser"),
    ("邦讯门禁控制器协议（新版）", "bangxun_new_parser", "BangxunNewParser"),
    ("钛迪ES2200门禁控制器协议", "tidi_es2200_parser", "TidiES2200Parser"),
    ("高新兴260R门禁控制器协议", "gaoxin_260r_parser", "Gaoxin260RParser"),
    ("高新兴300R门禁控制器协议", "gaoxin_300r_parser", "Gaoxin300RParser"),
    ("中达CHD805门禁控制器协议", "zhongda_chd805_parser", "ZhongdaCHD805Parser")
]

print("=== 测试所有协议解析器是否能正常加载 ===")

success_count = 0
failure_count = 0

for parser_name, module_name, class_name in parsers_to_test:
    try:
        # 动态导入模块
        module = __import__(module_name)
        # 获取类
        parser_class = getattr(module, class_name)
        # 实例化
        parser = parser_class()
        print(f"✅ 成功加载：{parser_name}")
        success_count += 1
    except Exception as e:
        print(f"❌ 加载失败：{parser_name}")
        print(f"   错误信息：{e}")
        failure_count += 1

print("\n=== 测试结果 ===")
print(f"总解析器数量：{len(parsers_to_test)}")
print(f"成功加载：{success_count}")
print(f"加载失败：{failure_count}")

if failure_count == 0:
    print("🎉 所有解析器均成功加载！")
else:
    print("⚠️  部分解析器加载失败，请检查错误信息！")
