# encoding:utf-8
"""
@CreateTime:      2025/5/8 17:01
@Author:          Tsuiguangchun
@FileName:        [广西]testRoomData.py
@IDE_SoftWare:    PyCharm
@description:    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from asptest.common.mysqlpool import MySQLHelper
from aspire.DateTimeLibs import get_current_time
from spider_tools.Common.esdata import esDB, lastThreeDays
from loguru import logger
import spider_tools.Common.TestEnv as TestEnv
import time
import uuid, hashlib


class DHToZZ(object):
    # 用电估算只有广西有，广西传electric_estimate：True执行
    # t_zz_space_resources：空间表，包括机房、站点,需要注意city_id和country_id，通过precinct_id和t_cfg_precinct表的precinct_id关联
    # t_zz_power_specialty：站点属性报表，通过站点id（ini_id）关联t_zz_space_resources的站点的res_code，有一个站点类型属性（site_type）
    # t_zz_power_device：设备主表，通过device_id和t_cfg_device的device_id关联。这表res_code和其它表没有关联，这个是综资的主键id,造数据使用动环resource_code关联传值
    electric_estimate = False
    # 站点
    precinctId = '01-01-15-04-11'

    def __init__(self, env='db_pas_gx'):
        self.conn_obj = MySQLHelper(TestEnv.ServerConfig[env])
        check_space_sql = f"""SELECT * FROM t_zz_space_resources WHERE precinct_id like '{self.precinctId}%';"""
        check_space = self.conn_obj.select(sql=check_space_sql, isdict=True)
        logger.debug(f'check_space_data:{check_space}')
        if len(check_space) > 0:
            logger.info(f'当前站点存在，准备开始清楚已有数据')
            self.conn_obj.delete(sql=f"DELETE FROM t_zz_space_resources WHERE precinct_id like '{self.precinctId}%';")
            self.conn_obj.delete(
                sql="DELETE FROM t_zz_space_resources WHERE zh_label like '%auto%';")
            self.conn_obj.delete(sql="DELETE FROM t_zz_power_device WHERE product_name like 'AUTOTEST001%';")
            self.conn_obj.delete(sql="DELETE FROM t_zz_power_device_sys WHERE zh_label like '%auto%';")
            self.conn_obj.delete(sql="DELETE FROM t_zz_switch_power where res_code like '161_%';")
            self.conn_obj.delete(sql="DELETE FROM t_cfg_devicesys where devicesys_id like 'auto%';")
            self.conn_obj.delete(sql="DELETE FROM t_zz_smart_meter where res_code like '161_%';")
            self.conn_obj.delete(sql="DELETE FROM t_cfg_devicesys_detail where devicesys_id like 'auto%';")

            self.conn_obj.delete(sql="DELETE FROM t_zz_power_specialty where product_name like 'AUTOTEST001%' or zh_label like '%auto%';")
            self.conn_obj.delete(sql=f"DELETE FROM t_cfg_devicesys where up_id like '{self.precinctId}%';")
            self.conn_obj.delete(
                sql=f"DELETE FROM t_cfg_devicesys_detail where sub_id in (select device_id from t_cfg_device where precinct_id like '{self.precinctId}%' and device_type = 6);")
            if self.electric_estimate:
                self.conn_obj.delete(sql="DELETE FROM t_device_link where id like 'auto%';")
                self.conn_obj.delete(sql=f"DELETE FROM capacity_electric_estimate where site_id like '{self.precinctId}%';")
                self.conn_obj.delete(
                    sql=f"DELETE FROM capacity_electric_budget where estimate_id in (SELECT id FROM capacity_electric_estimate WHERE site_id like '{self.precinctId}%');")
                self.conn_obj.delete(
                    sql=f"DELETE FROM capacity_electric_budget_device where budget_id in (select b.id from capacity_electric_budget b, capacity_electric_estimate a where a.site_id like '{self.precinctId}%' and a.id = b.estimate_id);")

        time.sleep(10)

    def check_insert_zz(self):
        """
        动环站点机房设备数据转入综资表，匹配关联。
        当前关联适用广西平台，其他平台可能匹配规则不一样应该差别不大，也可能其他省的综资数据库表结构不一致导致
        插入失败
        """

        date_time = get_current_time('%Y-%m-%d %H:%M:%S')
        date = get_current_time('%Y%m%d')
        site_type = self.conn_obj.selectone(sql=f"SELECT site_id,site_type FROM t_cfg_site where site_id = '{self.precinctId}'",
                                isdict=True)['site_type']
        site_precinct = f"""SELECT precinct_id,precinct_name,resource_code,description FROM t_cfg_precinct WHERE precinct_id like '{self.precinctId}%' and precinct_kind = 2;"""
        # site_precinct = """SELECT precinct_id,precinct_name,resource_code,description FROM t_cfg_precinct WHERE precinct_name like '广西auto%' and precinct_kind = 2;"""
        # room_precinct = """SELECT precinct_id,precinct_name,resource_code FROM t_cfg_precinct WHERE precinct_name like '广西auto%' and precinct_kind = 5;"""
        # site_precinct_name = self.conn_obj.select(sql=site_precinct, isdict=True)
        site_precinct = self.conn_obj.select(sql=site_precinct, isdict=True)
        if site_precinct:
            # try:
            for precinct in site_precinct:  # 站点
                relate_site = f'SITE-{str(uuid.uuid4())[8:]}'
                city_id = precinct['precinct_id'][:8]
                area_id = precinct['precinct_id'][:11]
                site_id = precinct['precinct_id']
                site_name = precinct['precinct_name']
                power_site_level = precinct['description']
                res_code = precinct['resource_code']
                city_name_sql = f"""SELECT precinct_id,precinct_name FROM t_cfg_precinct WHERE precinct_id = '{city_id}';"""
                area_name_sql = f"""SELECT precinct_id,precinct_name FROM t_cfg_precinct WHERE precinct_id = '{area_id}';"""
                city_name = self.conn_obj.select(city_name_sql, isdict=True)[0]['precinct_name']
                area_name = self.conn_obj.select(area_name_sql, isdict=True)[0]['precinct_name']
                logger.info(city_id, area_id, site_id, site_name, city_name, area_name)
                site_insert_sql = f"""INSERT INTO t_zz_space_resources (data_time, precinct_id, int_id, zh_label, space_type, city_id, county_id, create_time )
                                    VALUES('{date}' , '{site_id}', '{relate_site}', '{site_name}', 101, '{city_name[:-1]}', '{area_name}', '{date_time}' );"""
                device_specialty_sql = f"""INSERT INTO t_zz_power_specialty (
                                                `res_code`,
                                                `zh_label`,
                                                `data_time`,
                                                `device_type_id`,
                                                `power_site_level`,
                                                `create_time`,
                                                `site_type`
                                            )
                                            VALUES
                                                (
                                                    '{relate_site}',
                                                    '{site_name}',
                                                    '{date}',
                                                    0,
                                                    '{power_site_level}',
                                                    '{date_time}',
                                                    {site_type}
                                                );"""
                logger.info(f'开始写入综资设备信息：{device_specialty_sql}')
                self.conn_obj.insertone(site_insert_sql)
                self.conn_obj.insertone(device_specialty_sql)
                # zz_admin_area_sql = f"""INSERT INTO zz_admin_area(`zz_city_id`, `zz_county_id`, `precinct_id`, `city_name`) VALUES ('{city_name}', '{area_name}', '{city_id}', '{city_name}');"""

                logger.info(f'开始写入:将动环站点写入综资站点信息:{site_insert_sql}')

                room_precinct_sql = f"""SELECT precinct_id,precinct_name,resource_code FROM t_cfg_precinct WHERE precinct_id like '{site_id}%' and precinct_kind = 5;"""
                room_precinct = self.conn_obj.select(room_precinct_sql, isdict=True)
                if room_precinct:
                    for room in room_precinct:  # 机房
                        room_id = room['precinct_id']
                        room_name = room['precinct_name']
                        room_resource_code = room['resource_code']
                        relate_room = f'ROOM-{uuid.uuid4()}'

                        room_insert_sql = f"""INSERT INTO t_zz_space_resources ( `data_time`, `precinct_id`, `int_id`, `zh_label`, `related_site`, `space_type`, `city_id`, `county_id`, `create_time` )
                                                                                VALUES
                                                                                    ( '{date}','{room_id}', '{relate_room}', '{room_name}', '{relate_site}', 102, '{city_name[:-1]}', '{area_name}', '{date_time}' );"""
                        logger.info(f'开始写入:将动环机房写入综资机房信息：{room_insert_sql}')
                        self.conn_obj.insertone(sql=room_insert_sql)

                        device_sql = f"""SELECT * FROM t_cfg_device WHERE precinct_id = '{room_id}';"""
                        logger.info(f'device_sql:{device_sql}')
                        device_list = self.conn_obj.select(sql=device_sql, isdict=True)
                        node_num = 1
                        code_num = 1
                        for device in device_list:  # 机房设备
                            device_name = device['device_name']
                            device_id = device['device_id']
                            device_type_id = device['device_type']
                            device_model = device['device_model']
                            device_code = device['device_code'] if device['device_code'] else None
                            manufacturer_name = device['manufacturer_name']
                            resource_code = device['resource_code']
                            logger.info(f'device_name:{device_name}, device_id:{device_id}, device_type:{device_type_id}',
                                        f'manufacturer_name:{manufacturer_name}', device_model, resource_code)
                            device_belong_type_sql = f"""SELECT dict_id,dict_note FROM t_cfg_dict WHERE dict_code = {device_type_id} and col_name = 'device_type';"""
                            logger.info(f'device_belong_type_sql:{device_belong_type_sql}')
                            device_type_dictId = self.conn_obj.select(sql=device_belong_type_sql, isdict=True)[0]['dict_id']
                            device_type_name = self.conn_obj.select(sql=device_belong_type_sql, isdict=True)[0]['dict_note']
                            sub_device_type_sql = f"""SELECT * FROM t_cfg_dict WHERE dict_code = {device_type_id} and up_dict = {device_type_dictId} and col_name = 'sub_device_type';"""
                            logger.info(f'sub_device_type_sql:{sub_device_type_sql}')
                            sub_device_type_name_list = self.conn_obj.select(sql=sub_device_type_sql, isdict=True)
                            sub_device_type_name = sub_device_type_name_list[0][
                                'dict_note'] if sub_device_type_name_list else device_name
                            if resource_code is None:
                                self.conn_obj.update(
                                    sql=f"update t_cfg_device set resource_code = '{room_resource_code}_{device_type_id}{code_num}' where device_id = '{device_id}';")
                            code_num += 1
                            if resource_code:
                                device_insert_sql = f"""
                                                        INSERT INTO t_zz_power_device (
                                                            `res_code`,
                                                            `zh_label`,
                                                            `data_time`,
                                                            `device_id`,
                                                            `device_type_id`,
                                                            `device_type`,
                                                            `device_code`,
                                                            `related_site`,
                                                            `related_room`,
                                                            `lifecycle_status`,
                                                            `rated_power`,
                                                            `device_subclass`,
                                                            `start_time`,
                                                            `product_name`,
                                                            `vendor_id`,
                                                            `power_device_id`,
                                                            `power_site_level`,
                                                            `estimated_retirement_time`,
                                                            `sys_no_uuid`,
                                                            `create_time` 
                                                        )
                                                        VALUES
                                                            (
                                                                '{resource_code}',
                                                                '{device_name}',
                                                                '{date}',
                                                                '{device_id}',
                                                                {device_type_id},
                                                                '{device_type_name}',
                                                                '{device_code}',
                                                                '{relate_site}',
                                                                '{relate_room}',
                                                                '工程',
                                                                NULL,
                                                                '{sub_device_type_name}',
                                                                '{get_current_time('%Y-%m-%d')}',
                                                                'AUTOTEST001',
                                                                '{manufacturer_name}',
                                                                '{device_id}',
                                                                NULL,
                                                                '2029-07-31',
                                                                '54001',
                                                                '{date_time}' 
                                                            );"""
                                # t_zz_power_specialty表最后一个 ralated_power_device删除了，需要手动加
                                device_specialty_sql = f"""INSERT INTO t_zz_power_specialty (
                                        `res_code`,
                                        `zh_label`,
                                        `data_time`,
                                        `device_id`,
                                        `device_type_id`,
                                        `device_type`,
                                        `device_code`,
                                        `related_site`,
                                        `related_room`,
                                        `lifecycle_status`,
                                        `rated_power`,
                                        `device_subclass`,
                                        `start_time`,
                                        `product_name`,
                                        `vendor_id`,
                                        `power_device_id`,
                                        `power_site_level`,
                                        `estimated_retirement_time`,
                                        `create_time`,
                                        `sys_no_uuid`,
                                        `city_id`,
                                        `county_id`,
                                        `site_type`
                                    )
                                    VALUES
                                        (
                                        '{relate_site}',
                                        '{device_name}',
                                        '{date}',
                                        NULL,
                                        6,
                                        '{device_type_name}',
                                        '{device_code}',
                                        '{relate_site}',
                                        '{relate_room}',
                                        '工程',
                                        NULL,
                                        '{sub_device_type_name}',
                                        '{get_current_time('%Y-%m-%d')}',
                                        'AUTOTEST001',
                                        '中国移动集团设计院',
                                        'db7758536b8',
                                        '{power_site_level}',
                                        '2036-02-20',
                                        '{date_time}',
                                        '54002',
                                        '{city_id}',
                                        '{area_id}',
                                        {site_type}
                                        );"""
                                logger.info(f'开始写入综资设备信息：{device_specialty_sql}')
                                self.conn_obj.insertone(device_insert_sql)
                                # 不清楚设备要不要放到‘站点属性表’，设备插入主键冲突，注释了(1062, "Duplicate entry 'SITE--b229-4b61-ab2a-636bbbf67dd8-6' for key 'uq_res_code'")
                                # self.conn_obj.insertone(device_specialty_sql)

                                t_zz_power_device_sys_sql = f"""select * from t_zz_power_device_sys where related_room = '{relate_room}';"""
                                check_room_device_sys = self.conn_obj.select(sql=t_zz_power_device_sys_sql, isdict=True)

                                if device_type_id == 6 and len(check_room_device_sys) == 0:  # 插入综资202开关电源系统，201UPS系统
                                    system_id = f"auto{str(uuid.uuid4())[8:]}"
                                    node_num += 1 if node_num >= 3 else node_num == 3
                                    logger.info(f'开始写入：{room_name}开关电源系统！')
                                    zz_switch_sql = f"""INSERT INTO t_zz_switch_power ( `res_code`, `signal_output_rated_capacity`, `related_system`, `total_rack_match_modules`, `create_time` )
                                                        VALUES
                                                            ( '{resource_code}', '100', '{device_name}', '20', '{date_time}');"""
                                    zz_link_sql = f"""INSERT INTO t_device_link ( `id`, `device_name`, `down_device_name`, `device_type`, `parent_device_name`, `parent_device_type`, `site_id`, `room_id`, `device_id`, `create_time` )
                                                        VALUES
                                                            ( '{system_id}', '{device_name}', '{resource_code}', '{device_type_name}', '{device_name}_p', '{device_type_name}', '{relate_site}', '', NULL, '{date_time}' );"""
                                    logger.info(f"zz_link_sql:{zz_link_sql}")
                                    zz_smart_sql = f"""INSERT INTO t_zz_smart_meter( `res_code`, `collected_device`, `create_time` )
                                                        VALUES
                                                            ( '{resource_code}', '{device_name}', '{date_time}' );"""
                                    deviceSys_detail_sql = f"""INSERT INTO t_cfg_devicesys_detail (`devicesys_id`, `sub_id`, `scc_index`, `cell_index`, `cell_num`) 
                                                        VALUES ('{system_id}', '{device_id}', NULL, NULL, NULL);"""
                                    # `pe_entity_type` int(11) DEFAULT NULL COMMENT '设备系统类型', 1ups,3开关电源
                                    deviceSys_sql = f"""INSERT INTO t_cfg_devicesys(
                                                    `devicesys_id`,
                                                    `up_id`,
                                                    `devicesys_name`,
                                                    `devicesys_code`,
                                                    `devicesys_desc`,
                                                    `is_hide_device`,
                                                    `flag`,
                                                    `updateTime`,
                                                    `pe_entity_type`,
                                                    `work_style`,
                                                    `unit`,
                                                    `ktRatio`,
                                                    `current_ele`,
                                                    `resource_origin`,
                                                    `resource_code`,
                                                    `resource_name`,
                                                    `purpose`,
                                                    `sys_voltage`,
                                                    `sys_device_number`,
                                                    `design_reserve_length`,
                                                    `battery_number`,
                                                    `max_discharge_current`,
                                                    `battery_capacity`,
                                                    `confirm_content`,
                                                    `confirm_time` 
                                                )
                                                VALUES
                                                    (
                                                        '{system_id}',
                                                        '{site_id}',
                                                        '{device_type_name}',
                                                        '{device_name}',
                                                        NULL,
                                                        1,
                                                        NULL,
                                                        '{date_time}',
                                                        3,
                                                        '0',
                                                        NULL,
                                                        0.2,
                                                        NULL,
                                                        NULL,
                                                        '{site_id}_{device_name}',
                                                        NULL,
                                                        '1',
                                                        NULL,
                                                        NULL,
                                                        NULL,
                                                        NULL,
                                                        NULL,
                                                        NULL,
                                                        NULL,
                                                NULL 
                                                    );"""
                                    # 倒数第二个的ralated_power_device已被删除，需要自行加回，对应value值{system_id}
                                    device_power_sys_sql = f"""INSERT INTO t_zz_power_device_sys (
                                                        `res_code`,
                                                        `zh_label`,
                                                        `data_time`,
                                                        `device_id`,
                                                        `device_type_id`,
                                                        `device_type`,
                                                        `device_code`,
                                                        `related_site`,
                                                        `related_room`,
                                                        `lifecycle_status`,
                                                        `rated_power`,
                                                        `device_subclass`,
                                                        `start_time`,
                                                        `product_name`,
                                                        `vendor_id`,
                                                        `power_device_id`,
                                                        `power_site_level`,
                                                        `gx_power_site_level`,
                                                        `estimated_retirement_time`,
                                                        `sys_no_uuid`,
                                                        `city_id`,
                                                        `county_id`,
                                                        `province_id`,
                                                        `asset_code`,
                                                        `device_brand`,
                                                        `power_monitor_dev_name`,
                                                        `power_room_type`,
                                                        `serial_number`,
                                                        `accept_date`,
                                                        `factory_number`,
                                                        `upper_device_name`,
                                                        `upper_device_type`,
                                                        `create_time`
                                                    )
                                                    VALUES
                                                        (
                                                            '{resource_code}',
                                                            '中恒开关电源系统auto',
                                                            '{date}',
                                                            NULL,
                                                            202,
                                                            '{device_type_name}',
                                                            '{device_code}',
                                                            '{relate_site}',
                                                            '{relate_room}',
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            '{city_id}',
                                                            '{area_id}',
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            NULL,
                                                            '{date_time}'
                                                        );"""

                                    self.conn_obj.insertone(sql=zz_smart_sql)
                                    self.conn_obj.insertone(sql=zz_switch_sql)

                                    # 用电评估是广西的功能，传electric_estimate：True执行
                                    # `charge_type`tinyint(1)'加电类型:1:交流/2:直流',
                                    if self.electric_estimate:
                                        # 插入系统设备
                                        self.conn_obj.insertone(sql=deviceSys_detail_sql)
                                        self.conn_obj.insertone(sql=deviceSys_sql)
                                        self.conn_obj.insertone(sql=device_power_sys_sql)

                                        capacity_electric_estimate_sql = f""" INSERT INTO capacity_electric_estimate ( `site_id`, `room_id`, `charge_type`, `rated_vout`, `electric_device_type`, `electric_device_rated_power`, `electric_device_name`, `status`, `message`, `create_time` )
                                        VALUES( '{site_id}', '{room_id}', 2, '24V', 1, '100', '{device_name}', 2, NULL, '{date_time}' );"""
                                        logger.info(f'capacity_electric_estimate_sql:{capacity_electric_estimate_sql}')
                                        self.conn_obj.insertone(capacity_electric_estimate_sql)
                                        estimate_id_sql = f"""SELECT id FROM capacity_electric_estimate WHERE site_id = '{site_id}'"""
                                        estimate_id_list = self.conn_obj.select(estimate_id_sql, isdict=True)
                                        # 查询评估ID

                                        # estimate_id_sql = f"""SELECT * FROM capacity_electric_budget WHERE estimate_id IN (
                                        # SELECT id FROM capacity_electric_estimate WHERE site_id = '{site_id}' );"""

                                        if len(estimate_id_list) > 0:
                                            estimate_id = estimate_id_list[0]['id']
                                            capacity_electric_budget = f"""INSERT INTO capacity_electric_budget (
                                                                                    `estimate_id`,
                                                                                    `system_type`,
                                                                                    `system_name`,
                                                                                    `system_rated_capacity`,
                                                                                    `rated_capacity_flag`,
                                                                                    `current_ele_flag`,
                                                                                    `actual_load_current`,
                                                                                    `charge_current`,
                                                                                    `system_load_capacity`,
                                                                                    `system_load_rate`,
                                                                                    `system_charge_load`,
                                                                                    `system_charge_load_rate`,
                                                                                    `evaluate_time`,
                                                                                    `best_sort`,
                                                                                    `create_time` 
                                                                                )
                                                                                VALUES
                                                                                    (
                                                                                        {estimate_id},
                                                                                        2,
                                                                                        '中恒开关电源系统56',
                                                                                        '1900',
                                                                                        2,
                                                                                        NULL,
                                                                                        NULL,
                                                                                        NULL,
                                                                                        NULL,
                                                                                        NULL,
                                                                                        '4166.667',
                                                                                        '2.193',
                                                                                        '{date_time}',
                                                                                        1,
                                                                                        '{date_time}' 
                                                                                );"""
                                            self.conn_obj.insertone(sql=capacity_electric_budget)
                                            budget_id_list = self.conn_obj.select(
                                                sql=f"""select id from capacity_electric_budget where estimate_id={estimate_id};""",
                                                isdict=True)
                                            if len(budget_id_list) > 0:
                                                # 预算设备
                                                budget_id = budget_id_list[0]['id']
                                                budget_device_sql = f"""INSERT INTO capacity_electric_budget_device ( `budget_id`, `device_type`, `device_name`, `parent_device_name`, `device_rated_capacity`, `device_load`, `device_load_rate`, `device_charge_load`, `device_charge_load_rate`, `node_level`, `number`, `create_time` )
                                                                            VALUES( '{budget_id}', '{device_type_name}', '{device_name}', '{device_name}auto/{node_num}', '1250', NULL, NULL, '100.000', NULL, '1-{node_num}', {node_num}, '{date_time}' )"""
                                                self.conn_obj.insertone(sql=budget_device_sql)
                                                self.conn_obj.insertone(sql=zz_link_sql)

                                else:
                                    logger.info('无需插入综资设备系统')

        else:
            logger.info("未能找到对应站点机房信息")
            # logger.info( f'city_name:{city_name}, area_name:{area_name}, site_name:{site_name}, relate_site:{
            # relate_site}, relate_room:{relate_room}')


class RoomData(object):

    def __init__(self, env='db_pas_gx'):
        self.conn_obj = MySQLHelper(TestEnv.ServerConfig[env])

    def all_deviceType_esData(self, precinct_id='01-07-05-02-41-01', device_type=(6, 92), day=3, env='sx',
                              formula_config=False):
        """
        批量写入设备所有测点的es数据
        :param precinct_id:机房
        :param device_type:设备类型ID，单个或者多个（6，23）
        :day:
        :env:
        :param formula_config:True/False,如果Ture时查询当前站点或机房用电关系公式的设备测点写入ES数据，如计算能耗
        """
        # # -----------------------------------------------以下批量写入设备测点信息---------------------------------

        # precinct_id = '01-02-10-04-43-01'
        # precinct_id = "01-24-04-07-19%"
        date_list = lastThreeDays(day)
        # date_list = ['2024-05-09', '2024-05-10', '2024-05-11', '2024-05-12']

        mens = 20
        logger.info(date_list)
        if formula_config:
            energy_formula_config_sql = f"""SELECT * FROM energy_formula_config WHERE belong_station='{precinct_id}';"""
            # energy_formula_config_sql = f"""SELECT * FROM energy_formula_config WHERE belong_station=(SELECT precinct_id
            #                             FROM t_cfg_precinct WHERE precinct_id like'{precinct_id}%');"""
            logger.info(f'energy_formula_config_sql:{energy_formula_config_sql}')
            energy_formula_config_list = self.conn_obj.select(sql=energy_formula_config_sql, isdict=True)
            # logger.info(energy_formula_config_list)
            if len(energy_formula_config_list) > 0:
                for date in date_list:
                    for formula_config in range(len(energy_formula_config_list)):
                        device_id1 = energy_formula_config_list[formula_config].get('device_id1')
                        mete_code1 = energy_formula_config_list[formula_config].get('mete_code1')
                        logger.info(f'device_id1:{device_id1}', f'mete_code1:{mete_code1}')
                        if device_id1 is None:
                            break
                        esDB(precinct_id=precinct_id, mete_code=mete_code1, imdate=date,
                             minval=mens, maxval=mens + 100.5, device_id=device_id1,
                             env=env).insert_esdata_device_batch(is_changing=True, timedelta_min=60, stepnum=2)
                        mens = mens + 100

        # 根据当前的机房对应设备，找到对应设备模版详情表存在的所有测点meteCode写入历史数据，当前插入前三天的测点数据，间隔30分钟一条，即是一个测点一天插入48条数据
        else:
            if isinstance(device_type, tuple):
                device_info_sql = f"SELECT device_id,device_model FROM t_cfg_device where device_type in {device_type} and precinct_id like '{precinct_id}';"
            else:
                device_info_sql = f"SELECT device_id,device_model FROM t_cfg_device where device_type = {device_type} and precinct_id like '{precinct_id}';"
            logger.info(device_info_sql)
            device_info_list = self.conn_obj.select(sql=device_info_sql, isdict=True)
            logger.info(f'device_info_list:{device_info_list}', end='---' * 30 + '\n')

            for device_info in device_info_list:
                logger.info('device_info:', device_info['device_id'], device_info['device_model'])
                mete_code_sql = f"SELECT mete_code FROM t_cfg_metemodel_detail WHERE model_id = {device_info['device_model']};"
                logger.info(mete_code_sql, end='---' * 30 + '')
                mete_code_list = self.conn_obj.select(sql=mete_code_sql, isdict=True)
                logger.info(f'mete_code_list:{mete_code_list}', end='---' * 30 + '\n')

                for date in date_list:
                    date_time = date
                    for mete_code in mete_code_list:
                        esDB(precinct_id=precinct_id, mete_code=mete_code['mete_code'], imdate=date_time,
                             minval=mens, maxval=mens + 17.5, device_id=device_info['device_id'],
                             env=env).insert_esdata_device_batch(is_changing=True, timedelta_min=60, stepnum=2)
                        # mete_code['mete_code']
                        mens = mens + 1
                        if mete_code['mete_code'] in ('011301', '012301', '013301', '015301', '017301'):
                            if mens > 28:
                                mens = 20

    def room_deviceModelDetail_insert(self, device_type, precinct_id):

        """
        回填机房有设备但是没有测点数据
        ？model_detail表里的测点的mete_id关联是什么表
        """
        if isinstance(device_type, tuple):
            device_info_sql = f"SELECT device_id,device_model FROM t_cfg_device where device_type in {device_type} and precinct_id like '{precinct_id}';"
            mete_info_sql = f"SELECT * FROM t_cfg_mete WHERE device_type in {device_type} and precinct_id like '{precinct_id}';"
        else:
            device_info_sql = f"SELECT device_id,device_model FROM t_cfg_device where device_type = {device_type} and precinct_id like '{precinct_id}';"
            mete_info_sql = f"SELECT * FROM t_cfg_mete WHERE device_type = {device_type} and precinct_id like '{precinct_id}'; "
        logger.info(device_info_sql, mete_info_sql)
        device_info_list = self.conn_obj.select(sql=device_info_sql, isdict=True)
        device_mete_list = self.conn_obj.select(sql=mete_info_sql, isdict=True)
        logger.info(f'device_info_list:{device_info_list}', end='---' * 30 + '\n')

        for device_info in device_info_list:
            device_id = device_info['device_id']
            device_model = device_info['device_model']
            for mete_info in device_mete_list:
                mete_code = mete_info['mete_code']
                insert_model_detail_sql = f"INSERT INTO"


if __name__ == '__main__':
    zz_dh = DHToZZ(env='db_pas_chongqing')
    zz_dh.check_insert_zz()

    # 造设备历史ES数据
    # room_data = RoomData(env='db_pas_guangdong')
    # room_data.all_deviceType_esData(precinct_id='01-01-23-03-09', device_type=92, day=7, formula_config=True,env='guangdong')
