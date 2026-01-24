# from datetime import datetime, timedelta
#
# # ========== 2. 工具函数 ==========
# def parse_date(date_str):
#     """解析日期字符串为 datetime 对象"""
#     if not date_str:
#         # 默认前一天
#         return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
#     return datetime.strptime(date_str, "%Y-%m-%d")
#
# def years_between(start: datetime, end: datetime) -> float:
#     """计算两个日期之间相差的年数，保留 1 位小数"""
#     days = (end - start).days
#     return round(days / 365.0, 2)
#
# def classify_service_period(running_years: float, update_cycle_years: float) -> str:
#     """
#     根据运行年数和更新周期（年），判断服役年限分区段
#     """
#     if running_years >= update_cycle_years * 1.5:
#         return "超期服役>=1.5倍更新周期"
#     elif running_years >= update_cycle_years:
#         return "超期服役1.5倍更新周期"
#     else:
#         ratio = running_years / update_cycle_years
#         if ratio < 0.7:
#             return "<70%"
#         else:
#             return ">70%在超期内"
#
# # ========== 3. 主计算 ==========
# def calculate_main():
#     start_time = parse_date(START_TIME_STR)
#     current_time = parse_date(CURRENT_TIME_STR)
#     running_years = years_between(start_time, current_time)
#     service_period = classify_service_period(running_years, UPDATE_CYCLE_YEARS)
#
#     print("=== 计算结果 ===")
#     print(f"当前时间：{current_time.strftime('%Y-%m-%d')}")
#     print(f"上线时间：{start_time.strftime('%Y-%m-%d')}")
#     print(f"在网运行时长：{running_years} 年")
#     print(f"更新周期：{UPDATE_CYCLE_YEARS} 年")
#     print(f"服役年限分区段：{service_period}")
#
# if __name__ == "__main__":
#     # ========== 1. 脚本内形参 ==========
#     # 请按需手动修改以下参数
#     START_TIME_STR = "2028-11-17"  # 设备上线时间，格式：YYYY-MM-DD
#     UPDATE_CYCLE_YEARS = 6.0  # 更新周期，单位：年
#     CURRENT_TIME_STR = ""  # 留空默认取前一天；也可手动填写，如 "2025-09-20"
#
#     calculate_main()
import time
from random import random
import random

from datetime import datetime

# iteration = 1
# time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.mktime(time.localtime()) + iteration))
# current  = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
# print(current[-2:])


# yl_device_name = ["'1#工况环境'", '2#工况环境', '系统参数', '1#一次侧机组（冷机/冷塔）', '2#一次侧机组（冷机/冷塔）',
#                   'CDU']
# to_str = ",".join(yl_device_name)
# print(to_str)
#
# from random import random
# import random
# import pymysql
# from datetime import datetime
# from datetime import timedelta
#
#
# def get_sql_result(sql='select a from b'):
#     conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",
#                            database="cinterdb_400_jt_gz", charset='utf8mb4', autocommit=True)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     conn.close()
#     return [li for li in result]
#
#
# yl_device_name = ["'1#工况环境'", "'2#工况环境'", "'系统参数'", "'1#一次侧机组（冷机/冷塔）'",
#                   "'2#一次侧机组（冷机/冷塔）'", "'CDU'"]
# to_str = ",".join(yl_device_name)
# siteId = '2025'
# roomid = '202501'
# device = get_sql_result(
#     sql=f'SELECT DeviceID,DeviceName FROM m_device where SiteID IN ({siteId}) AND RoomID in ({roomid}) AND DeviceName in ({to_str})')
# device1 = get_sql_result(
#     sql=f'SELECT DeviceID,DeviceName FROM m_device where SiteID IN ({siteId}) AND RoomID in ({roomid}) AND DeviceName in ({to_str})')
#
# print(device+device1)


import os

# base_path = os.path.dirname()
base_path = os.path.dirname(os.getcwd())
targe_path = os.path.join(base_path, 'doc', 'B接口.csv')
data = open(targe_path, 'r', encoding='utf-8')
for line in data:
    print(line)

signal_list = ['013351', '013352', '013353', '012325', '012318', '012321', '013323'
    , '013330', '012326', '012329', '012333', '012339', '012340', '012334', '012345', '012344', '013405']
signal_ids_str = ",".join([f"'{id}'" for id in signal_list])
print(signal_ids_str)

from datetime import datetime, timedelta

start_str = "2025-11-01 00:00:00"
end_str = "2025-11-02 23:59:59"

# 转换为datetime对象
current_start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
overall_end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
interval = timedelta(days=2)
while current_start < overall_end:
    current_end = min(current_start + interval - timedelta(seconds=1), overall_end)

    # 格式化时间字符串
    begin_time = current_start.strftime("%Y-%m-%d %H:%M:%S")
    end_time = current_end.strftime("%Y-%m-%d %H:%M:%S")
    current_start += interval
    print(1)

from typing import List, Iterable, Optional


