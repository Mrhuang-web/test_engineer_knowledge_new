from elasticsearch import Elasticsearch
import json

# 创建 Elasticsearch 客户端
# 替换为你实际的 Elasticsearch 服务器地址和端口
es = Elasticsearch(["http://10.1.203.38:9200"])  # 根据你的 ESConfig 配置修改

# 要发送的数据
data = {
    "mains_nature": "市电直供",
    "power_monitoring_site_name": "",
    "cold_storage_time": "",
    "water_cooling_conf": "",
    "property_unit": "",
    "county_id": "520404",
    "power_is_substations": "否",
    "mains_configuration_level": "2市电1油机",
    "total_mains_number": "2",
    "tatal_tank_volume": "",
    "is_attach_idc_room": "否",
    "total_tank_number": "",
    "power_site_level": "通信机楼",
    "irms_province_code": "GZ",
    "is_cold_storage_install": "",
    "batch_num": "20250723",
    "mains_voltage_level": "10KV",
    "res_code": "44100000000123123",
    "power_monitoring_site_id": "",
    "zh_label": "2406461412",
    "mains_capacity": "4500",
    "power_supply": "双变电站引入",
    "province_id": "520000",
    "collect_time": "2025-07-23 14:27:54",
    "design_pue": "1.5",
    "mains_backup_method": "1+1冷备",
    "actual_pue": "1.5",
    "city_id": "520400"
}

# 索引名称
index_name = "ods_zz_site_property_202507m"

# 发送数据到 Elasticsearch
try:
    response = es.index(index=index_name, body=data, doc_type="point_history_data")
    print("数据发送成功:", json.dumps(response, indent=4, ensure_ascii=False))
except Exception as e:
    print("发送数据时出错:", e)
