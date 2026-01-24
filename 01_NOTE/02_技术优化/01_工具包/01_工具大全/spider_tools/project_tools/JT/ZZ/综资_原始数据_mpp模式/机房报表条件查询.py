import json
import time
import requests
import csv
from asptest.common.mysqlpool import MySQLHelper
import spider_tools.Common.TestEnv as TestEnv

# 数据库连接
conn_obj = MySQLHelper(TestEnv.ServerConfig['mpp_pas_jt'])

# 读取 province.json 文件


# 配置
head_token = '7ccc1a4a79d37ebb2c992b7c8c4dac10'
cookies = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJvNXBranhlWmxqQzFxN1pZVjVLQ2ZNa2tIbnNEWUhJeWtuQVNzb0FDb21zIn0.eyJqdGkiOiIxMWUwOWIwYi1kMzQ1LTRlMWEtYTUxYi1jZTkwYWMzMDBkOGUiLCJleHAiOjE3NjgxNTYzMDAsIm5iZiI6MCwiaWF0IjoxNzY4MTM0NzAwLCJpc3MiOiJodHRwOi8vMTAuMS4yMDMuMzg6ODE4MC9hdXRoL3JlYWxtcy9kZW1vX3JlYWxtIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjFhYjNlM2JhLTY0ZjgtNDYzZS04NTFhLTIxNDhjYzdkNTMxYSIsInR5cCI6IkJlYXJlciIsImF6cCI6InByb2RfdnVlIiwibm9uY2UiOiIyNzkyODBmNy1kNWUyLTQzYjMtOGE5NS0yMTQwNGU5ZGJmYmYiLCJhdXRoX3RpbWUiOjE3NjgxMzQ3MDAsInNlc3Npb25fc3RhdGUiOiJiMDdhOTVhNC05ZGY1LTRlZmUtYjNiZC1kODY0OWQxZjUyN2MiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHA6Ly8xMC4xLjE2Mi4yMTU6ODA4MCIsImh0dHA6Ly8xMC4xLjIwMy4zODoxODI4MCIsImh0dHA6Ly8xMC4xLjE2MS43MDo4MDgwIiwiaHR0cDovLzEwLjEyLjcwLjU5OjE4MjgwIiwiaHR0cDovL2xvY2FsaG9zdDo4ODg4IiwiaHR0cDovLzEwLjEuMjAzLjM4OjE4NjgwIiwiaHR0cDovLzEwLjEuMjAzLjM4OjE4NTgwIiwiaHR0cDovLzEwLjEuMTYzLjIwMzo4MDgwIiwiaHR0cDovLzEwLjEuNS4xMDM6ODA4MCIsImh0dHA6Ly8xMC4xLjE2OS4xNzE6ODA4MCIsImh0dHA6Ly8xMC4xLjIwMy4xMjA6MTgyODAiLCJodHRwOi8vMTAuMS4xNjguMjI0OjgwODAiLCJodHRwOi8vMTAuMTgxLjEyLjEyMTozMDkxMiIsImh0dHA6Ly9sb2NhbGhvc3Q6ODA4MCIsImh0dHA6Ly8xMC4xMi4xMi4xODQ6MTgyODAiLCJodHRwOi8vMTAuMTgxLjEyLjExMTo4MDgwIiwiaHR0cDovLzEwLjEuMTI4LjUzOjgwODAiLCJodHRwOi8vMTAuMTgxLjEyLjEyMTozMDkxMyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJlbXBsb3llZVR5cGUiOiJhZG1pbiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6Im1pZ3UuYWx1ZGEgbWlndS5hbGF1ZGEiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhbGF1ZGEiLCJsb2NhbGUiOiJlbiIsImdpdmVuX25hbWUiOiJtaWd1LmFsdWRhIiwidXNlck5hbWUiOiJhbGF1ZGEiLCJmYW1pbHlfbmFtZSI6Im1pZ3UuYWxhdWRhIiwiZW1haWwiOiIxMjMwMUBxcS5jb20ifQ.kq0zQ9ruBBfGlIqto5l5Ok3oyj4MBr72DZ1mB7vpMpWREdSKU3PYv4l5learQIA37qyWYNqeocM-7v7WiSTGyKvJI0TAOCY8naGj4KCDM8E60BMMmgJS24Re6rpGxzVp15V9brHciiV_WJmPFZ1r05N1Pbnp-j6T_bSTddyEmJtMXED6zeU8TssatXGWdy7fUxRtBUjotdJUjyMiqRiOA0DO_mT47lXwR3e2BTDgpGA2mZ4LfFjhZnC-tX8Yi10LUwdhfK9T-GfAzdwttNf4yPS6LvXXlDjhCjiMoB3AEM0yQCYxky94TeDBamoIFD95wE08JeVozPjOv5r7sgIwIQ'

