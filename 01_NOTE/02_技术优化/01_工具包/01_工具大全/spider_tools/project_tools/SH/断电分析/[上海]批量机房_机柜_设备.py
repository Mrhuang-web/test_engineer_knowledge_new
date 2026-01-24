# encoding:utf-8
"""
@CreateTime:      2024/1/30 16:12
@Author:          Tsuiguangchun
@FileName:        make_room_devices.py
@IDE_SoftWare:    PyCharm
@description:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
使用完之后，需要到sim_fsu里面输入
补充 - 删除逻辑
"""
import random
import time
import json
from spider_tools.Common import TestEnv
from spider_tools.Common.all_excelCase_file_path import load_excel_data
import os
import requests
from asptest.common.mysqlpool import MySQLHelper
import uuid

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

conn_obj = MySQLHelper(TestEnv.ServerConfig['db_pas_sh'])

dict_number = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}

cookies = 'SESSION=MmVlNjk0NGUtZWU5MS00YTkyLTljNDAtOWMwN2JjNTViMTc0; JSESSIONID=1B23FFFEF1CDEC99C8571A4FA59A6300'
head_token = '7ccc1a4a79d37ebb2c992b7c8c4dac10'


def make_device_sql():
    # 01_01：机房[1个机柜列-n个机柜]
    # 删除方式：delete from t_cfg_device where precinct_id = '01-01-08-04-15-G97-02' and device_id like '00713006000000300%';
    precinct_id = '01-01-08-04-15-G97-02'
    device_model = '00001008000000018855'
    for cabinet_col_id in range(2, 9):
        for cabinet_id in range(10, 99):
            device_id = '00713006000000300'
            device_name = "UPS配电"

            device_id = device_id + str(cabinet_col_id) + str(cabinet_id)
            device_name = device_name + "0" + str(cabinet_col_id) + str(cabinet_id)
            insert_floor_sql = f"INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`, `brand`, `manufacturer`, `battery_single_number`, `battery_single_voltage`, `module_count`, `back_module_count`, `sigle_module_info`, `confirm_content`, `confirm_time`, `convert_efficiency`, `design_reserve_length`, `battery_number`, `max_discharge_efficiency`, `battery_type`, `protocol_convert_type`, `dev_describe`, `power_device_id`, `status`, `sys_no`) VALUES ('1', '{device_id}', '{device_name}', '{precinct_id}', 8, NULL, 000, '{device_model}', 11, NULL, 9, 1, NULL, '100100000000009', 1617, 1, NULL, NULL, NULL, '2025-08-12 18:11:53', NULL, NULL, NULL, NULL, '中兴力维', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 10106425, NULL, NULL, NULL, NULL, NULL, 0, 0, 101, NULL, 0, '2025-08-12 17:04:32', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);"
            conn_obj.insertone(sql=insert_floor_sql)
            print(f"已经插入：{insert_floor_sql}")