def test(k: Optional[float], *args):
    print(k, args)


test("c", 2, 3, 4)


def input_parma(siteId="", roomId="", deviceid="", signalid="", signal_number=""):
    parma_key = {}
    if siteId: parma_key["siteId"] = siteId
    if roomId: parma_key["roomId"] = roomId
    if deviceid: parma_key["deviceid"] = deviceid
    if signalid: parma_key["signalid"] = signalid
    if signal_number: parma_key["signal_number"] = signal_number
    return parma_key


def test1(k, **args):
    print(args, 2)


x = input_parma(siteId=1, roomId=1)
x.update({'1': 1, '2': 2})

print(input_parma(siteId=1, roomId=1))

print(type(input_parma(siteId=1, roomId=1)))

print(test1(1, **x))

[
('008318', 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)', '200', '01-32-01-02-01-03', None, None, 0, 10456053,
  '37261006000000079739', '四楼电力室1#艾默生(EMERSON UPS)(NXR)', '输出相电流Ia', 1, 2, 8, 8, 11, None,
  '无冷热通道隔离', '昭阳区全球通大楼', None, '01-32', '遥测信号', None, '夏热冬冷地区', '01-32-01-02', '昭通市',
  '通信机楼', None, 1, None, '01-32-01', '输出相电流Ia', None, 'A', '电力机房', '01-32-01-02-01', '云南', '3'),
 (
 '008318', 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)', '200', '01-32-01-02-01-03', None, None, 0, 10456053,
 '37261006000000079739', '四楼电力室1#艾默生(EMERSON UPS)(NXR)', '输出相电流Ia', 1, 2, 8, 8, 11, None, '无冷热通道隔离',
 '昭阳区全球通大楼', None, '01-32', '遥测信号', None, '夏热冬冷地区', '01-32-01-02', '昭通市', '通信机楼', None, 1,
 None, '01-32-01', '输出相电流Ia', None, 'A', '电力机房', '01-32-01-02-01', '云南', '3'),

    (
 '008318', 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)', '200', '01-32-01-02-01-03', None, None, 0, 10456053,
 '37261006000000079739', '四楼电力室1#艾默生(EMERSON UPS)(NXR)', '输出相电流Ia', 1, 2, 8, 8, 11, None, '无冷热通道隔离',
 '昭阳区全球通大楼', None, '01-32', '遥测信号', None, '夏热冬冷地区', '01-32-01-02', '昭通市', '通信机楼', None, 1,
 None, '01-32-01', '输出相电流Ia', None, 'A', '电力机房', '01-32-01-02-01', '云南', '3'), (
 '008318', 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)', '200', '01-32-01-02-01-03', None, None, 0, 10456053,
 '37261006000000079739', '四楼电力室1#艾默生(EMERSON UPS)(NXR)', '输出相电流Ia', 1, 2, 8, 8, 11, None, '无冷热通道隔离',
 '昭阳区全球通大楼', None, '01-32', '遥测信号', None, '夏热冬冷地区', '01-32-01-02', '昭通市', '通信机楼', None, 1,
 None, '01-32-01', '输出相电流Ia', None, 'A', '电力机房', '01-32-01-02-01', '云南', '3'), (
 '008318', 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)', '200', '01-32-01-02-01-03', None, None, 0, 10456053,
 '37261006000000079739', '四楼电力室1#艾默生(EMERSON UPS)(NXR)', '输出相电流Ia', 1, 2, 8, 8, 11, None, '无冷热通道隔离',
 '昭阳区全球通大楼', None, '01-32', '遥测信号', None, '夏热冬冷地区', '01-32-01-02', '昭通市', '通信机楼', None, 1,
 None, '01-32-01', '输出相电流Ia', None, 'A', '电力机房', '01-32-01-02-01', '云南', '3'), (
 '008318', 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)', '200', '01-32-01-02-01-03', None, None, 0, 10456053,
 '37261006000000079739', '四楼电力室1#艾默生(EMERSON UPS)(NXR)', '输出相电流Ia', 1, 2, 8, 8, 11, None, '无冷热通道隔离',
 '昭阳区全球通大楼', None, '01-32', '遥测信号', None, '夏热冬冷地区', '01-32-01-02', '昭通市', '通信机楼', None, 1,
 None, '01-32-01', '输出相电流Ia', None, 'A', '电力机房', '01-32-01-02-01', '云南', '3'), (
 '008318', 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)', '200', '01-32-01-02-01-03', None, None, 0, 10456053,
 '37261006000000079739', '四楼电力室1#艾默生(EMERSON UPS)(NXR)', '输出相电流Ia', 1, 2, 8, 8, 11, None, '无冷热通道隔离',
 '昭阳区全球通大楼', None, '01-32', '遥测信号', None, '夏热冬冷地区', '01-32-01-02', '昭通市', '通信机楼', None, 1,
 None, '01-32-01', '输出相电流Ia', None, 'A', '电力机房', '01-32-01-02-01', '云南', '3')]
