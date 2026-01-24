from elasticsearch import Elasticsearch
import json

# 创建 Elasticsearch 客户端
# 替换为你实际的 Elasticsearch 服务器地址和端口
es = Elasticsearch(["http://10.1.203.38:9200"])

# 要发送的数据
data = {
    "pms_id": "",
    "pms_name": "",
    "dh_name": "",
    "zg_name": "银川市灵武市胡家堡农家乐(箱体)",
    "province_id": "",
    "dh_id": "01-08-08-01-11-01",
    "zg_id": "2406461412",
    "batch_num": "2025-07-23 08:34:23.043389",
    "statis_ymd": "20250723",
    "uuid": "00c8df3b-3ae2-4946-8760-9bb9d4312411"
}

# 索引名称
index_name = "ods_zz_irms_site_map_2025y"

# 发送数据到 Elasticsearch
try:
    response = es.index(index=index_name, body=data, doc_type="point_history_data")
    print("数据发送成功:", json.dumps(response, indent=4, ensure_ascii=False))
except Exception as e:
    print("发送数据时出错:", e)