def make_fsu_mete_sql():
    # 00713006000000300210 - 00713006000000300230
    # UPS配电0210 - UPS配电0210

    #   metecode    showmetename  metekind meteno unit  measureVal
    mete_list = [
        ['009301', '分路XX相电流Ia', '1', '0', 'A', 30],
        ['009302', '分路XX相电流Ib', '1', '0', 'A', 0.02],
        ['009303', '分路XX相电流Ic', '1', '0', 'A', 20],
        ['009304', '分路XX相电压Ua', '1', '0', 'V', 10],
        ['009305', '分路XX相电压Ub', '1', '0', 'V', 10],
        ['009306', '分路XX相电压Uc', '1', '0', 'V', 10],
        ['009307', '分路XX有功功率Pa', '1', '0', 'kW', 10],
        ['009308', '分路XX有功功率Pb', '1', '0', 'kW', 10],
        ['009309', '分路XX有功功率Pc', '1', '0', 'kW', 10],
    ]

    precinct_name = '上海机房1'
    building_id = '01-01-08-04-15-G97'
    building_name = '上海楼栋1'
    precinct_id = '01-01-08-04-15-G97-02'
    collectTime = '2025-09-23 14:01:03'
    createTime = '2025-09-23 14:01:05'

    number = 1
    deviceName = 'UPS配电02'
    device_id = '007130060000003002'
    for num in range(10, 52):
        deviceName_ = deviceName + str(num)
        deviceid = device_id + str(num)
        for info in mete_list:
            sql = f"INSERT INTO `fsu_point_data_20250924` (`id`, `meteCode`, `deviceId`, `signalNumber`, `collectTime`, `measureVal`, `meteName`, `precinctName`, `buildingID`, `buildingName`, `precinctID`, `deviceName`, `unit`, `create_time`) VALUES ('{number}', '{info[0]}', '{deviceid}', '{info[3]}', '{collectTime}', {info[5]}, '{info[1]}', '{precinct_name}', '{building_id}', '{building_name}', '{precinct_id}', '{deviceName_}', '{info[4]}', '{createTime}');"
            data = conn_obj.insertone(sql)
            print(sql)
            number += 1


def make_floor_Internet():
    work = os.path.join(ROOT_PATH, "doc", "flood_name[100层].csv")
    file = open(file=work, mode='r', encoding='utf-8')  # utf-8
    data = file.read()
    # print(f"data:{data}")
    url = "http://10.1.203.120:9081/spider/web/v1/configManagement/savePrecinct?namespace=alauda"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "head_orgAccount": "alauda",
        "head_userName": "alauda",
        "head_token": head_token,
        "cookie": cookies
    }
    for name in data.split('\n'):
        print(f"开始创建机楼：{name}\n")
        data = {
            "upPrecinctId": "01-01-08-04-15",
            "precinctId": "",
            "precinctName": f"{name}",
            "leader": "",
            "leaderName": "",
            "leaderPhone": "OLweh6O6d5Ej2RbXEr36iQ==",
            "areaCode": "",
            "resourceCode": "",
            "description": "",
            "precinctKind": 3,
            "accessType": 0,
            "namespace": "alauda"
        }
        response = requests.post(url=url, headers=headers, json=data).text
        time.sleep(6)
        print(response)


def make_room_Internet():
    work = os.path.join(ROOT_PATH, "doc", "room_name[100层].csv")
    file = open(file=work, mode='r', encoding='utf-8')  # utf-8
    data = file.read()
    # print(f"data:{data}")
    url = "http://10.1.203.120:9081/spider/web/v1/configManagement/saveStationPrecinct?namespace=alauda"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "head_orgAccount": "alauda",
        "head_userName": "alauda",
        "head_token": head_token,
        "cookie": cookies
    }
    for name in data.split('\n'):
        Name = name.split(",")
        if len(Name) > 1:
            print(f"开始创建机房：{Name[1]}\n")
            data = {
                "upPrecinctId": f"{Name[0]}",
                "precinctId": "",
                "precinctName": f"{Name[1]}",
                "areaCode": "",
                "stationTypeName": "数据中心",
                "roomKind": "5",
                "airType": 1,
                "x": "",
                "y": "",
                "altitude": "",
                "runType": "0",
                "leader": "",
                "leaderName": "",
                "leaderPhone": "",
                "resourceCode": "",
                "address": "",
                "description": "",
                "precinctKind": 5,
                "scene": "",
                "accessType": 1,
                "namespace": "alauda"
            }
            response = requests.post(url=url, headers=headers, json=data).text
            time.sleep(6)
            print(response)