# 接口请求地址


# 请求头
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "head_orgAccount": "alauda",
    "head_userName": "alauda",
    "head_token": head_token,
    "Authorization": cookies
}


def compare_data(table_name, province_code=None, city_code=None, area_code=None, batch_num='20250723'):
    url = ''
    data = ''
    data_device = {"page": 1, "rows": 20,
                   "data": {"provinceCode": province_code, "cityCode": city_code, "areaCode": area_code, "siteCode": "",
                            "roomCode": "", "deviceSubclass": ""}, "precinctId": "", "siteType": "",
                   "namespace": "alauda"}
    # 构建请求参数
    if table_name == 'ods_zz_site':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getSite"
        data = {
            "page": 1, "rows": 20,
            "data": {
                "lifecycleStatus": "", "provinceCode": province_code, "cityCode": city_code, "areaCode": area_code,
                "useCorp": "", "businessType": "", "siteName": "", "siteType": ""
            },
            "precinctId": "", "siteType": "", "namespace": "alauda"
        }
    elif table_name == 'ods_zz_room':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getRoom"
        data = {
            "page": 1, "rows": 20,
            "data": {"startCutinDate": "", "endCutinDate": "", "lifecycleStatus": "", "provinceCode": province_code,
                     "cityCode": city_code, "areaCode": area_code, "equiproomLevel": "", "sharedUnit": "",
                     "equiproomType": "", "siteCode": "", "roomName": "", "businessUnit": ""}, "precinctId": "",
            "siteType": "",
            "namespace": "alauda"
        }
    elif table_name == 'ods_zz_site_property':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getSitePropertyList"
        data = {"page": 1, "rows": 20,
                "data": {"mainsVoltageLevel": "", "provinceCode": "", "cityCode": "", "areaCode": "", "siteName": "",
                         "mainsBackupMethod": "", "powerSiteLevel": "", "mainsNature": "", "isColdStorageInstall": ""},
                "precinctId": "", "siteType": "", "namespace": "alauda"}
    elif table_name == 'ods_zz_room_property':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getRoomPropertyList"
        data = {"page": 1, "rows": 20,
                "data": {"spaceRoomType": "", "provinceCode": "", "cityCode": "", "areaCode": "", "powerRoomType": "",
                         "siteCode": "", "roomName": ""}, "precinctId": "", "siteType": "", "namespace": "alauda"}

    elif table_name == 'ods_zz_device_transform':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceTransform"
        data = data_device
    elif table_name == 'ods_zz_device_transform_device':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceTransformDevice"
        data = data_device
    elif table_name == 'ods_zz_device_high_distribution':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceHighDistribution"
        data = data_device
    elif table_name == 'ods_zz_device_high_power':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceHighPower"
        data = data_device
    elif table_name == 'ods_zz_device_high_dc_distribution':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceHighDcDistribution"
        data = data_device
    elif table_name == 'ods_zz_device_power_generation':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDevicePowerGeneration"
        data = data_device
    elif table_name == 'ods_zz_device_switch_power':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceSwitchPower"
        data = data_device
    elif table_name == 'ods_zz_device_low_ac_distribution':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceLowAcDistribution"
        data = data_device
    elif table_name == 'ods_zz_device_low_dc_distribution':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceLowDcDistribution"
        data = data_device
    elif table_name == 'ods_zz_device_ups':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceUps"
        data = data_device
    elif table_name == 'ods_zz_device_battery':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceBattery"
        data = data_device
    elif table_name == 'ods_zz_device_air':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceAir"
        data = data_device
    elif table_name == 'ods_zz_device_energy_save':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceEnergySave"
        data = data_device
    elif table_name == 'ods_zz_device_power_monitor':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDevicePowerMonitor"
        data = data_device
    elif table_name == 'ods_zz_device_smart_meter':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceSmartMeter"
        data = data_device
    elif table_name == 'ods_zz_device_other':
        url = "http://10.1.203.38:18580/spider/web/v1/report/zzData/getDeviceOther"
        data = data_device

    response1 = None
    # 发送请求
    try:
        response1 = requests.post(url=url, headers=headers, json=data)
        response = response1.json()
        page_result = response['total']
    except:
        print("data:", data)
        print("response:", response1)
        page_result = None

    # 构建SQL语句
    if province_code:
        sql_index = f"SELECT COUNT(1) FROM {table_name} WHERE province_id = '{province_code}' and batch_num = '{batch_num}'"
    elif area_code:
        sql_index = f"SELECT COUNT(1) FROM {table_name} WHERE province_id = '{province_code}' AND city_id = '{city_code}' AND county_id = '{area_code}' and batch_num = '{batch_num}'"
    elif city_code:
        sql_index = f"SELECT COUNT(1) FROM {table_name} WHERE province_id = '{province_code}' AND city_id = '{city_code}' and batch_num = '{batch_num}'"
    else:
        sql_index = f"SELECT COUNT(1) FROM {table_name} WHERE stat_time = '{batch_num}'"

    # 查询数据库
    if province_code or area_code or city_code:
        sql_result = conn_obj.select(sql_index)[0][0]
        # 比较结果
        match_status = "匹配" if sql_result == page_result else "不匹配"
        return match_status, province_code, city_code, area_code, page_result, sql_result
    else:
        sql_result = conn_obj.select(sql_index)[0][0]
        # 比较结果
        match_status = "匹配" if sql_result == page_result else "不匹配"
        return table_name, match_status, province_code, city_code, area_code, page_result, sql_result


