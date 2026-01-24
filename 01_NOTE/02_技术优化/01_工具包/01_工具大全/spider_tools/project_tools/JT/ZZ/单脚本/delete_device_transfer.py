#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除Elasticsearch中指定条件的数据
"""

from elasticsearch import Elasticsearch
from spider_tools.Conf.Config import Config  # 你的原始配置入口
from sqlalchemy import create_engine, text

# 配置信息
es = Elasticsearch(["http://10.1.203.38:9200"])  # 地址换成你的

# 2. 设置删除条件
index_name = "ods_zz_device_transform_2025y"  # 要操作的索引名称
# 删除条件：related_site为1001001001001的数据
query = {
    "query": {
        "term": {
            "related_site": "731175910028376230"
        }
    }
}

# 如果要删除power_device_id为1001001001001的数据，可以使用以下条件
# query = {
#     "query": {
#         "term": {
#             "power_device_id": "1001001001001"
#         }
#     }
# }

# 数据库同步删除
env = 'release'
conf = Config()
dbip = conf.get_conf(env, 'dbip')
dbport = conf.get_conf(env, 'dbport')
dbname = conf.get_conf(env, 'dbname')
dbuser = conf.get_conf(env, 'dbuser')
dbpw = conf.get_conf(env, 'dbpw')
url = conf.get_conf(env, 'esurl')

engines = f"mysql+pymysql://{dbuser}:{dbpw}@{dbip}:{dbport}/{dbname}?charset=utf8"
print(engines)
engine = create_engine(engines, max_overflow=5)
conn = engine.connect()





try:
    # 3. 执行删除操作
    print(f"正在删除索引 {index_name} 中 related_site 为 731175910028376230 的数据...")
    response = es.delete_by_query(index=index_name, body=query, doc_type="point_history_data")

    # 4. 输出删除结果
    print("删除操作完成！")
    print(f"删除的文档数量: {response['deleted']}")
    print(f"耗时: {response['took']}ms")
    print(f"版本冲突数: {response.get('version_conflicts', 0)}")

    # 5. 数据库清空power_device_id
    precinct = '01-08-08-01-02-01%'
    update = f""" update t_cfg_device set power_device_id = '' WHERE precinct_id LIKE '{precinct}'; """
    conn.execute(text(update))
    print('清空power_device_id成功')

except Exception as e:
    print(f"删除数据时出错: {e}")