def make_room_Internet_single():
    station = ''
    floor = ''
    room = ''

    url = "http://10.1.203.120:9081/spider/web/v1/configManagement/saveStationPrecinct?namespace=alauda"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "head_orgAccount": "alauda",
        "head_userName": "alauda",
        "head_token": head_token,
        "cookie": cookies
    }
    for name in range(3, 20):
        Name = name.split(",")
        if len(Name) > 1:
            print(f"开始创建机房：{Name[1]}\n")
            data = {
                "upPrecinctId": f"{Name[0]}",
                "precinctId": "",
                "precinctName": f"{Name[1]}",
                "areaCode": "",
                "stationTypeName": "数据中心",
                "roomKind": "5",
                "airType": 1,
                "x": "",
                "y": "",
                "altitude": "",
                "runType": "0",
                "leader": "",
                "leaderName": "",
                "leaderPhone": "",
                "resourceCode": "",
                "address": "",
                "description": "",
                "precinctKind": 5,
                "scene": "",
                "accessType": 1,
                "namespace": "alauda"
            }
            response = requests.post(url=url, headers=headers, json=data).text
            time.sleep(6)
            print(response)


def make_cabinet_columns_Internet():
    work = os.path.join(ROOT_PATH, "doc", "cabinet_columns_name[100层].csv")
    file = open(file=work, mode='r', encoding='utf-8')  # utf-8
    data = file.read()
    # print(f"data:{data}")
    url = "http://10.1.203.120:9081/spider/web/v1/energyCabinetColumn/addOrUpdateCabinetColumn?namespace=alauda"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "head_orgAccount": "alauda",
        "head_userName": "alauda",
        "head_token": head_token,
        "cookie": cookies
    }
    for name in data.split('\n'):
        Name = name.split(",")
        if len(Name) > 1:
            print(f"开始创建机柜列：{Name[4]}\n")
            data = {
                "stationName": Name[0],
                "buildingName": Name[1],
                "roomName": Name[2],
                "roomId": Name[3],
                "cabinetColumnName": Name[4],
                "cabinetColumnType": 1,
                "ratedElectricalLoad": 10000,
                "designCabinetNumber": 10,
                "channelName": Name[5],
                "channelType": "1",
                "businessName": "",
                "isConfig": "",
                "isEdit": True,
                "serialNo": 1,
                "index": 1,
                "sortOrder": 11
            }
            response = requests.post(url=url, headers=headers, json=data).text
            time.sleep(6)
            print(response)


def make_cabinet_columns_Internet_single():
    url = "http://10.1.203.120:9081/spider/web/v1/energyCabinetColumn/addOrUpdateCabinetColumn?namespace=alauda"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "head_orgAccount": "alauda",
        "head_userName": "alauda",
        "head_token": head_token,
        "cookie": cookies
    }

    stationName = '黄某测试数据某_上海定制2'
    buildingName = '黄某某_上海定制2'
    roomName = '黄某测试数据某_上海定制2'
    roomId = '01-01-08-04-07-01-02'

    for ids in range(2, 30):
        cabinetColumnName = '测试机柜列'
        channelName = '冷通道'
        if ids < 10:
            cabinetColumnName = cabinetColumnName + '0' + str(ids)
            channelName = channelName + '0' + str(ids)
        else:
            cabinetColumnName = cabinetColumnName + str(ids)
            channelName = channelName + str(ids)
        data = {
            "stationName": stationName,
            "buildingName": buildingName,
            "roomName": roomName,
            "roomId": roomId,
            "cabinetColumnName": cabinetColumnName,
            "cabinetColumnType": 1,
            "ratedElectricalLoad": 10000,
            "designCabinetNumber": 10,
            "channelName": channelName,
            "channelType": "1",
            "businessName": "",
            "isConfig": "",
            "isEdit": True,
            "serialNo": 1,
            "index": 1,
            "sortOrder": 11
        }
        response = requests.post(url=url, headers=headers, json=data).text
        time.sleep(6)
        print(response)


