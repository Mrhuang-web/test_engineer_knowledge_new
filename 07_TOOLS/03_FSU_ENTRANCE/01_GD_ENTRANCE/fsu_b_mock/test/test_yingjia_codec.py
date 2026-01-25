#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试盈佳协议编解码器
"""

import os
import sys
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import logging
from codec.through_data_codec import ThroughDataCodec

# 配置日志，设置为DEBUG级别
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 设置编解码器日志级别
logging.getLogger('codec.through_data').setLevel(logging.DEBUG)

# 读取盈佳协议配置
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'yingjia', 'yingjia.json')
with open(config_path, 'r', encoding='utf-8') as f:
    yingjia_config = json.load(f)

# 创建编解码器实例
codec = ThroughDataCodec(yingjia_config)

# 测试数据帧类型生成
print("=== 测试数据帧类型生成 ===")
pdu_left_result = {
    "cid2": "48",
    "ver": "10",
    "adr": "FD"
}
data_frame_result = {
    "group": "F0",
    "type": "E0",
    "password": "0000000000"
}

data_frame_type = codec._generate_data_frame_type(pdu_left_result, data_frame_result)
print(f"生成的数据帧类型: {data_frame_type}")
assert data_frame_type == "48_F0_E0", f"期望 '48_F0_E0', 实际 '{data_frame_type}'"
print("✓ 数据帧类型生成测试通过")

# 测试不同的cid2值
pdu_left_result["cid2"] = "49"
data_frame_result["group"] = "F1"
data_frame_result["type"] = "E1"
data_frame_type = codec._generate_data_frame_type(pdu_left_result, data_frame_result)
print(f"生成的数据帧类型: {data_frame_type}")
assert data_frame_type == "49_F1_E1", f"期望 '49_F1_E1', 实际 '{data_frame_type}'"
print("✓ 不同cid2值测试通过")

# 测试编码字段
print("\n=== 测试编码字段 ===")

# 模拟解析数据
parsed_data = {
    "透传数据": {
        "cid2": "48",
        "ver": "10",
        "adr": "FD"
    },
    "数据帧": {
        "group": "F0",
        "type": "E0",
        "password": "0000000000"
    }
}

response_data = {}

# 测试 {pdu_left}_{cid2} 格式的字段名
field = {
    "name": "{pdu_left}_{cid2}",
    "length": 1,
    "type": "hex",
    "value": "00"
}

encoded_field = codec._encode_field(field, parsed_data, response_data)
print(f"编码字段 {field['name']}: {encoded_field.hex().upper()}")
# 期望的值应该是从透传数据中获取的cid2值，即0x48
assert encoded_field.hex().upper() == "48", f"期望 '48', 实际 '{encoded_field.hex().upper()}'"
print("✓ {pdu_left}_{cid2} 字段编码测试通过")

# 测试正常字段编码
field = {
    "name": "group",
    "length": 1,
    "type": "hex",
    "value": "F0"
}

encoded_field = codec._encode_field(field, parsed_data, response_data)
print(f"编码字段 {field['name']}: {encoded_field.hex().upper()}")
assert encoded_field.hex().upper() == "F0", f"期望 'F0', 实际 '{encoded_field.hex().upper()}'"
print("✓ 正常字段编码测试通过")

print("\n=== 所有测试通过 ===")
print("盈佳协议编解码器功能正常!")
