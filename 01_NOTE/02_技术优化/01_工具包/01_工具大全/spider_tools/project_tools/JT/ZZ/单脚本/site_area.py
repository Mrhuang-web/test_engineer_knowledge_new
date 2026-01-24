from elasticsearch import Elasticsearch
import json

# 创建 Elasticsearch 客户端
# 替换为你实际的 Elasticsearch 服务器地址和端口
es = Elasticsearch(["http://10.1.203.38:9200"])

# 要发送的数据
data = {
    "china_tower_station_code": "无",
    "village_pass_serv_code": "",
    "cutin_date": "2022-08-01",
    "site_type": "用户站点",
    "latitude": "24.25487893",
    "floor_number": "1",
    "project_name": "",
    "related_dc": "",
    "uuid": "",
    "county_id": "520404",
    "is_headquarters_used": "否",
    "pms_address_code": "",
    "business_type": "家客集客",
    "int_id": "2406461412",
    "lifecycle_status": "在网",
    "qualitor": "杨加寿",
    "if_tele_cmn_serv": "否",
    "longitude": "98.28418972",
    "tele_cmn_serv_pro_code": "",
    "address": "德宏芒市遮放镇街道村街道村委会街道四队",
    "village_pass_serv_name": "",
    "irms_province_code": "GZ",
    "project_code": "",
    "area_type": "城区",
    "batch_num": "20250723",
    "alias_name": "芒市MS-ZF-B0091集客站点",
    "standardaddress": "6432594",
    "if_village_pass_serv": "否",
    "zh_label": "银川市灵武市胡家堡农家乐(箱体)",
    "province_id": "520000",
    "tele_cmn_serv_pro_name": "",
    "use_corp": "中国移动",
    "collect_time": "2025-07-23 18:42:56",
    "city_id": "520400"
}

# 索引名称
index_name = "ods_zz_site_202507m"

# 发送数据到 Elasticsearch
try:
    response = es.index(index=index_name, body=data, doc_type="point_history_data")
    print("数据发送成功:", json.dumps(response, indent=4, ensure_ascii=False))
except Exception as e:
    print("发送数据时出错:", e)
