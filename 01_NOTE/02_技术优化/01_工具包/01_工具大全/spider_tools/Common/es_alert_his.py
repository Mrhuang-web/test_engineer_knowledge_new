# -*- coding: utf-8 -*-
import json
import os
import random
import time

import requests
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from sqlalchemy import *

from Conf.Config import Config


class es_alert_his:
    '''动环告警历史表，因越来越大，因此李可槐和王小荣整了一个Logstash，把每个月的历史告警导入到ES中
        1）业务上，慢慢把原来依赖于alert_alerts_his表的内容，迁移到es上
        2)es中的index_name为alert_YYYYMM
      自动化测试中，经常需要对告警历史表进行增删，业务上关注的主要是alert_id, device_id, mete_code, seria_number, starttime和endtime
    '''

    def __init__(self, env='sx'):
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        self.url = conf.get_conf(env, 'esurl')
        self.es = Elasticsearch(self.url)
        engines = "mysql+pymysql://" + self.dbuser + ":" + self.dbpw + \
                  "@" + self.dbip + "/" + self.dbname + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()
        self.index_name = None
        self.mapping = '''{"settings":{"number_of_shards":1,"number_of_replicas":1,"refresh_interval":"60s"},"mappings": {"his": {"properties": {"alert_end_time": {"type": "date"},"alert_explain": {"type": "keyword"},"alert_id": {"type": "keyword"},"alert_level": {"type": "keyword"},"alert_reason": {"type": "keyword"},"alert_start_month": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256}}},"alert_start_time": {"type": "date"},"alert_type": {"type": "keyword"},"biz_sys": {"type": "keyword"},"change_plan": {"type": "keyword"},"city_name": {"type": "keyword"},"classify_type": {"type": "short"},"clear_value": {"type": "keyword"},"confirm_people": {"type": "keyword"},"confirm_remark": {"type": "keyword"},"confirm_state": {"type": "keyword"},"confirm_time": {"type": "date"},"create_time": {"type": "date"},"cur_moni_time": {"type": "date"},"cur_moni_value": {"type": "keyword"},"device_id": {"type": "keyword"},"device_name": {"type": "keyword"},"device_type": {"type": "keyword"},"device_type_name": {"type": "keyword"},"engineering_status": {"type": "keyword"},"fixed": {"type": "short"},"force_clear": {"type": "short"},"force_clear_reason": {"type": "keyword"},"full_name": {"type": "keyword"},"index_seq": {"type": "long"},"is_standard_level": {"type": "keyword"},"logical_type": {"type": "keyword"},"lsc_id": {"type": "keyword"},"lsc_name": {"type": "keyword"},"manufacturer_name": {"type": "keyword"},"mete_code": {"type": "keyword"},"mete_id": {"type": "keyword"},"mete_name": {"type": "keyword"},"namespace": {"type": "keyword"},"object_id": {"type": "keyword"},"object_type": {"type": "keyword"},"order_id": {"type": "keyword"},"order_status": {"type": "keyword"},"order_type": {"type": "keyword"},"precinct_id": {"type": "keyword"},"precinct_name": {"type": "keyword"},"province_name": {"type": "keyword"},"r_alert_id": {"type": "keyword"},"raw_mete_code": {"type": "keyword"},"raw_mete_name": {"type": "keyword"},"remark": {"type": "keyword"},"room_id": {"type": "keyword"},"room_kind_name": {"type": "keyword"},"room_name": {"type": "keyword"},"serial_no": {"type": "keyword"},"show_type": {"type": "short"},"site_name": {"type": "keyword"},"site_type": {"type": "keyword"},"source_alert_id": {"type": "keyword"},"source_clear_alert_id": {"type": "keyword"},"source_room": {"type": "keyword"},"status_masks": {"type": "keyword"},"sub_logical_type": {"type": "keyword"},"task_flag": {"type": "keyword"},"third_party_flag": {"type": "short"},"threshold": {"type": "keyword"}}}}}'''
        self.sqlfile = open(str(os.path.dirname(__file__) +
                                '/selectForESList.sql'), encoding='utf-8')

    def get_db_info(self, device_id, mete_code):
        s = text(
            "SELECT tcd.precinct_id AS room_id, tcd.device_name,tcd.device_kind,tcd.device_type,tcmd.mete_id FROM t_cfg_device tcd INNER JOIN t_cfg_metemodel_detail tcmd"
            " ON tcd.device_model = tcmd.model_id"
            " AND tcd.device_id = :device_id AND tcmd.mete_code = :mete_code")
        result = self.conn.execute(s, device_id=device_id, mete_code=mete_code)
        row = result.fetchall()
        return row

    def get_alertdata(self, sqlindex, mete_code, device_id):
        """
        获取数据库特定区域下的某个测点相关数据
        :return:
        """
        sqlalllist = self.get_sqllist()  # 获取预设sql
        print("sqlalllist[sqlindex]:", sqlalllist[sqlindex])
        print("sqlalllist[sqlindex]:",  sqlindex )
        # result = self.conn.execute(
        #     text(sqlalllist[sqlindex]),
        #     [(mete_code,
        #     mete_code,
        #     device_id)])
        result = self.conn.execute(
            text(sqlalllist[sqlindex]), {'mete_code':mete_code, 'mete_code1':mete_code,'device_id':device_id})
        # [(1, 'asdsewadada', 'lajsdljasld', 'lol@gmail.com', 51)]
        row = result.fetchall()
        print(row)
        return row

    def get_sqllist(self):
        """
        读取到预设的sql
        :return:
        """
        f = self.sqlfile
        # print("sql文件位置--------------,",f)
        line = f.readline()
        sqlall = ''
        while line:
            sqlall = sqlall + line.strip("\n").strip("\t")
            line = f.readline()
        sqlalllist = sqlall.split(';')
        return sqlalllist

    def insert(
            self,
            device_id,
            mete_code,
            alert_start_time,
            alert_end_time,
            flush=True):
        '''es_alert_his().insert(device_id='343400001006000002202853',mete_code='008012',alert_start_time='2021-10-25T01:01:06.000Z',alert_end_time='2021-10-25T01:01:06.000Z')'''
        alert_start_month = alert_start_time[:4] + alert_start_time[5:7]
        self.index_name = 'alert_' + alert_start_month
        indetype = "his"
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(
                index=self.index_name, body=self.mapping)
            print('创建索引')
        else:
            print('索引已存在，直接写数据')
        # urlputindex = self.url + "/" + self.index_name
        # urlputmapping = self.url + "/" + self.index_name + "/" + indetype + "/_mapping"
        # requests.put(urlputindex)  # 新增index
        # pload = json.dumps(self.mapping)
        # requests.put(urlputmapping, pload)  # 创建mapping
        actions = []
        r = self.get_alertdata(3, mete_code, device_id)
        print("self.index_name",self.index_name)
        print("self.index_name",self.es)
        for i in r:
            print("r===", r, type(r))
            l = list(i)
            # print(self.get_db_info(device_id, mete_code)[0])
            # (room_id,device_name,device_kind,device_type,mete_id) = self.get_db_info(device_id, mete_code)[0]
            action = {"_index": self.index_name,
                      "_type": indetype,
                      "_source": {"cancel_people": None,
                                  "site_type": l[1],
                                  "alert_start_time": alert_start_time,
                                  "cancel_remark": None,
                                  "device_type": str(l[4]),
                                  "threshold": "40.0",
                                  "source_room": l[37],
                                  "force_clear_reason": None,
                                  "order_status": None,
                                  "index_seq": int(time.strftime('%m%d%H%M%S',
                                                                 time.localtime()) + str(random.randrange(1,
                                                                                                          100))),
                                  "biz_sys": None,
                                  "mete_name": l[11],
                                  "classify_type": 0,
                                  "alert_id": time.strftime('%Y%m%d%H%M%S',
                                                            time.localtime()) + '_' + str(random.randrange(1,
                                                                                                           100000)),
                                  "engineering_status": "非工程状态",
                                  "alert_level": l[15],
                                  "alert_explain": "设备整流器、逆变器、变压器等功率器件运行温度超过设定阈值",
                                  "order_type": None,
                                  "status_masks": None,
                                  "cancel_time": None,
                                  "third_party_flag": 3,
                                  "device_id": device_id,
                                  "task_flag": None,
                                  "create_time": alert_start_time,
                                  "precinct_id": l[24],
                                  "object_id": None,
                                  "province_name": l[26],
                                  "lsc_id": "1",
                                  "site_name": l[28],
                                  "room_name": l[29],
                                  "show_type": 0,
                                  "full_name": l[30],
                                  "change_plan": None,
                                  "source_clear_alert_id": time.strftime('%Y%m%d%H%M%S',
                                                                         time.localtime()) + '_' + str(
                                      random.randrange(1,
                                                       100000)),
                                  "fixed": 1,
                                  "confirm_people": None,
                                  "order_id": None,
                                  "serial_no": None,
                                  "room_id": l[37],
                                  "room_kind_name": l[38],
                                  "raw_mete_code": mete_code,
                                  "remark": "某个水浸探头探测到积水告警",
                                  "alert_type": None,
                                  "device_name": l[42],
                                  "city_name": l[43],
                                  "source_alert_id": None,
                                  "sub_logical_type": "水浸",
                                  "alert_start_month": alert_start_month,
                                  "device_type_name": l[46],
                                  "mete_id": l[47],
                                  "confirm_remark": "",
                                  "cur_moni_value": "38.6",
                                  "object_type": None,
                                  "force_clear": None,
                                  "lsc_name": "广东",
                                  "raw_mete_name": "温度过高告警",
                                  "r_alert_id": time.strftime('%Y%m%d%H%M%S',
                                                              time.localtime()) + '_' + str(random.randrange(1,
                                                                                                             100000)) + "_L2",
                                  "manufacturer_name": l[54],
                                  "mete_code": mete_code,
                                  "confirm_state": "0",
                                  "confirm_time": None,
                                  "alert_end_time": alert_end_time,
                                  "clear_value": None,
                                  "is_standard_level": "是",
                                  "cur_moni_time": alert_start_time,
                                  "logical_type": "辅助及控制部件告警",
                                  "namespace": None,
                                  "alert_reason": None,
                                  "precinct_name": l[65]}}
            print("action",action)
            actions.append(action)
            if len(actions) == 100:
                helpers.bulk(self.es, actions)
                del actions[0:len(actions)]
            helpers.bulk(self.es, actions)
        if flush:
            self.flush()

    def delete(
            self,
            device_id,
            mete_code,
            alert_start_time,
            alert_end_time=None,
            flush=True):
        '''es_alert_his().delete(device_id='343400001006000002159059', mete_code='008012',alert_start_time='2021-10-25T01:01:06')'''
        self.index_name = 'alert_' + \
                          alert_start_time[:4] + alert_start_time[5:7]
        indetype = "his"
        urldelmapping = self.url + "/" + self.index_name + \
                        "/" + indetype + "/_delete_by_query"
        search_kv_list = [
            "device_id=%s" %
            device_id,
            "mete_code=%s" %
            mete_code,
            "alert_start_time=%s" %
            alert_start_time]
        if alert_end_time is not None:
            search_kv_list.append("alert_end_time=%s" % alert_end_time)
        param = query_kw_list_to_json(search_kv_list)
        pload = json.dumps(param)
        print(param)
        requests.post(urldelmapping, pload)
        if flush:
            self.flush()

    def flush(self):
        self.es.indices.refresh(self.index_name)