def make_cabinet_Internet_single():
    url = "http://10.1.203.120:9081/spider/web/v1/energyCabinet/addOrUpdateCabinet?namespace=alauda"

    precinct_id = '01-01-08-04-16-01-02'
    room_id = "SELECT  room.precinct_id  from t_cfg_precinct room left join t_cfg_precinct building on room.up_precinct_id = building.precinct_idleft join t_cfg_precinct site on building.up_precinct_id = site.precinct_id where building.precinct_id = '01-01-08-04-16-01';"

    cabinet_columns = conn_obj.select(
        f"SELECT cabinet_column_number,cabinet_column_name,id FROM energy_cabinet_column WHERE cabinet_column_name LIKE '测试机柜列%' AND precinct_id = '{precinct_id}' ORDER BY update_time ASC;")
    print(f"cabinet_columns:{cabinet_columns}")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "head_orgAccount": "alauda",
        "head_userName": "alauda",
        "head_token": head_token,
        "cookie": cookies
    }

    stationName = '性能采集测试站点'
    buildingName = '性能采集测试楼栋'
    roomName = '性能采集机房1'

    number = 1
    for rom in room_id[1:]:
        for cabinet_column_number, cabinet_column_name, id in cabinet_columns:
            print(cabinet_column_number, cabinet_column_name, id)

            if number <= 2:
                for cab_id in range(1, 2):
                    cabinet_name = '测试机柜'
                    cabinet_name = cabinet_name + '0' + str(cab_id)
                    print(f"开始创建机柜：{cabinet_name}\n")
                    data = {
                        "stationName": stationName,
                        "buildingName": buildingName,
                        "roomName": roomName,
                        "cabinetColumnNumber": cabinet_column_number,
                        "cabinetColumnName": cabinet_column_name,
                        "cabinetNumber": "",
                        "cabinetName": cabinet_name,
                        "cabinetAlias": "",
                        "sortOrder": 123,
                        "ratedElectricalLoad": 111,
                        "ratedU": "42",
                        "ratedU1": 37,
                        "networkPortNumber": "",
                        "cabinetType": 1,
                        "ratedWeight": "",
                        "cabinetLength": "",
                        "cabinetWidth": "",
                        "isConfig": "",
                        "businessName": "",
                        "isEdit": True,
                        "serialNo": 1,
                        "cabinetColumnId": id,
                        "index": 1
                    }
                    response = requests.post(url=url, headers=headers, json=data).text
                    time.sleep(6)
                    print(response)
            number += 1


