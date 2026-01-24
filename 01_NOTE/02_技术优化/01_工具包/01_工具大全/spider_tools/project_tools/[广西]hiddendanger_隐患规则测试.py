# encoding:utf-8
"""
@CreateTime:      2025/6/4 16:55
@Author:          Tsuiguangchun
@FileName:        hiddendanger_隐患规则测试.py
@IDE_SoftWare:    PyCharm
@description:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import copy
import json
import os
from loguru import logger
from asptest.common.mysqlpool import MySQLHelper
import spider_tools.Common.TestEnv as TestEnv
import requests
import time

# print(TestEnv.ServerConfig)
conn_obj = MySQLHelper(TestEnv.ServerConfig["db_pas_guangxi"])


class GxYinH(object):
    # device_id = None
    # device_code = None
    # device_name = None
    # device_type = None
    # mete_code = None
    # mete_name = None
    # resource_code = None
    # device_type_name = None
    # precinct_id = '01-07-05-02-35-01'
    # precinct_name = '百色测试数据二节点综合机房'
    # site_name = '百色测试数据二节点'


    device_id = None
    device_code = None
    device_name = None
    device_type = None
    mete_code = None
    mete_name = None
    resource_code = None
    device_type_name = None
    precinct_id = '01-07-21-01-01-03-01'
    precinct_name = 'HJJ核心机楼机房1'
    site_name = 'HJJ核心机楼'

    @classmethod
    def get_device_mete_code_info(cls, mete_code, precinct_name):
        get_device_info_sql = f"""SELECT b.device_id,b.device_code,b.device_name,a.device_type,a.mete_code,a.mete_name,
        a.alarm_explain,b.precinct_id,c.precinct_name,c.resource_code,d.dict_note
        FROM t_cfg_mete a,t_cfg_device b,t_cfg_precinct c,t_cfg_dict d
        WHERE a.device_type = b.device_type AND b.precinct_id = c.precinct_id AND a.mete_code = {mete_code} 
        AND b.device_type = d.dict_code AND d.col_name = 'device_type'
        AND c.precinct_name = '{precinct_name}';"""

        logger.debug(f'获取设备信息sql:\n{get_device_info_sql}')
        result = conn_obj.selectone(sql=get_device_info_sql, isdict=True)
        logger.debug(f'获取{precinct_name}-{mete_code}设备信息结果:\n{result}')
        if result:
            # cls.device_id = result['device_id']
            # cls.device_code = result['device_code']
            # cls.device_name = result['device_name']
            # # cls.device_name = '机房环境'
            # cls.device_type = result['device_type']
            # cls.mete_code = result['mete_code']
            # cls.mete_name = result['mete_name']
            # cls.precinct_id = result['precinct_id']
            # cls.precinct_name = result['precinct_name']
            # cls.device_type_name = result['dict_note']
            # cls.resource_code = result['resource_code']

            # 可行
            # cls.device_id = '00781006000003663228'
            # cls.device_code = '170200000024118'
            # cls.device_name = '华为温度41045'
            # cls.device_type = '17'
            # cls.mete_code = '017012'
            # cls.mete_name = '温度过低告警'
            # cls.precinct_id = '01-07-10-02-06-14'
            # cls.precinct_name = '南宁测试数据区广西数据中心1#楼四层401IDC机房'
            # cls.device_type_name = '机房环境'
            # cls.resource_code = '781_0000001000593_000001016'


            cls.device_id = '00541006000000106478'
            cls.device_code = '170100000031006'
            cls.device_name = '机房环境'
            cls.device_type = '17'
            cls.mete_code = '017012'
            cls.mete_name = '温度过低告警'
            cls.precinct_id = '01-07-21-01-01-03-01'
            cls.precinct_name = 'HJJ核心机楼机房1'
            cls.device_type_name = '机房环境'
            cls.resource_code = '541_2032_20250905'
        else:
            logger.error(f'获取{precinct_name}-{mete_code}设备信息失败')

    @classmethod
    def check(cls):
        t_zz_space_resources_sql = f"""SELECT * FROM `t_zz_space_resources` WHERE precinct_id = '{cls.precinct_id[:-3]}';"""
        t_zz_power_specialty_sql = f"""SELECT * FROM `t_zz_power_specialty` WHERE device_id = '{cls.device_id}';"""
        logger.debug('综资空间表查询sql:', t_zz_space_resources_sql)
        logger.debug('综资资源表查询sql:', t_zz_power_specialty_sql)
        print(cls.precinct_id[:-3])

        t_zz_space_resources = conn_obj.selectone(sql=t_zz_space_resources_sql, isdict=True)
        # resource_code = t_zz_space_resources.get('res_code')
        if not t_zz_space_resources:
            logger.error(f'查询站点不在‘综资空间表’内')
            relate_site = f'SITE-{time.strftime("%Y%m%d%H%M")}'
            insert_t_zz_space_resources_sql = f"""INSERT INTO `t_zz_space_resources`(`id`, `data_time`, `precinct_id`, `int_id`, `zh_label`, `related_site`, `space_type`, `create_time`) VALUES (null, '{relate_site[5:13]}', '{cls.precinct_id}', '{relate_site}', '{cls.precinct_name}', NULL, 101, '2024-05-28 14:58:33');"""
            logger.debug(f'插入综资空间表：\n{insert_t_zz_space_resources_sql}')
            conn_obj.insert(sql=insert_t_zz_space_resources_sql)
        else:
            t_zz_power_specialty = conn_obj.selectone(sql=t_zz_power_specialty_sql, isdict=True)
            relate_site = f'SITE-{time.strftime("%Y%m%d%H%M")}'
            if not t_zz_power_specialty:
                logger.error(f'{cls.device_id}设备不在t_zz_power_specialty内，现在开始插入此设备')
                insert_t_zz_power_specialty_sql = f"""INSERT INTO `t_zz_power_specialty` (`id`, `res_code`, `zh_label`, `data_time`, `device_id`, `device_type_id`, `device_type`, `device_code`, `power_device_name`, `related_site`, `related_room`, `ralated_power_device`, `cell_voltage_level`, `total_monomers_number`, `rated_capacity`, `signal_output_rated_capacity`, `total_rack_match_modules`, `lifecycle_status`, `rated_power`, `device_subclass`, `start_time`, `product_name`, `vendor_id`, `power_device_id`, `power_site_level`, `gx_power_site_level`, `create_time`) VALUES (null, NULL, '{cls.mete_name}', NULL, '{cls.device_id}', {cls.device_type}, '{cls.device_name}', '{cls.mete_code}', '{cls.mete_name}', '{relate_site}', NULL, '', '6', '2', '20', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{time.strftime("%Y-%m-%d %H:%M:%S")}');"""
                print(insert_t_zz_power_specialty_sql)
                conn_obj.insert(sql=insert_t_zz_power_specialty_sql)
            logger.debug(f'查询站点在综资空间表的数据：\n{t_zz_space_resources}')
            return t_zz_space_resources['int_id']

    @classmethod
    def send_yh(cls, rule_id=67, value1=20, date1='2025-06-10 00:00:00', device_property=None, many=False, **kwargs):
        url = 'http://10.12.8.147:31454/v1/hiddenDanger/rule/testRule'
        session = requests.Session()
        if device_property is None:
            device_property = ''
        data = {
            'ruleId': rule_id,
            'deviceDataList': [{
                'siteName': cls.site_name,
                'deviceId': cls.device_id,
                'deviceCode': cls.device_code,
                # 'deviceCode': None,
                # 'deviceCode': '100100000000017',
                # 'deviceCode': '00001008000000086197',
                'deviceName': cls.device_name,
                'deviceProperty': device_property,
                'signalId': cls.mete_code,
                'signalName': cls.mete_name,
                'signalNum': 0,
                'value': value1,
                'date': date1
            }]}
        # logger.debug('触发请求体：', json.dumps(data))
        logger.debug(f'data单个非持续时常隐患: {json.dumps(data, ensure_ascii=False)}')
        if many:
            data_list = copy.deepcopy(data['deviceDataList'])
            for key, value in kwargs.items():
                data_list[0][key] = value
            data['deviceDataList'].extend(data_list)
            logger.debug(f"传多个字典：{json.dumps(data, ensure_ascii=False)}")
        response = session.post(url, data=json.dumps(data, ensure_ascii=False),
                                headers={'Content-Type': 'application/json'})
        if json.loads(response.text)['status'] != str(200):
            logger.error(f"请求发送失败，状态码: {response.text}")
        else:
            logger.success("请求发送成功", response.text)
            logger.success(response.text)


if __name__ == '__main__':
    # gx = GxYinH()
    # gx.get_device_mete_code_info(mete_code='008333', precinct_name='百色测试数据to传输节点机房1')
    # gx.check()
    # gx.send_yh(many=True, rule_id=99, value1=-11, date1='2025-09-14 12:12:00', value=-15,
    #            date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 测试
    # 008333 99
    # gx = GxYinH()
    # gx.get_device_mete_code_info(mete_code='015303', precinct_name='百色测试数据to传输节点机房1')
    # gx.check()
    # gx.send_yh(many=True, rule_id=107, value1=40, date1='2025-10-21 19:12:00', value=50,
    #            date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 41  017012

    # 可行
    # gx = GxYinH()
    # gx.get_device_mete_code_info(mete_code='017012', precinct_name='南宁测试数据区广西数据中心1#楼四层401IDC机房')
    # gx.check()
    # gx.send_yh(many=True, rule_id=47, value1=27, date1='2025-10-22 19:12:00', value=28,
    #            date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


    gx = GxYinH()
    gx.get_device_mete_code_info(mete_code='017012', precinct_name='HJJ核心机楼机房1')
    gx.check()
    gx.send_yh(many=True, rule_id=47, value1=27, date1='2025-10-22 19:12:00', value=28,
               date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # gx.send_yh(many=True, rule_id=99, value1=-11, date1='2025-09-14 12:12:00', value=-15,
    #            date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # gx.send_yh(many=False, rule_id=105, value1=99, date1='2025-09-11 00:00:00', value=109,
    #            date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # , date = "2024-06-12 15:20:57"
