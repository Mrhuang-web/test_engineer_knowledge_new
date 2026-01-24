import os
import time

import requests
import spider_tools.Common.TestEnv as TestEnv
from asptest.common.mysqlpool import MySQLHelper
from spider_tools.Common.all_excelCase_file_path import load_excel_data

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
work = os.path.join(ROOT_PATH, "Params", "upload", "room_name.csv")
conn_obj = MySQLHelper(TestEnv.ServerConfig['db_pas_sh'])


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