def make_mete_Internet_single():
    # 前置说明:需要准备足够的设备  -- 即接入的时候,需要接入足够的设备,不然只有一个机房有

    # 前面造数的设备，公用device_model
    # device_model = '00001008000000018855', device_name = "UPS配电"
    # 好像没数据

    url = "http://10.1.203.120:9081/spider/web/v1/energyCabinetColumn/addOrUpdateConfig?namespace=alauda"
    precinct_id = "01-01-08-04-16-01-02"

    # "precinct_id"	"cabinet_column_number"	"cabinet_column_name"	"id"	"cabinet_name"	"cabinet_number"
    # "01-01-08-04-15-G97-02"	"7369248738096979968"	"测试机柜列02"	"0446e684db0e4b20be8d784cd0d1eaeb"	"测试机柜01"	"7369249851512725504"
    cabinet_list_sql = f"SELECT a.precinct_id,b.cabinet_column_number,b.cabinet_column_name,a.id,a.cabinet_name,a.cabinet_number FROM energy_cabinet a INNER JOIN energy_cabinet_column b ON a.cabinet_column_id=b.id WHERE a.precinct_id = '{precinct_id}'  ORDER BY b.cabinet_column_number,a.cabinet_number ASC;"
    print(cabinet_list_sql)
    cabinet_list = conn_obj.select(cabinet_list_sql)
    print(cabinet_list)

    #   "device_id"	"device_name"
    #   "00713006000000300210"	"UPS配电0210"
    # todo 这里选择指定设备即可,需要再使用sql查找对应的
    device_list_sql = "SELECT device_id,device_name FROM t_cfg_device WHERE device_model = '00001008000000018855' and CHAR_LENGTH(device_name) > 8;"
    device_list = conn_obj.select(device_list_sql)

    #   meteid                  metecode    showmetename  metekind devicename  roomname                         meteno unit  configdata  configtype-支路  type-支路内  datatype
    mete_list = [
        ['6200900009301000001', '009301', '分路XX相电流Ia', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'A', '1', '1', '2', '1'],
        ['6200900009302000001', '009302', '分路XX相电流Ib', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'A', '1', '2', '2', '1'],
        ['6200900009303000001', '009303', '分路XX相电流Ic', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'A', '1', '3', '2', '1'],
        ['6200900009304000001', '009304', '分路XX相电压Ua', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'V', '1', '1', '1', '1'],
        ['6200900009305000001', '009305', '分路XX相电压Ub', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'V', '1', '2', '1', '1'],
        ['6200900009306000001', '009306', '分路XX相电压Uc', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'V', '1', '3', '1', '1'],
        ['6200900009307000001', '009307', '分路XX有功功率Pa', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'kW', '1', '1', '3', '1'],
        ['6200900009308000001', '009308', '分路XX有功功率Pb', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'kW', '1', '2', '3', '1'],
        ['6200900009309000001', '009309', '分路XX有功功率Pc', '1', 'UPS配电',
         '性能采集测试站点/性能采集测试楼栋/性能采集机房1', '0', 'kW', '1', '3', '3', '1'],
    ]

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "head_orgAccount": "alauda",
        "head_userName": "alauda",
        "head_token": head_token,
        "cookie": cookies
    }

    # cabinet_columns_list = ['测试机柜列02', '测试机柜列03', '测试机柜列04', '测试机柜列05', '测试机柜列06','测试机柜列07']
    cabinet_columns_sql = f"SELECT b.cabinet_column_name FROM energy_cabinet a INNER JOIN energy_cabinet_column b ON a.cabinet_column_id=b.id WHERE a.precinct_id = '{precinct_id}' ORDER BY b.cabinet_column_number,a.cabinet_number ASC;"

    for cabinet_column_name in cabinet_columns_sql:
        # todo 这里控制遍历的sql,如不需要,直接指定设备即可
        # for cabinet_info, device_info in zip(cabinet_list, device_list):
        for cabinet_info in cabinet_list:
            if cabinet_column_name in cabinet_info[2]:
                # 三路支路 - 每支路都有电压，电流，功率
                req = []
                for info in mete_list:
                    data = {
                        "deviceType": 9,
                        "meteId": info[0],
                        "meteCode": info[1],
                        "showMeteName": info[2],
                        "meteKind": info[3],
                        # "deviceId": device_info[0],
                        "deviceId": '00001006000000153964',
                        "deviceName": info[4],
                        "roomName": info[5],
                        "meteName": info[2],
                        "meteNo": info[6],
                        "realName": info[2],
                        "unit": info[7],
                        "precinctId": precinct_id,
                        # "channelId": info[0]+device_info[0],
                        "channelId": info[0] + '00001006000000153964',
                        "configData": info[8],
                        "name": info[5] + '/' + info[4] + '/' + info[2],
                        "configType": info[9],
                        "type": info[10],
                        "cabinetId": cabinet_info[3],
                        "id": "",
                        "cabinetName": cabinet_info[4],
                        "dataType": 1,
                        "upMeteId": info[2]
                    },
                    req += data
                #   json.dumps(req, ensure_ascii=False)
                response = requests.post(url=url, headers=headers, json=req).text
                time.sleep(2)
                # print(mete_list[0][5], cabinet_info[2], cabinet_info[4], device_info[0], device_info[1], response)
                print(mete_list[0][5], cabinet_info[2], cabinet_info[4], '00001006000000153964', 'UPS设备', response)


