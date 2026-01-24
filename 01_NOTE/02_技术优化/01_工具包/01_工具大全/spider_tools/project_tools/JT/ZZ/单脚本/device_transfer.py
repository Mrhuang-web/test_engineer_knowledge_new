#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
油浸变压器设备数据 → Elasticsearch
索引：ods_zz_device_transform_2025y
"""

from elasticsearch import Elasticsearch
import json
from typing import List, Any
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus as urlquote
from spider_tools.Conf.Config import Config  # 你的原始配置入口
import os

# 1. 创建客户端
es = Elasticsearch(["http://10.1.203.38:9200"])  # 地址换成你的


# 2. 待写入的设备数据（直接从你给的 JSON 粘过来）
def generate_data(device_id, zh_label: str, res_code: str):
    data = {
        "power_device_name": "",
        "estimated_retirement_time": "2030-01-01",
        "device_subclass": "油浸变压器",
        "device_type": "变压器",
        "assets_no": "",
        "county_id": "520404",
        "maintainor": "覃启胜-13765781567",
        "lifecycle_status": "现网",
        "qualitor": "铁塔公司",
        "related_room": "754155543695894570",
        "qr_code_no": "235452080044264008369",
        "rated_power": "10",
        "backup_method": "单台设备",
        "input_rated_voltage": "10KV",
        "irms_province_code": "GZ",
        "related_site": "731175910028376230",
        "power_device_id": device_id,
        "batch_num": "20250723",
        "product_name": "S9-10/10",
        "res_code": res_code,
        "zh_label": zh_label,
        "start_time": "2015-01-01",
        "province_id": "520000",
        "device_code": "03020001",
        "device_number": "1",
        "vendor_id": "黔南望江",
        "low_reted_current": "10",
        "collect_time": "2025-07-23 14:29:46",
        "city_id": "520400"
    }
    return data


index_name = "ods_zz_device_transform_2025y"

env = 'release'
conf = Config()
dbip = conf.get_conf(env, 'dbip')
dbport = conf.get_conf(env, 'dbport')
dbname = conf.get_conf(env, 'dbname')
dbuser = conf.get_conf(env, 'dbuser')
dbpw = conf.get_conf(env, 'dbpw')
url = conf.get_conf(env, 'esurl')

# engines = f"mysql+pymysql://{urlquote(dbuser)}:{urlquote(dbpw)}@{dbip}:{dbport}/{urlquote(dbname)}?charset=utf8"
engines = f"mysql+pymysql://{dbuser}:{dbpw}@{dbip}:{dbport}/{dbname}?charset=utf8"
print(engines)
engine = create_engine(engines, max_overflow=5)
conn = engine.connect()

precinct = '01-08-08-01-02-01%'
sql_index = f""" SELECT device_id FROM t_cfg_device WHERE precinct_id LIKE '{precinct}' and power_device_id = ''; """
result = conn.execute(text(sql_index))
# 3. 写入 ES

# 4264010000 + 20
res_code = 4264023010
try:
    number = 0
    for device in result:
        "res_code  res_code不能重复，否则取出来的会去重"
        res_code = int(res_code) + 1

        "power_device_id"
        max_index = f""" SELECT max(power_device_id) FROM t_cfg_device WHERE precinct_id LIKE '{precinct}'; """
        result = conn.execute(text(max_index))

        max_power_device_id = result.fetchone()[0]
        if max_power_device_id != '' and max_power_device_id:
            power_device_id = int(max_power_device_id) + 1
            zh_label = '三都县岜炮一楼无线机房-油浸变压器-1' + str(power_device_id)
        else:
            power_device_id = 1001001001001
            zh_label = '三都县岜炮一楼无线机房-油浸变压器-1'
        power_device_id = str(power_device_id)
        print('power_device_id:', power_device_id, zh_label)

        "device_id  - 更新update power_device_id"
        device_id = device[0]
        update = f""" update t_cfg_device set power_device_id = '{power_device_id}' WHERE device_id = '{device_id}'; """
        conn.execute(text(update))
        print('device_id:', device_id, )

        res_code = str(res_code)
        data = generate_data(power_device_id, zh_label, res_code)
        print(data)
        resp = es.index(index=index_name, body=data, doc_type="point_history_data")
        print("数据写入成功:", json.dumps(resp, indent=4, ensure_ascii=False))

        number += 1
        print('number:', number)
        # if number > 400:
        #     break



except Exception as e:
    print("写入数据时出错:", e)