def traverse_and_compare(mode):
    # 打开CSV文件
    with open('compare_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # 写入CSV表头
        csv_writer.writerow(['match', 'province_id', 'city_id', 'area_id', 'page_data', 'sql_data'])

        if mode == 'province':
            for province_code, cities in province_data.items():
                # 比较省份
                result = compare_data(table_name, province_code)
                csv_writer.writerow(result)
        elif mode == 'city':
            for province_code, cities in province_data.items():
                # 比较省份
                result = compare_data(table_name, province_code)
                csv_writer.writerow(result)
                if province_code not in ('110000', '120000', '310000', '500000'):
                    items = list(cities.items())
                    del items[0]
                    cities = dict(items)

                # 遍历城市
                for city_code, areas in cities.items():
                    # 比较城市
                    result = compare_data(table_name, province_code, city_code)
                    csv_writer.writerow(result)
        elif mode == 'county':
            for province_code, cities in province_data.items():
                # 比较省份
                result = compare_data(table_name, province_code)
                csv_writer.writerow(result)

                if province_code not in ('110000', '120000', '310000', '500000'):
                    items = list(cities.items())
                    del items[0]
                    cities = dict(items)

                # 遍历城市
                for city_code, areas in cities.items():
                    # 比较城市
                    result = compare_data(table_name, province_code, city_code)
                    csv_writer.writerow(result)

                    # 遍历区
                    for area_code in areas:
                        # 比较区
                        result = compare_data(table_name, province_code, city_code, area_code)
                        csv_writer.writerow(result)

                # time.sleep(1)  # 控制请求频率


def traverse_and_compare_table(tables):
    # 打开CSV文件
    with open('compare_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # 写入CSV表头
        csv_writer.writerow(['table_name', 'match', 'province_id', 'city_id', 'area_id', 'page_data', 'sql_data'])

        for table_name in tables:
            # 比较省份
            result = compare_data(table_name)
            csv_writer.writerow(result)


# 执行遍历和比较
if __name__ == "__main__":
    with open('province.json', 'r', encoding='utf-8') as f:
        province_data = json.load(f)

    """
        手工指定格式
        "省份编码"：{
        "110000": ["110000"],
        "110101": ["110101"]
        }
        
        或：
        province:province_data[province]
        province_data = {'220000': province_data['220000']}
    """

    """
        全表匹配 - 无过滤
    """
    # table = ['ods_zz_site', 'ods_zz_room', 'ods_zz_room_property', 'ods_zz_site_property', 'ods_zz_device_transform',
    #          'ods_zz_device_transform_device', 'ods_zz_device_high_distribution', 'ods_zz_device_high_power',
    #          'ods_zz_device_high_dc_distribution', 'ods_zz_device_low_ac_distribution',
    #          'ods_zz_device_power_generation', 'ods_zz_device_switch_power', 'ods_zz_device_low_dc_distribution',
    #          'ods_zz_device_ups', 'ods_zz_device_battery', 'ods_zz_device_air', 'ods_zz_device_energy_save',
    #          'ods_zz_device_power_monitor', 'ods_zz_device_smart_meter', 'ods_zz_device_other']
    # traverse_and_compare_table(table)

    # province_data = {'220000': province_data['220000']}
    table_name = 'ods_zz_room'
    mode = 'province'
    stat_time = '20250723'
    traverse_and_compare(mode)
