# -*- coding: utf-8 -*-

import requests
import json

# 1. 目标地址（只需改这里）
TARGET_IP_PORT = "10.1.203.120:9080"  # 换成你的实际 IP:端口

# 10012 - 10018

# 动态参数
fsu_ip = '10.12.5.142'
fsu_port = '10019'

# roomName = '01-01-17-02-05-01'
# precinctId = '01-01-17-02-05-01'
# precinctIdName = '广州测试数据白云白云1核心'
# controllerName = '白云控制器测试2'
# doorName = '白云控制器测试门2'


roomName = '01-01-10-02-01-01'
precinctId = '01-01-10-02-01-01'
precinctIdName = '河源测试数据东源县东源综合楼4F动力1'
controllerName = '河源测试控制器测试9'
doorName = '河源测试控制器测试门9'



# 2. 组装 URL
url = f"http://{TARGET_IP_PORT}/spider/web/v1/entranceGuard/device/create?namespace=alauda"

# 3. 原始 header（一字不改）
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "X-REQUESTED-WITH": "XMLHttpRequest",
}

# 4. 原始 cookie（一字不改）
cookies = {
    "SESSION": "MGM1YTU0OTQtYWUxNi00YmE2LTljZDItMzA2OTJiNmM0OWQ5",
    "JSESSIONID": "AAB9CC691627DB137059066AA28BAE6E"
}

# 协议规范
device_dict_proto = {
    # 力维协议 - comPort不能重复/
    'lw': {
        "accessMode": "2",
        "accessModeName": "UDP-力维",
        "ipAddress": "10.12.5.142",
        "port": "10020",
        "groupNo": "20",
        "comPort": "01",
        "protocolVersion": "10",
        "protocolStart": "7E",
        "protocolEnd": "0D",
    }
}

# 5. 原始 json body（一字不改）
payload = {
    # 省市区机房 - 需要根据实际情况修改
    "data": {
        "city": "01-01-10",
        "cityName": "河源市",
        "area": "01-01-10-02",
        "areaName": "东源县",
        "roomName": roomName,
        "precinctIdName": precinctIdName,
        "controllerName": controllerName,
        "doorName": doorName,
        "deviceCode": "TEST-2",
        "partition": "10.9.128.78",
        "precinctId": precinctId,

        "accessMode": "2",
        "accessModeName": "UDP-力维",
        "ipAddress": fsu_ip,
        "port": fsu_port,
        "groupNo": "20",
        "comPort": "01",
        "protocolVersion": "10",
        "protocolStart": "7E",
        "protocolEnd": "0D",

    },
    "namespace": "alauda"
}

# 6. 发送请求（verify=False 对应 curl 的 --insecure）
resp = requests.post(
    url,
    headers=headers,
    cookies=cookies,
    json=payload,
    verify=False,
    timeout=10
)

# 7. 打印结果
print("HTTP Status:", resp.status_code)
try:
    print("Response JSON:", json.dumps(resp.json(), ensure_ascii=False, indent=2))
except Exception:
    print("Response Text:", resp.text)
