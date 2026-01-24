#!/usr/bin/env python
# -*- coding:utf8 -*-


# 云南 121
# SOCKET_PORT = 8092
# HTTP_PORT = 8091
# MYSQL_CONN_STR = "mysql+pymysql://root:nZ0qJ8kA1aI9@10.1.203.38:3306/cinterdb_400_yn?charset=utf8&autocommit=true"

# guangxi
# SOCKET_PORT = 8292
# HTTP_PORT = 8891
# MYSQL_CONN_STR = "mysql+pymysql://root:G$SGp!8L3O@10.1.203.38:3306/cinterdb_400_gx?charset=utf8&autocommit=true"


# guangxi
# SOCKET_PORT = 8292
# HTTP_PORT = 8892
# MYSQL_CONN_STR = "mysql+pymysql://root:2oLYLnC-1*y7lub5hX$h@10.12.12.186:3306/c_guangxi?charset=utf8&autocommit=true"

SOCKET_PORT = 8097
HTTP_PORT = 8087
# MYSQL_CONN_STR = "mysql+pymysql://root:G$SGp!8L3O@10.1.203.38:3306/cinterdb?charset=utf8&autocommit=true"
MYSQL_CONN_STR = "mysql+pymysql://root:G$SGp!8L3O@10.1.203.38:3306/cinterdb_400_dcim_out?charset=utf8&autocommit=true"

# dcim
# SOCKET_PORT = 8292
# HTTP_PORT = 8891
# MYSQL_CONN_STR = "mysql+pymysql://root:G$SGp!8L3O@10.1.203.38:3306/cinterdb_400_dcim?charset=utf8&autocommit=true"

# dcim_out接入到集团
# SOCKET_PORT = 8292
# HTTP_PORT = 8891
# MYSQL_CONN_STR = "mysql+pymysql://root:G$SGp!8L3O@10.1.203.38:3306/cinterdb_400_dcim_out?charset=utf8&autocommit=true"


# #gz
# SOCKET_PORT = 8296
# HTTP_PORT = 8896
# MYSQL_CONN_STR = "mysql+pymysql://root:G$SGp!8L3O@10.1.203.38:3306/cinterdb_400_gz?charset=utf8&autocommit=true"


# #guangdong
# SOCKET_PORT = 8090
# HTTP_PORT = 8089
# MYSQL_CONN_STR = "mysql+pymysql://root:G$SGp!8L3O@10.1.203.38:3306/cinterdb_400_gd?charset=utf8&autocommit=true"

# C接口规范中定义的一些常量及枚举值
# 5.2.6常量定义
# 如果长度不够，则在末尾以〈SPACE键〉填充
# 注释掉3.5的
# NAME_LENGTH = 40    #名字命名长度 字节
# USER_LENGTH = 20
# PASSWORD_LEN = 20
# EVENT_LENGTH = 160
# ALARM_LENGTH = 165
# LOGIN_LENGTH = 100
# DES_LENGTH = 40
# UNIT_LENGTH = 8
# STATE_LENGTH = 160
# VER_LENGTH  = 20 #


NAME_LENGTH = 20  # NAME_LENGTH	名字命名长度	40字节
USER_LENGTH = 20  # USER_LENGTH	用户名长度	20字节
PASSWORD_LEN = 20  # PASSWORD_LEN	口令长度	20字节
TIME_LEN = 20  # TIME_LEN	时间串长度	19字节
EVENT_LENGTH = 20  # EVENT_LENGTH	事件信息长度	160字节
ALARM_LENGTH = 20  # ALARM_LENGTH	告警事件信息长度	175字节
ALARMSERIALNO_LENGTH = 20  # ALARMSERIALNO_LENGTH	告警序号	10字节
LOGIN_LENGTH = 20  # LOGIN_LENGTH	登录事件信息长度	100字节
DES_LENGTH = 20  # DES_LENGTH	描述信息长度	60字节
UNIT_LENGTH = 20  # UNIT_LENGTH	数据单位的长度	8字节
STATE_LENGTH = 20  # STATE_LENGTH	态值描述长度	160字节
VER_LENGTH = 20  # VER_LENGTH	版本描述的长度	20字节
SCID_LEN = 20  # SCID_LEN	SC编号长度	7字节
SITEID_LEN = 20  # SITEID_LEN	站点编号长度	20字节
ROOM_LEN = 20  # ROOM_LEN	机房编号长度	20字节
DEVICEID_LEN = 20  # DEVICEID_LEN	设备编号长度	26字节
ID_LEN = 20  # ID_LEN	监控点编号长度	20字节
NMALARMID_LEN = 20  # NMALARMID_LEN	网管告警编号	40字节
SIGNALNUM_LEN = 20  # SIGNALNUM_LEN	同类监控点顺序号	3字节
DEVICETYPE_LEN = 20  # DEVICETYPE_LEN	设备类型	2字节

# 5.1.7 枚举定义
# 监控系统下级SC向上级SC提供的权限定义
EnumRightMode = {"INVALID": 0, "LEVEL1": 1, "LEVEL2": 2}
EnumResult = {"FAILURE": 0, "SUCCE": 1}
EnumAcceSCMode = {"ASK_ANSWER": 0, "CHANGE_TRIGGER": 1, "TIME_TRIGGER": 2, "STOP": 3}
EnumType = {"ALARM": 0, "DO": 1, "AO": 2, "AI": 3, "DI": 4, "DEVICE": 5, "ROOM": 6, "SITE": 7, "AREA": 8, "AO": 9}
EnumState = {"NOALARM": 0, "CRITICAL": 1}
EnumAcceLSCMode = {"ASK_ANSWER": 0, "CHANGE_TRIGGER": 1, "TIME_TRIGGER": 2, "STOP": 3}