def make_fsu_device(ip="10.12.12.186", port=8044):
    precinct_id_sql = "SELECT precinct_id FROM t_cfg_precinct WHERE precinct_name like '上海机房%' and precinct_id like \'01-01-08-04-15-%\';"
    precinct_id_list = conn_obj.select(sql=precinct_id_sql)
    print(precinct_id_list)
    for pd in range(len(precinct_id_list)):
        # print(precinct_id_list[pd][0])
        device_id = "00" + str(int("00813006000001768642") + pd)
        device_code = str(2025092201 + pd)
        device_name = f"上海设备2025年{'%05d' % pd}FSU"
        precinct_id = precinct_id_list[pd][0]
        access_device_id = "001" + str(int(device_code))
        insert_device_sql = f"INSERT INTO t_cfg_device(`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`) VALUES ('713', '{device_id}', '{device_name}', '{precinct_id}', 1, NULL, 000, NULL, 13, NULL, 76, 3, NULL, '{device_code}', 1617, 1, NULL, NULL, NULL, '2025-09-22 11:40:14', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 8528903, NULL, NULL, NULL, NULL, NULL, 0, 0, 124, NULL, NULL, NULL, NULL)"
        insert_fsu_sql = f"INSERT INTO t_cfg_fsu(`device_id`, `access_device_id`, `address`, `listen_port`, `up_fsu_id`, `up_link_port`, `net_type`, `net_info`, `fsu_state`, `register_server`, `udp_port`) VALUES ('{device_id}', '{access_device_id}', '{ip}', {port}, NULL, NULL, 0, NULL, 0, '1', NULL)"
        conn_obj.insertone(sql=insert_device_sql)
        conn_obj.insertone(sql=insert_fsu_sql)
        print(f"已经插入：{precinct_id}")
    # for precinct_id in precinct_id_list:
    #     print(precinct_id_list.get[0])
    # pass


def recover():
    """
    恢复 energy_cabinet_attribute_config 表数据
    插入三条分路电流监控配置记录
    """

    # 定义三条 INSERT 语句（保留原始数据）

    cabinet_sql = """SELECT a.id FROM energy_cabinet a INNER JOIN energy_cabinet_column b ON a.cabinet_column_id=b.id WHERE a.precinct_id = '01-01-08-04-07-01-01' and CHAR_LENGTH(a.cabinet_name)>5 AND CHAR_LENGTH(b.cabinet_column_name)>6  AND a.id NOT IN ('4684ed368dbc44caa047886dbc064f14','2ced2ebbef944943919398bbed4089c2') ORDER BY b.cabinet_column_number,a.cabinet_number ASC;"""
    cabinet_info = conn_obj.select(sql=cabinet_sql)
    print(cabinet_info)

    for cab_id in cabinet_info:
        print(cab_id)
        sql_one = """INSERT INTO `energy_cabinet_attribute_config`(`id`, `cabinet_id`, `mete_code`, `mete_no`, `up_mete_id`, `device_id`, `name`,
                                          `power_source`, `config_type`, `type`, `update_time`, `update_user`, `data_type`)
            VALUES('0e984772acd74c79aad78b84816a0004', '50c5ec059d464c5e9817285984f87356', '009303', '0', '分路XX相电流Ic',
                   '00001006000000153964',
                   '性能采集测试站点/性能采集测试楼栋/性能采集机房1/UPS配电/分路XX相电流Ic', NULL, 3, 2,
                   '2025-11-21 15:35:35', 'alauda', '2');"""

        sql_two = """INSERT INTO `energy_cabinet_attribute_config`(`id`, `cabinet_id`, `mete_code`, `mete_no`, `up_mete_id`, `device_id`, `name`,
                                          `power_source`, `config_type`, `type`, `update_time`, `update_user`, `data_type`)
            VALUES('86302e1b38c546ab849e7215b9e6d27f', '50c5ec059d464c5e9817285984f87356', '009302', '0', '分路XX相电流Ib',
                   '00001006000000153964',
                   '性能采集测试站点/性能采集测试楼栋/性能采集机房1/UPS配电/分路XX相电流Ib', NULL, 2, 2,
                   '2025-11-21 15:35:35', 'alauda', '2');"""

        sql_three = """INSERT INTO `energy_cabinet_attribute_config`(`id`, `cabinet_id`, `mete_code`, `mete_no`, `up_mete_id`, `device_id`, `name`,
                                          `power_source`, `config_type`, `type`, `update_time`, `update_user`, `data_type`)
            VALUES('8a50a5d52e3f48a886b5627356b5de2c', '50c5ec059d464c5e9817285984f87356', '009301', '0', '分路XX相电流Ia',
                   '00001006000000153964',
                   '性能采集测试站点/性能采集测试楼栋/性能采集机房1/UPS配电/分路XX相电流Ia', NULL, 1, 2,
                   '2025-11-21 15:35:35', 'alauda', '2');"""

        random_id = uuid.uuid4().hex
        sql_one = sql_one.replace('0e984772acd74c79aad78b84816a0004', random_id)
        sql_one = sql_one.replace('50c5ec059d464c5e9817285984f87356', cab_id[0])
        print(sql_one)
        random_id = uuid.uuid4().hex
        sql_two = sql_two.replace('86302e1b38c546ab849e7215b9e6d27f', random_id)
        sql_two = sql_two.replace('50c5ec059d464c5e9817285984f87356', cab_id[0])
        random_id = uuid.uuid4().hex
        sql_three = sql_three.replace('8a50a5d52e3f48a886b5627356b5de2c', random_id)
        sql_three = sql_three.replace('50c5ec059d464c5e9817285984f87356', cab_id[0])
        conn_obj.insertone(sql=sql_one)
        conn_obj.insertone(sql=sql_two)
        conn_obj.insertone(sql=sql_three)
        print(f"已恢复机柜ID：{cab_id} 的三条分路电流监控配置记录")

