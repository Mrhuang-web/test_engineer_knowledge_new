# 先 fsu -> 触发采集 -> 入cabinet_history -> 状态变更1 -> 再统计 -> 产生告警

# INSERT INTO `fsu_point_data_20260108` (`id`, `meteCode`, `deviceId`, `deviceName`, `signalNumber`, `collectTime`, `measureVal`, `unit`, `meteName`, `precinctID`, `precinctName`, `buildingID`, `buildingName`, `create_time`) VALUES (1, '004307', '00713006000000201904', '401-交流母线配电C', '1', '2026-01-08 14:05:00', 11.9, NULL, NULL, '01-25-01-01-01-04-13', NULL, NULL, NULL, '2026-01-08 00:00:00');


import os
import random

import spider_tools.Common.TestEnv as TestEnv
from asptest.common.mysqlpool import MySQLHelper

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
conn_obj = MySQLHelper(TestEnv.ServerConfig['db_pas_sh'])


def insert_fsu_day():
    precinct_id = '01-01-08-07-05-01-02%'

    create_time = '2026-01-08 18:26:55'  # 不用变更
    collect_time = '2026-01-08 18:26:55'

    value = random.randint(5, 8)
    mete_code = ''
    device_id = ''
    mete_no = ''
    selecr_sql_model = f"""SELECT cabinet_conifg.mete_code AS mete_code,cabinet_conifg.device_id,cabinet_conifg.mete_no FROM energy_cabinet_attribute_config as cabinet_conifg LEFT JOIN energy_cabinet as cabinet ON cabinet_conifg.cabinet_id = cabinet.id WHERE cabinet.precinct_id like '{precinct_id}'"""
    selecr_data_model = conn_obj.select(sql=selecr_sql_model)

    for config in selecr_data_model:
        fsu_max_id = """SELECT max(id) FROM fsu_point_data_20260108"""

        id = conn_obj.select(sql=fsu_max_id)

        if id[0][0] is None:
            id = ((1),)
            ids = id[0]
        else:
            ids = id[0][0]
            ids += 1

        mete_code = config[0]
        device_id = config[1]
        mete_no = config[2]
        insert_sql_model = f"""INSERT INTO fsu_point_data_20260108 (id, meteCode, deviceId, deviceName, signalNumber, collectTime, measureVal, unit, meteName, precinctID, precinctName, buildingID, buildingName, create_time) VALUES ({ids}, '{mete_code}', '{device_id}', '401-交流母线配电C', '{mete_no}', '{collect_time}', '{value}', NULL, NULL, '01-25-01-01-01-04-13', NULL, NULL, NULL, '{create_time}');"""

        conn_obj.select(sql=insert_sql_model)


if __name__ == "__main__":
    insert_fsu_day()
