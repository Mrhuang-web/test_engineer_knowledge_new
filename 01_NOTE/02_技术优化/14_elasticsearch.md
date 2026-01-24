# 基础语法

## kibana格式

```
统计索引表里数据条数
GET /ods_ftp_device_pe_other*/_count


先精确查询对应数据
GET /ods_ftp_device_pe_high_distribution*/_search
{
  "query": {
    "term": {
      "related_room.keyword": "441000000000008003271359"
    }
  }
}





再修改数据（匹配，再script修改具体值）
POST /ods_ftp_device_pe_high_distribution*/_update_by_query
{
  "query": {
    "term": {
      "related_room.keyword": "441000000000008003271359"
    }
  },
  "script": {
    "source": "ctx._source.related_room = '广州市广州天河区天环1号楼'", 
    "lang": "painless"
  }
}



数据插入使用：
POST /ods_ftp_device_pe_other/_bulk
{"index":{"_type": "doc"}}
{"res_code": "123", "related_site": "广州市广州天河区天环路1路", "related_room": "广州市广州天河区天环路1路3号楼"}

查询最后一条数据：
GET /ods_ftp_room_property*/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "_doc": {
        "order": "desc"
      }
    }
  ],
  "size": 1
}

```

## head格式

```
查询语法
    先精确查询对应数据
    get
    
    ods_zz_site_202505m/_search
    {
      "query": {
        "term": {
          "point_history_data.int_id.keyword": "441000000000007995689853"
        }
      }
    }





插入/修改语法【单条件】
    再修改数据（匹配，再script修改具体值）
    POST 
    ods_ftp_device_pe_high_distribution*/_update_by_query
    
    {
      "query": {
        "term": {
          "related_room.keyword": "441000000000008003271359"
        }
      },
      "script": {
        "source": "ctx._source.related_room = '广州市广州天河区天环1号楼'", 
        "lang": "painless"
      }
    }
```



# py形式

## 创建客户端方式

```
批量的用的客户端


from elasticsearch import Elasticsearch

# 创建客户端
es = Elasticsearch(
    ["https://localhost:9200"],
    basic_auth=("elastic", "your_password"),
    verify_certs=False  # 如果是自签名证书
)

# 索引一个文档
doc = {"title": "Python ES 请求示例", "content": "Hello Elasticsearch"}
resp = es.index(index="test-index", id=1, document=doc)
print("索引结果:", resp)

# 查询文档
query = {
    "query": {
        "match": {
            "title": "Python"
        }
    }
}
resp = es.search(index="test-index", body=query)
print("查询结果:", resp)
```

## request方式

```
单次的增和查和删用的request


import requests
import json

url = "http://localhost:9200/test-index/_search"
headers = {"Content-Type": "application/json"}
query = {
    "query": {
        "match": {
            "title": "Python"
        }
    }
}

response = requests.get(url, data=json.dumps(query), headers=headers)
print(response.json())
```