# 01-01-08
def insert_history():
    # precinct_id = "01-01-08-07-05-01-02"
    precinct_id = "01-01-08-04-13-01-01"
    # precinct_id = "01-01-08%"
    collect_time = '2026-01-08 14:10:49'
    update_time = '2026-01-08 14:15:49'

    cabinet_sql = f"""SELECT cabinet.id FROM energy_cabinet cabinet LEFT JOIN t_cfg_precinct room ON cabinet.precinct_id = room.precinct_id left join t_cfg_precinct building on room.up_precinct_id = building.precinct_id WHERE room.precinct_id = '{precinct_id}';"""
    # cabinet_sql = f"""SELECT cabinet.id FROM energy_cabinet cabinet LEFT JOIN t_cfg_precinct room ON cabinet.precinct_id = room.precinct_id left join t_cfg_precinct building on room.up_precinct_id = building.precinct_id WHERE room.precinct_id like '{precinct_id}';"""
    cabinet_info = conn_obj.select(sql=cabinet_sql)
    cab = []
    for cab_id in cabinet_info[1:]:
        if cab_id not in cab:
            insert_sql = f"""INSERT INTO `cabinet_history` (`cabinet_id`, `total_current`, `branch1_current`, `branch2_current`, `branch3_current`, `alarm_satisfied`, `collect_time`, `update_time`) VALUES ('{cab_id[0]}', 14, 14, 0, 0, 0, '{collect_time}', '{update_time}');"""
            print(insert_sql)
            conn_obj.insertone(insert_sql)
        cab.append(cab_id)


if __name__ == "__main__":
    # internet
    # make_floor_Internet()
    # make_room_Internet()
    # make_cabinet_columns_Internet()
    # make_cabinet_Internet()
    # make_fsu_device()

    # internet single
    # make_cabinet_columns_Internet_single()
    # make_cabinet_Internet_single()
    # make_mete_Internet_single()
    # make_fsu_mete_sql()

    insert_history()

    # sql
    # make_device_sql()

    # 批量 ->  只需这几步就可以实现 -> 前提设备要有测点
    # make_cabinet_columns_Internet()
    # make_cabinet_Internet_single()
    # make_mete_Internet_single()
    # insert_history()
