import os
import time

import requests
import spider_tools.Common.TestEnv as TestEnv
from asptest.common.mysqlpool import MySQLHelper
from spider_tools.Common.all_excelCase_file_path import load_excel_data

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
work = os.path.join(ROOT_PATH, "Params", "upload", "room_name.csv")
conn_obj = MySQLHelper(TestEnv.ServerConfig['db_pas_sh'])


def make_room():
    """创建批量机房"""

    # 方式1：文件读取
    # file = open(file=work, mode='r', encoding='utf-8')
    # data = file.read()
    # 方式2：少量直接列表写入
    rooms = ['性能采集机房1', '性能采集机房2', '性能采集机房3', '性能采集机房4', '性能采集机房5',
             '性能采集机房6', '性能采集机房7', '性能采集机房8', '性能采集机房9', '性能采集机房10',
             '性能采集机房11', '性能采集机房12', '性能采集机房13', '性能采集机房14', '性能采集机房15',
             '性能采集机房16', '性能采集机房17', '性能采集机房18', '性能采集机房19', '性能采集机房20',
             '性能采集机房21', '性能采集机房22', '性能采集机房23', '性能采集机房24', '性能采集机房25',
             '性能采集机房26', '性能采集机房27', '性能采集机房28', '性能采集机房29', '性能采集机房30',
             '性能采集机房31', '性能采集机房32', '性能采集机房33', '性能采集机房34', '性能采集机房35',
             '性能采集机房36', '性能采集机房37', '性能采集机房38', '性能采集机房39', '性能采集机房40',
             ]

    url = "http://10.1.203.120:9081/spider/web/v1/configManagement/saveStationPrecinct?namespace=alauda"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "head_orgAccount": "alauda",
        "head_userName": "alauda",
        "Cookie": "SESSION=NTEzMGYxZWUtZWM4Ny00YWI0LTg5MTItNzg4NzNiYzNmZTY1; JSESSIONID=38E25E5023E67296273CBD09EFF5067C"
    }
    # for name in data.split('\n'):
    for name in rooms:
        print(f"开始创建机房：{name}\n")
        data = {
            "upPrecinctId": "01-01-08-07-05-01",
            "precinctId": "",
            "precinctName": f"{name}",
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
        time.sleep(5)
        print(response)


def make_fsu_device(ip="10.12.12.186", port=8080):
    """创建批量FSU设备 - 每个机房10个FSU"""
    """ device_code对应fsu_id """

    precinct_id_sql = "SELECT precinct_id FROM t_cfg_precinct WHERE precinct_id like '01-01-08-07-05-01%' and precinct_kind='5';"
    precinct_id_list = conn_obj.select(sql=precinct_id_sql)
    ftp_proxy = 1
    batch = 0

    # province_index : 对应省份的缩写 -> 0101 -> 就是101 即广东
    for pd in range(0, len(precinct_id_list)):
        for num in range(1):
            device_id = "00" + str(int("00100006011001768642") + pd + num + batch)  # 这里需要倍数增加
            device_code = str(2025000000000 + num + pd + batch)
            device_name = f"2025年{'%04d' % pd}FSU"
            precinct_id = precinct_id_list[pd][0]
            access_device_id = "001" + str(int(device_code))
            insert_device_sql = f"INSERT INTO t_cfg_device(`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`) VALUES ('713', '{device_id}', '{device_name}', '{precinct_id}', 1, NULL, 000, NULL, 13, NULL, 76, 3, NULL, '{device_code}', 1617, 1, NULL, NULL, NULL, '2024-01-30 11:40:14', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 8528903, NULL, NULL, NULL, NULL, NULL, 0, 0, 124, NULL, NULL, NULL, NULL)"
            insert_fsu_sql = f"INSERT INTO t_cfg_fsu(`device_id`, `access_device_id`, `address`, `listen_port`, `up_fsu_id`, `up_link_port`, `net_type`, `net_info`, `fsu_state`, `register_server`, `udp_port`,`new_version`,`user_name`,`pass_word`,`ftp_port`,`ftp_proxy`,http_proxy_url,fsu_origin_code) VALUES ('{device_id}', '{access_device_id}', '{ip}', {port}, NULL, NULL, 0, NULL, 0, '1', NULL, 0, NULL, NULL, NULL, {ftp_proxy}, NULL, NULL)"
            conn_obj.insertone(sql=insert_device_sql)
            conn_obj.insertone(sql=insert_fsu_sql)
            print(f"已经插入：{precinct_id}")
        batch += 10


def update_fsu_device():
    precinct_id = '01-01-08-07-05-01'
    device_id = '006011001768'
    fsu_id_sql = f"select device_id from t_cfg_device where device_id like '%{device_id}%' and precinct_id like '{precinct_id}%';"
    fsu_id_sql_list = conn_obj.select(sql=fsu_id_sql)
    for item in range(0, len(fsu_id_sql_list)):
        update_fsu_sql = f"update t_cfg_fsu set address = '10.1.4.194', listen_port = '{8200 + item}', http_proxy_url = NULL where device_id = '{fsu_id_sql_list[item][0]}';"
        conn_obj.select(sql=update_fsu_sql)


def ip_table_rule():
    # 服务器IP和端口段白名单生成
    start_ip = 33  # 10.9.223.33
    start_port = 8201  # 第一组起始端口
    rules = 5
    ports_per_rule = 10

    for i in range(rules):
        ip = f"10.9.223.{start_ip}"
        port_list = list(range(start_port + i * ports_per_rule,
                               start_port + (i + 1) * ports_per_rule))
        port_str = ",".join(map(str, port_list))
        print(f"-A INPUT -s {ip} -p tcp -m multiport --dport {port_str} -j ACCEPT")

def delete_fsu_device():
    device_id = '006011001768'
    precinct_id = '01-01-08-07-05-01'
    delete_device_sql = f"DELETE FROM t_cfg_device WHERE device_id like '%{device_id}%' and precinct_id like '{precinct_id}%';"
    delete_fsu_sql = f"DELETE FROM t_cfg_fsu WHERE device_id like '%{device_id}%' ;"
    conn_obj.select(sql=delete_device_sql)
    conn_obj.select(sql=delete_fsu_sql)


if __name__ == '__main__':
    # delete_fsu_device()
    # make_room()
    # make_fsu_device()
    update_fsu_device()
    # ip_table_rule()