def query_kw_list_to_json(kw_list=[]):
    result_dict = {"query": {"bool": {"must": []}}}
    for li in kw_list:
        tmp_dict = {}
        match_dict = {}
        k, v = li.split('=')
        tmp_dict.setdefault(k, v)
        if not v.find('T') and not v.find(':'):  # 对于日期格式的，只能term处理，而非match处理
            match_dict.setdefault("term", tmp_dict)
        else:
            match_dict.setdefault("match", tmp_dict)
        result_dict["query"]["bool"]["must"].append(match_dict)
    return result_dict


def _test_query_kw_list_to_json():
    kw_list = ["device_id=00001006000003381228", "site_name=卓望"]
    json_obj = query_kw_list_to_json(kw_list)
    print(json.dumps(json_obj))


if __name__ == "__main__":
    # es_alert_his().insert(device_id='00451006000002751397', mete_code='007002', alert_start_time='2021-12-20T01:01:06.000Z', alert_end_time='2021-12-22T01:01:06.000Z')
    # es_alert_his().insert(
    #     device_id='00111006000003327383',
    #     mete_code='008011',
    #     alert_start_time='2021-12-19T01:01:07.000Z',
    #     alert_end_time='2021-12-22T01:01:07.000Z')
    # es_alert_his().delete(device_id='00111006000003327383', mete_code='008011',alert_start_time='2021-12-19T01:01:07')
    # es_alert_his().insert(device_id='343400001006000002202853',mete_code='008012',alert_start_time='2021-10-25T01:01:06.000Z',alert_end_time='2021-10-25T01:01:06.000Z')
    # es_alert_his().insert(device_id='00111006000003327383', mete_code='008011', alert_start_time='2021-06-30T09:08:24.000Z', alert_end_time='2021-06-30T09:08:37.000Z')
    # es_alert_his().insert(device_id='00111006000003327381', mete_code='008011', alert_start_time='2021-06-30T09:08:24.000Z', alert_end_time='2021-06-30T09:08:37.000Z')
    # es_alert_his().delete(device_id='343400001006000002202853', mete_code='008012',alert_start_time='2021-10-25T01:01:06')

    # result = es_alert_his().get_db_info(device_id='00001006000003381228', mete_code='008042')
    # print(result)

    es_alert_his().insert(
        device_id='00713006000001671859',
        mete_code='002010',
        alert_start_time='2023-10-08T01:01:07.000Z',
        alert_end_time='2023-10-08T01:21:07.000Z')

    es_alert_his().insert(
        device_id='00713006000001671859',
        mete_code='002010',
        alert_start_time='2023-10-08T02:01:07.000Z',
        alert_end_time='2023-10-08T03:21:07.000Z')

    es_alert_his().insert(
        device_id='00713006000001671859',
        mete_code='092001',
        alert_start_time='2023-10-08T04:01:07.000Z',
        alert_end_time='2023-10-08T06:21:07.000Z')
    pass
