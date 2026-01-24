import datetime
from datetime import datetime as datetime2,timedelta
import json
import os
import random
import time
from urllib.parse import quote_plus as urlquote
import requests
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from sqlalchemy import *
import  urllib.parse
from Conf.Config import Config
# from datetime import datetime, timedelta



def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

def lastThreeDays(num):
    days = []
    for i in range(num + 1):
        days.append((datetime.date.today() + datetime.timedelta(0 - i)).strftime("%Y-%m-%d"))
        # days[::-1]
    return days[::-1]

def afterThreeDays(num):
    days = []
    for i in range(num + 1):
        days.append((datetime.date.today() + datetime.timedelta(0 + i)).strftime("%Y-%m-%d"))
        # days[::-1]
    return days[::-1]








class esDB():
    def __init__(
            self,
            precinct_id,
            mete_code='000000',
            imdate=datetime.datetime.now().strftime('%Y-%m-%d'),
            minval=1,
            maxval=1,
            device_id='1',
            del_col='meteID',
            del_clo_v='1',
            estime='T23:50:50',
            env='release'):
        conf = Config()
        
        # 接口请求数据【后续调用】
        self.precinct_id = precinct_id
        self.mete_code = mete_code
        self.imdate = imdate
        self.minval = minval
        self.maxval = maxval
        self.device_id = device_id
        self.del_col = del_col
        self.del_col_v = del_clo_v


        # 链接es【最开始就用】
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        self.url = conf.get_conf(env, 'esurl')
        self.estime = estime
        
        
        # mysql数据库的链接
        engines = "mysql+pymysql://" + urlquote(self.dbuser) + ":" + urlquote(self.dbpw) + \
                  "@" + self.dbip+":"+self.dbport + "/" + urlquote(self.dbname) + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()
        




        # es数据列 【对应索引的字段信息 - 最开头是type名称，然后是properties关键字，然后是字段，每个字段都有类型；具体配置看nacos】
        # type_name: point_history_data     #type的名称
        # index_name: fsu*                  #index的名称
        self.esparam = param = {

            "point_history_data": {
                "properties": {
                    "airType": {
                        "type": "short"
                    },
                    "airTypeName": {
                        "type": "keyword"
                    },
                    "areaID": {
                        "type": "keyword"
                    },
                    "areaName": {
                        "type": "keyword"
                    },
                    "buildingID": {
                        "type": "keyword"
                    },
                    "buildingName": {
                        "type": "keyword"
                    },
                    "centerSiteKind": {
                        "type": "short"
                    },
                    "centerSiteKindName": {
                        "type": "keyword"
                    },
                    "channelID": {
                        "type": "keyword"
                    },
                    "cityID": {
                        "type": "keyword"
                    },
                    "cityName": {
                        "type": "keyword"
                    },
                    "climateName": {
                        "type": "keyword"
                    },
                    "climateType": {
                        "type": "short"
                    },
                    "collectTime": {
                        "type": "date"
                    },
                    "desc": {
                        "type": "keyword"
                    },
                    "deviceID": {
                        "type": "keyword"
                    },
                    "deviceKind": {
                        "type": "short"
                    },
                    "deviceKindName": {
                        "type": "keyword"
                    },
                    "deviceName": {
                        "type": "keyword"
                    },
                    "deviceType": {
                        "type": "short"
                    },
                    "deviceTypeName": {
                        "type": "keyword"
                    },
                    "indexSeq": {
                        "type": "date"
                    },
                    "manufacturerId": {
                        "type": "keyword"
                    },
                    "measureVal": {
                        "type": "float"
                    },
                    "meteID": {
                        "type": "keyword"
                    },
                    "meteKind": {
                        "type": "short"
                    },
                    "meteKindName": {
                        "type": "keyword"
                    },
                    "meteName": {
                        "type": "keyword"
                    },
                    "precinctID": {
                        "type": "keyword"
                    },
                    "precinctName": {
                        "type": "keyword"
                    },
                    "provinceID": {
                        "type": "keyword"
                    },
                    "provinceName": {
                        "type": "keyword"
                    },
                    "roomKind": {
                        "type": "short"
                    },
                    "roomKindName": {
                        "type": "keyword"
                    },
                    "signalNumber": {
                        "type": "keyword"
                    },
                    "siteID": {
                        "type": "keyword"
                    },
                    "siteName": {
                        "type": "keyword"
                    },
                    "siteType": {
                        "type": "short"
                    },
                    "siteTypeName": {
                        "type": "keyword"
                    },
                    "temperatureMeteType": {
                        "type": "short"
                    },
                    "temperatureMeteTypeName": {
                        "type": "keyword"
                    },
                    "type": {
                        "type": "keyword"
                    },
                    "unit": {
                        "type": "keyword"
                    }
                }
            }

        }
        


        # 读取预设的sql
        self.sqlfile = open(str(os.path.dirname(__file__) +
                                '/selectForESList.sql'), encoding='utf-8')
        # self.sqlfile = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) + '/Params/SqlScript/'+'selectForESList.sql', encoding='utf-8')

    



    def get_devicedata(self):
        """
        获取数据库特定设备的相关测点数据   -- 数据库的查询
        :return:
        """
        s = text(
            "SELECT a.device_id,b.precinct_name,a.rated_power,b.precinct_id,c.mete_code,a.device_name,a.manufacturer_id,c.up_mete_id,c.mete_no FROM "
            "t_cfg_device a "
            "INNER JOIN t_cfg_precinct b ON a.precinct_id=b.precinct_id "
            "INNER JOIN t_cfg_metemodel_detail c ON a.device_model=c.model_id "
            "WHERE  a.device_id = :device_id AND c.mete_code = :mete_code")
        
        result = self.conn.execute(
            s, device_id=self.device_id, mete_code=self.mete_code)
        
        row = result.fetchall()
        return row
    



    def insert_esdata_device_metecode(self, flush=True):
        '''
                生成特定区域的某个测点的数据
                还需要满足设备是存在的
                :return:
                '''
        createim = self.imdate.split("-")
        creattime = createim[0] + createim[1] + createim[2]
        
        # 链接es
        es = Elasticsearch(self.url)
        
        # 创建索引
        filename = "fsu_" + creattime + "_" + self.precinct_id[0:5]
        indetype = "point_history_data"
        urlputindex = self.url + "/" + filename
        urlputmapping = self.url + "/" + filename + "/" + indetype + "/_mapping"
        requests.put(urlputindex)  # 新增index
        urlputsetting = self.url + "/" + filename + "/_settings"
        requests.put(urlputsetting, json.dumps({"index": {"number_of_replicas": "0"}}))  # 修改副本数为0修改副本数为0

        
        # 转换es字段字典为json，并发起put请求【把字段成功打进去】
        # param={"point_history_data":{"properties":{"channelID":{"type":"keyword"},"collectTime":{"type":"date"},"desc":{"type":"keyword"},"deviceID":{"type":"keyword"},"deviceName":{"type":"keyword"},"indexSeq":{"type":"date"},"manufacturerId":{"type":"keyword"},"measureVal":{"type":"float"},"meteID":{"type":"keyword"},"precinctID":{"type":"keyword"},"precinctName":{"type":"keyword"},"signalNumber":{"type":"keyword"},"type":{"type":"keyword"}}}}
        pload = json.dumps(self.esparam)
        requests.put(urlputmapping, pload)  # 创建mapping
        

        # 根据预设sql，查询mysql里面对应表的数据 -- 即判断数据库区域下有没有对应测点 - 有才能进行下一步写入es的操作，否则写入后也没用对应不了
        if self.device_id == '1' and self.mete_code== '000000':
            # 未传入设备就向该区域下所有设备下的该测点写入数据
            print("机房全量查询未传设备==========")
            r = self.get_provincedata(4)
        else:
            # 机房全量查询
            print("机房全量查询==========")
            r = self.get_provincedata(0)
        

        print("预计写入数据条数==========", len(r))
        print("预计写入数据条数==========",  r )
        

        actions = []


        for i in r:
            
            # 预设4或预设0返回的结果列表
            l = list(i)
            if not l:
                break
            print("l:", l)
            meteID = l[0]
            # collectTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            collectTime = self.imdate + self.estime
            precinctName = l[1]
            print("l[2],", l[2])
            

            # ups
            if meteID in ('008349', '008350', '008351'):
                if self.minval == self.maxval:
                    measureVal = self.minval
                else:
                    measureVal = random.randint(
                        round(
                            self.minval * 100),
                        round(
                            self.maxval * 100)) / 100
                    # measureVal = random.randint(1, 80)

            # ups
            elif meteID in ('008318', '008319', '008320'):
                if l[2] is not None:
                    if self.minval == self.maxval:
                        measureVal = self.minval
                    else:
                        # measureVal = random.randint(1, round(float(l[2]) * 0.3) + 2)
                        measureVal = random.randint(
                            round(self.minval * 100), round(self.maxval * 100)) / 100
                else:
                    measureVal = None

            # 低压交流配电
            elif meteID in ('002330', '004306','006327', '009312', '009332', '078315', '078331', '088304',
                             '088305', '088308', '092316', '092324'):

                ##能耗关键测点，正常数据是递增的，除非换表和异常   -- 先根据device_id和meteid取获取到es中对应设备的昨天值
                result =self.esdata_query(meteID,l[8])
                print(" l[2]====" ,l[2])
                
                if self.minval!=1 and self.maxval!=1:
                    print("初始化传递的值")
                    if self.minval == self.maxval:
                        measureVal = self.minval
                    else:
                        measureVal = random.randint(
                            round(self.minval * 100), round(self.maxval * 100)) / 100
                else:
                    if  result==[]:
                        measureVal = 100
                    else:
                        print("获取昨天的电表值:",result)
                        #自增100
                        #查询昨天最后一个值然后+100 ，如果没有查询到就给100
                        measureVal =int(result)+100
                        print("进行自增return")
            
            # 其余全部测点都按这个格式
            else:
                if self.minval!=1 and self.maxval!=1:
                    print("self.minval", self.minval)
                    measureVal = random.randint(
                        round(self.minval * 100), round(self.maxval * 100)) / 100
                    print("measureVal", measureVal)
                else:
                    measureVal = random.randint(
                        round(
                            1 * 100),
                        round(
                            100 * 100)) / 100
            

            precinctID = l[3]
            temperatureMeteType = l[4]
            manufacturerId = l[5]
            type = 'AI'

            # if self.device_id != 1:
            #     deviceID = self.device_id
            # else:
            deviceID = l[8]
            deviceName = l[9]
            

            if l[10] is None:
                desc = '温度'
            else:
                desc = l[10]
            

            signalNumber = l[6]
            indexSeq = int(time.time()) * 1000
            

            if l[6] is None:
                signalNumber = ''
            else:
                signalNumber = str(l[6])
                desc = '温度'
            
            channelID = meteID + "_" + signalNumber + "_"

            airType = l[11]
            siteType = l[12]
            roomKind = l[13]
            deviceType = l[14]
            deviceKind = l[15]
            centerSiteKind = l[16]
            airTypeName = l[17]
            siteName = l[18]
            centerSiteKindName = l[19]
            provinceID = l[20]
            meteKindName = l[21]
            buildingID = l[22]
            climateName = l[23]
            areaID = l[24]
            cityName = l[25]
            siteTypeName = l[26]
            temperatureMeteTypeName = l[27]
            meteKind = l[28]
            deviceTypeName = l[29]
            cityID = l[30]
            meteName = l[31]
            buildingName = l[32]
            unit = l[33]
            roomKindName = l[34]
            siteID = l[35]
            provinceName = l[36]
            climateType = l[37]

            # 要提交给es的字段-即对应数据
            action = {
                "_index": filename,
                "_type": indetype,
                "_source": {
                    'meteID': meteID,
                    'collectTime': collectTime,
                    'precinctName': precinctName,
                    'measureVal': measureVal,
                    'precinctID': precinctID,
                    'temperatureMeteType': temperatureMeteType,
                    'manufacturerId': manufacturerId,
                    'signalNumber': signalNumber,
                    'indexSeq': indexSeq,
                    'type': type,
                    'deviceID': deviceID,
                    'deviceName': deviceName,
                    'channelID': channelID,
                    'desc': desc,
                    'airType': airType,
                    'siteType': siteType,
                    'roomKind': roomKind,
                    'deviceType': deviceType,
                    'deviceKind': deviceKind,
                    'centerSiteKind': centerSiteKind,
                    'airTypeName': airTypeName,
                    'siteName': siteName,
                    'centerSiteKindName': centerSiteKindName,
                    'provinceID': provinceID,
                    'meteKindName': meteKindName,
                    'buildingID': buildingID,
                    'climateName': climateName,
                    'areaID': areaID,
                    'cityName': cityName,
                    'siteTypeName': siteTypeName,
                    'temperatureMeteTypeName': temperatureMeteTypeName,
                    'meteKind': meteKind,
                    'deviceTypeName': deviceTypeName,
                    'cityID': cityID,
                    'meteName': meteName,
                    'buildingName': buildingName,
                    'unit': unit,
                    'roomKindName': roomKindName,
                    'siteID': siteID,
                    'provinceName': provinceName,
                    'climateType': climateType,
                }
            }

            actions.append(action)
            

            # 批量提交，每次满100就会清空，避免一次插入太多卡顿
            if len(actions) == 100:
                helpers.bulk(es, actions)
                del actions[0:len(actions)]
    
        # 避免为满足100后那些数据没有上报
        helpers.bulk(es, actions)
        
        # 刷新索引
        if flush:
            es.indices.refresh(index=filename)




    def insert_esdata_device(self, flush=True):
        '''
                生成特定区域的某个测点的数据  --> 直接是通过区域precinct_id结合mete_id直接去拿，省略了设备过滤
                使用的sql预设是1和2
                :return:
                '''
        createim = self.imdate.split("-")
        creattime = createim[0] + createim[1] + createim[2]
        

        es = Elasticsearch(self.url)
        filename = "fsu_" + creattime + "_" + self.precinct_id[0:5]
        indetype = "point_history_data"
        urlputindex = self.url + "/" + filename
        urlputmapping = self.url + "/" + filename + "/" + indetype + "/_mapping"
        requests.put(urlputindex)  # 新增index
        urlputsetting = self.url + "/" + filename + "/_settings"
        requests.put(urlputsetting, json.dumps({"index": {"number_of_replicas": "0"}}))  # 修改副本数为0修改副本数为0

        # param={"point_history_data":{"properties":{"channelID":{"type":"keyword"},"collectTime":{"type":"date"},"desc":{"type":"keyword"},"deviceID":{"type":"keyword"},"deviceName":{"type":"keyword"},"indexSeq":{"type":"date"},"manufacturerId":{"type":"keyword"},"measureVal":{"type":"float"},"meteID":{"type":"keyword"},"precinctID":{"type":"keyword"},"precinctName":{"type":"keyword"},"signalNumber":{"type":"keyword"},"type":{"type":"keyword"}}}}
        pload = json.dumps(self.esparam)
        requests.put(urlputmapping, pload)  # 创建mapping
        

        if self.device_id == '1':
            # 未传入设备就向该区域下所有设备下的该测点写入数据
            r = self.get_provincedata(2)
        else:
            # 已经传入设备
            r = self.get_provincedata(1)
        

        actions = []
        
        print("预计写入数据条数==========", len(r))
        
        for i in r:
            l = list(i)
            if not l:
                break
            print("l:", l)
            meteID = l[0]
            # collectTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            collectTime = self.imdate + self.estime
            precinctName = l[1]
            print("l[2],", l[2])
            

            if meteID in ('008349', '008350', '008351'):
                if self.minval == self.maxval:
                    measureVal = self.minval
                else:
                    measureVal = random.randint(
                        round(
                            self.minval * 100),
                        round(
                            self.maxval * 100)) / 100
                    # measureVal = random.randint(1, 80)

            elif meteID in ('008318', '008319', '008320'):
                if l[2] is not None:
                    if self.minval == self.maxval:
                        measureVal = self.minval
                    else:
                        # measureVal = random.randint(1, round(float(l[2]) * 0.3) + 2)
                        measureVal = random.randint(
                            round(self.minval * 100), round(self.maxval * 100)) / 100
                else:
                    measureVal = None
            else:
                if self.minval == self.maxval:
                    print("self.minval", self.minval)
                    measureVal = self.minval
                    print("measureVal", measureVal)
                else:
                    measureVal = random.randint(
                        round(
                            self.minval * 100),
                        round(
                            self.maxval * 100)) / 100

            precinctID = l[3]

            temperatureMeteType = l[4]
            manufacturerId = l[5]
            type = 'AI'

            if self.device_id != 1:
                deviceID = self.device_id
            else:
                deviceID = l[8]
            deviceName = l[9]
            if l[10] is None:
                desc = '温度'
            else:
                desc = l[10]
            signalNumber = l[6]
            indexSeq = int(time.time()) * 1000
            if l[6] is None:
                signalNumber = ''
            else:
                signalNumber = str(l[6])
                desc = '温度'
            # channelID = meteID + "_" + signalNumber + "_" + desc
            channelID = meteID + "_" + signalNumber + "_"
            airType = l[11]
            siteType = l[12]
            roomKind = l[13]
            deviceType = l[14]
            deviceKind = l[15]
            centerSiteKind = l[16]
            airTypeName = l[17]
            siteName = l[18]
            centerSiteKindName = l[19]
            provinceID = l[20]
            meteKindName = l[21]
            buildingID = l[22]
            climateName = l[23]
            areaID = l[24]
            cityName = l[25]
            siteTypeName = l[26]
            temperatureMeteTypeName = l[27]
            meteKind = l[28]
            deviceTypeName = l[29]
            cityID = l[30]
            meteName = l[31]
            buildingName = l[32]
            unit = l[33]
            roomKindName = l[34]
            siteID = l[35]
            provinceName = l[36]
            climateType = l[37]

            action = {
                "_index": filename,
                "_type": indetype,
                "_source": {
                    'meteID': meteID,
                    'collectTime': collectTime,
                    'precinctName': precinctName,
                    'measureVal': measureVal,
                    'precinctID': precinctID,
                    'temperatureMeteType': temperatureMeteType,
                    'manufacturerId': manufacturerId,
                    'signalNumber': signalNumber,
                    'indexSeq': indexSeq,
                    'type': type,
                    'deviceID': deviceID,
                    'deviceName': deviceName,
                    'channelID': channelID,
                    'desc': desc,
                    'airType': airType,
                    'siteType': siteType,
                    'roomKind': roomKind,
                    'deviceType': deviceType,
                    'deviceKind': deviceKind,
                    'centerSiteKind': centerSiteKind,
                    'airTypeName': airTypeName,
                    'siteName': siteName,
                    'centerSiteKindName': centerSiteKindName,
                    'provinceID': provinceID,
                    'meteKindName': meteKindName,
                    'buildingID': buildingID,
                    'climateName': climateName,
                    'areaID': areaID,
                    'cityName': cityName,
                    'siteTypeName': siteTypeName,
                    'temperatureMeteTypeName': temperatureMeteTypeName,
                    'meteKind': meteKind,
                    'deviceTypeName': deviceTypeName,
                    'cityID': cityID,
                    'meteName': meteName,
                    'buildingName': buildingName,
                    'unit': unit,
                    'roomKindName': roomKindName,
                    'siteID': siteID,
                    'provinceName': provinceName,
                    'climateType': climateType,
                }
            }

            actions.append(action)
            if len(actions) == 100:
                helpers.bulk(es, actions)
                del actions[0:len(actions)]
        
        helpers.bulk(es, actions)
        
        if flush:
            es.indices.refresh(index=filename)




    def insert_esdata_device_batch(self, timedelta_min=60,is_changing=True,stepnum=2, flush=True):
        '''
        同一个设备插入多条，不重复查询r，每小时插入一条数据
        esDB(precinct_id="01-02-10-04-35-01", mete_code="006309", imdate="2023-09-02", minval=120, maxval=120 ,device_id='16881181054244492',  env="release").insert_esdata_device_batch()
        :return:
        '''
        createim = self.imdate.split("-")
        creattime = createim[0] + createim[1] + createim[2]
        

        es = Elasticsearch(self.url)
        filename = "fsu_" + creattime + "_" + self.precinct_id[0:5]
        indetype = "point_history_data"
        urlputindex = self.url + "/" + filename
        urlputmapping = self.url + "/" + filename + "/" + indetype + "/_mapping"
        requests.put(urlputindex)  # 新增index
        urlputsetting = self.url + "/" + filename + "/_settings"
        

        requests.put(urlputsetting, json.dumps({"index": {"number_of_replicas": "0"}}))  # 修改副本数为0修改副本数为0
        pload = json.dumps(self.esparam)
        requests.put(urlputmapping, pload)  # 创建mapping
        

        if self.device_id == '1':
            # 未传入设备就向该区域下所有设备下的该测点写入数据
            r = self.get_provincedata(2)
        else:
            # 已经传入设备
            r = self.get_provincedata(1)
        

        actions = []
        
        
        print("预计写入数据条数==========", len(r))
        

        for i in r:
            
            l = list(i)
            
            if not l:
                break
            start = time.strptime('%s 00:00:15' % self.imdate, '%Y-%m-%d %H:%M:%S')
            dts = [dt.strftime('%Y-%m-%dT%H:%M:%S') for dt in
                   datetime_range(datetime.datetime(start.tm_year, start.tm_mon, start.tm_mday, 0, 0, 15),
                                  datetime.datetime(start.tm_year, start.tm_mon, start.tm_mday, 23, 59, 59),
                                  datetime.timedelta(minutes=timedelta_min))]
            beginstepnum=0
            
            for collectTime in dts:
                

                if is_changing is True:
                    beginstepnum=beginstepnum+stepnum
                else:
                    beginstepnum=0
                self.minval=self.minval+beginstepnum
                self.maxval=self.maxval+beginstepnum

                meteID = l[0]
                # collectTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                # collectTime = self.imdate + "T" + hms_str
                precinctName = l[1]
                

                if meteID in ('008349', '008350', '008351'):
                    if self.minval == self.maxval:
                        measureVal = self.minval
                    else:
                        measureVal = random.randint(
                            round(
                                self.minval * 100),
                            round(
                                self.maxval * 100)) / 100
                        # measureVal = random.randint(1, 80)

                elif meteID in ('008318', '008319', '008320'):
                    if l[2] is not None:
                        if self.minval == self.maxval:
                            measureVal = self.minval
                        else:
                            # measureVal = random.randint(1, round(float(l[2]) * 0.3) + 2)
                            measureVal = random.randint(
                                round(self.minval * 100), round(self.maxval * 100)) / 100
                    else:
                        measureVal = None
                else:
                    if self.minval == self.maxval:
                        # print("self.minval", self.minval)
                        measureVal = self.minval
                        # print("measureVal", measureVal)
                    else:
                        measureVal = random.randint(
                            round(
                                self.minval * 100),
                            round(
                                self.maxval * 100)) / 100

                precinctID = l[3]
                temperatureMeteType = l[4]
                manufacturerId = l[5]
                type = 'AI'
                if self.device_id != 1:
                    deviceID = self.device_id
                else:
                    deviceID = l[8]
                deviceName = l[9]
                if l[10] is None:
                    desc = ''
                    # desc = '温度'
                else:
                    desc = l[10]
                signalNumber = l[6]
                indexSeq = int(time.time()) * 1000
                if l[6] is None:
                    signalNumber = ''
                else:
                    signalNumber = str(l[6])
                    desc = ''
                    # desc = '温度'
                # channelID = meteID + "_" + signalNumber + "_" + desc
                channelID = meteID + "_" + signalNumber + "_"
                airType = l[11]
                siteType = l[12]
                roomKind = l[13]
                deviceType = l[14]
                deviceKind = l[15]
                centerSiteKind = l[16]
                airTypeName = l[17]
                siteName = l[18]
                centerSiteKindName = l[19]
                provinceID = l[20]
                meteKindName = l[21]
                buildingID = l[22]
                climateName = l[23]
                areaID = l[24]
                cityName = l[25]
                siteTypeName = l[26]
                temperatureMeteTypeName = l[27]
                meteKind = l[28]
                deviceTypeName = l[29]
                cityID = l[30]
                meteName = l[31]
                buildingName = l[32]
                unit = l[33]
                roomKindName = l[34]
                siteID = l[35]
                provinceName = l[36]
                climateType = l[37]
                action = {
                    "_index": filename,
                    "_type": indetype,
                    "_source": {
                        'meteID': meteID,
                        'collectTime': collectTime,
                        'precinctName': precinctName,
                        'measureVal': measureVal,
                        'precinctID': precinctID,
                        'temperatureMeteType': temperatureMeteType,
                        'manufacturerId': manufacturerId,
                        'signalNumber': signalNumber,
                        'indexSeq': indexSeq,
                        'type': type,
                        'deviceID': deviceID,
                        'deviceName': deviceName,
                        'channelID': channelID,
                        'desc': desc,
                        'airType': airType,
                        'siteType': siteType,
                        'roomKind': roomKind,
                        'deviceType': deviceType,
                        'deviceKind': deviceKind,
                        'centerSiteKind': centerSiteKind,
                        'airTypeName': airTypeName,
                        'siteName': siteName,
                        'centerSiteKindName': centerSiteKindName,
                        'provinceID': provinceID,
                        'meteKindName': meteKindName,
                        'buildingID': buildingID,
                        'climateName': climateName,
                        'areaID': areaID,
                        'cityName': cityName,
                        'siteTypeName': siteTypeName,
                        'temperatureMeteTypeName': temperatureMeteTypeName,
                        'meteKind': meteKind,
                        'deviceTypeName': deviceTypeName,
                        'cityID': cityID,
                        'meteName': meteName,
                        'buildingName': buildingName,
                        'unit': unit,
                        'roomKindName': roomKindName,
                        'siteID': siteID,
                        'provinceName': provinceName,
                        'climateType': climateType,
                    }
                }
                actions.append(action)
                if len(actions) == 100:
                    helpers.bulk(es, actions)
                    del actions[0:len(actions)]
        helpers.bulk(es, actions)
        if flush:
            es.indices.refresh(index=filename)





    def get_sqllist(self):
        """
        读取到预设的sql
        :return:
        """
        
        f = self.sqlfile
        
        # print("sql文件位置--------------,",f)
        line = f.readline()
        
        sqlall = ''
        
        # 通过;区分不同select
        while line:
            sqlall = sqlall + line.strip("\n").strip("\t")
            line = f.readline()
        sqlalllist = sqlall.split(';')
        

        return sqlalllist






    def get_provincedata(self, sqlindex):
        """
        获取数据库特定区域下的某个测点相关数据
        :return:
        """
        sqlalllist = self.get_sqllist()  # 获取预设sql
        # print("sqlalllist[sqlindex]---->", sqlalllist[sqlindex])
        
        if sqlindex == 1:
            result = self.conn.execute(
                text(sqlalllist[sqlindex]),
                {'precinct_id': self.precinct_id + '%', 'mete_code': self.mete_code, 'device_id': self.device_id})
            # (self.precinct_id + '%'),
            # (self.mete_code),
            # self.device_id)
        
        elif sqlindex == 2:
            result = self.conn.execute(text(sqlalllist[sqlindex]),
                                       {'precinct_id': self.precinct_id + '%', 'mete_code': self.mete_code})
            # (self.precinct_id + '%'),
            # (self.mete_code))
        
        elif sqlindex == 0:
            result = self.conn.execute(
                text(sqlalllist[sqlindex]),
                {'precinct_id': self.precinct_id + '%'})
        
        elif sqlindex == 4:
            result = self.conn.execute(
                text(sqlalllist[sqlindex]),
                {'precinct_id': self.precinct_id + '%'})
        
        else:
            print("其他")
        
        row = result.fetchall()
        return row



    def insert_esdata_province(self):
        '''
        生成特定区域的某个测点的数据
        :return:
        '''
        createim = self.imdate.split("-")
        creattime = createim[0] + createim[1] + createim[2]
        # creattime = (datetime.datetime.now() + datetime.timedelta(+2)).strftime("%Y%m%d")
        # creattime = (datetime.datetime.now()).strftime("%Y%m%d")
        

        es = Elasticsearch(self.url, timeout=120)
        filename = "fsu_" + creattime + "_" + self.precinct_id[0:5]
        # filename = "fsu_" + creattime + "_" + self.precinct_id
        

        indetype = "point_history_data"
        urlputindex = self.url + "/" + filename
        urlputmapping = self.url + "/" + filename + "/" + indetype + "/_mapping"
        requests.put(urlputindex)  # 新增index
        urlputsetting = self.url + "/" + filename + "/_settings"
        requests.put(urlputsetting, json.dumps({"index": {"number_of_replicas": "0"}}))  # 修改副本数为0
        


        # param={"point_history_data":{"properties":{"channelID":{"type":"keyword"},"collectTime":{"type":"date"},"desc":{"type":"keyword"},"deviceID":{"type":"keyword"},"deviceName":{"type":"keyword"},"indexSeq":{"type":"date"},"manufacturerId":{"type":"keyword"},"measureVal":{"type":"float"},"meteID":{"type":"keyword"},"precinctID":{"type":"keyword"},"precinctName":{"type":"keyword"},"signalNumber":{"type":"keyword"},"type":{"type":"keyword"}}}}
        pload = json.dumps(self.esparam)
        requests.put(urlputmapping, pload)  # 创建mapping
        

        if self.device_id == '1' and self.mete_code == "000000":
            r = self.get_provincedata(0)
        if self.mete_code != "000000":
            # 未传入设备就向该区域下所有设备下的该测点写入数据
            r = self.get_provincedata(2)
        if self.device_id != '1' and self.mete_code != "000000":
            # 已经传入设备
            r = self.get_provincedata(1)
        

        actions = []
        

        print("预计写入数据条数==========", len(r))
        

        for i in r:
            

            l = list(i)
            if not l:
                break
            
            print("l:", l)
            
            meteID = l[0]
            # collectTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            collectTime = self.imdate + self.estime
            precinctName = l[1]
            

            # print("l[2],", l[2])
            if meteID in ('008349', '008350', '008351'):
                if self.minval == self.maxval:
                    measureVal = self.minval
                else:
                    measureVal = random.randint(
                        round(
                            self.minval * 100),
                        round(
                            self.maxval * 100)) / 100
                    # measureVal = random.randint(1, 80)

            elif meteID in ('008318', '008319', '008320'):
                if l[2] is not None:
                    if self.minval == self.maxval:
                        measureVal = self.minval
                    else:
                        # measureVal = random.randint(1, round(float(l[2]) * 0.3) + 2)
                        measureVal = random.randint(
                            round(self.minval * 100), round(self.maxval * 100)) / 100
                else:
                    measureVal = None
            else:
                if self.minval == self.maxval:
                    measureVal = self.minval
                else:
                    measureVal = random.randint(
                        round(
                            self.minval * 100),
                        round(
                            self.maxval * 100)) / 100
            

            precinctID = l[3]

            temperatureMeteType = l[4]
            manufacturerId = l[5]
            type = 'AI'

            # if self.device_id != 1:
            #    deviceID = self.device_id
            # else:
            deviceID = l[8]
            deviceName = l[9]
            if l[10] is None:
                desc = ''
            else:
                desc = l[10]
            signalNumber = l[6]
            if l[6] is None:
                signalNumber = ''
            else:
                signalNumber = str(l[6])
                desc = ''
            # channelID = meteID + "_" + signalNumber + "_" + desc
            channelID = meteID + "_" + signalNumber + "_"
            indexSeq = int(time.time()) * 1000
            airType = l[11]
            siteType = l[12]
            roomKind = l[13]
            deviceType = l[14]
            deviceKind = l[15]
            centerSiteKind = l[16]
            airTypeName = l[17]
            siteName = l[18]
            centerSiteKindName = l[19]
            provinceID = l[20]
            meteKindName = l[21]
            buildingID = l[22]
            climateName = l[23]
            areaID = l[24]
            cityName = l[25]
            siteTypeName = l[26]
            temperatureMeteTypeName = l[27]
            meteKind = l[28]
            deviceTypeName = l[29]
            cityID = l[30]
            meteName = l[31]
            buildingName = l[32]
            unit = l[33]
            roomKindName = l[34]
            siteID = l[35]
            provinceName = l[36]
            climateType = l[37]
            action = {
                "_index": filename,
                "_type": indetype,
                "_source": {
                    'meteID': meteID,
                    'collectTime': collectTime,
                    'precinctName': precinctName,
                    'measureVal': measureVal,
                    'precinctID': precinctID,
                    'temperatureMeteType': temperatureMeteType,
                    'manufacturerId': manufacturerId,
                    'signalNumber': signalNumber,
                    'indexSeq': indexSeq,
                    'type': type,
                    'deviceID': deviceID,
                    'deviceName': deviceName,
                    'channelID': channelID,
                    'desc': desc,
                    'airType': airType,
                    'siteType': siteType,
                    'roomKind': roomKind,
                    'deviceType': deviceType,
                    'deviceKind': deviceKind,
                    'centerSiteKind': centerSiteKind,
                    'airTypeName': airTypeName,
                    'siteName': siteName,
                    'centerSiteKindName': centerSiteKindName,
                    'provinceID': provinceID,
                    'meteKindName': meteKindName,
                    'buildingID': buildingID,
                    'climateName': climateName,
                    'areaID': areaID,
                    'cityName': cityName,
                    'siteTypeName': siteTypeName,
                    'temperatureMeteTypeName': temperatureMeteTypeName,
                    'meteKind': meteKind,
                    'deviceTypeName': deviceTypeName,
                    'cityID': cityID,
                    'meteName': meteName,
                    'buildingName': buildingName,
                    'unit': unit,
                    'roomKindName': roomKindName,
                    'siteID': siteID,
                    'provinceName': provinceName,
                    'climateType': climateType,
                }
            }

            actions.append(action)
            if len(actions) == 100:
                helpers.bulk(es, actions)
                del actions[0:len(actions)]
        helpers.bulk(es, actions)
        es.indices.refresh(index=filename)




    def insert_esdata(self, flush=True):
        '''
        生成基础数据校验文档
        :return:
        '''
        creattime = datetime.datetime.now().strftime('%Y%m%d')
        # 调试用
        # creattime=(datetime.datetime.now() + datetime.timedelta(-1)).strftime("%Y%m%d")
        es = Elasticsearch(self.url, timeout=120)
        
        filename = "fsu_" + creattime + "_" + self.precinct_id
        indetype = "point_history_data"
        urlputindex = self.url + "/" + filename
        urlputmapping = self.url + "/" + filename + "/" + indetype + "/_mapping"
        requests.put(urlputindex)  # 新增index
        urlputsetting = self.url + "/" + filename + "/_settings"
        
        requests.put(urlputsetting, json.dumps({"index": {"number_of_replicas": "0"}}))  # 修改副本数为0

        

        param = {

            "point_history_data": {
                "properties": {
                    "airType": {
                        "type": "short"
                    },
                    "airTypeName": {
                        "type": "keyword"
                    },
                    "areaID": {
                        "type": "keyword"
                    },
                    "areaName": {
                        "type": "keyword"
                    },
                    "buildingID": {
                        "type": "keyword"
                    },
                    "buildingName": {
                        "type": "keyword"
                    },
                    "centerSiteKind": {
                        "type": "short"
                    },
                    "centerSiteKindName": {
                        "type": "keyword"
                    },
                    "channelID": {
                        "type": "keyword"
                    },
                    "cityID": {
                        "type": "keyword"
                    },
                    "cityName": {
                        "type": "keyword"
                    },
                    "climateName": {
                        "type": "keyword"
                    },
                    "climateType": {
                        "type": "short"
                    },
                    "collectTime": {
                        "type": "date"
                    },
                    "desc": {
                        "type": "keyword"
                    },
                    "deviceID": {
                        "type": "keyword"
                    },
                    "deviceKind": {
                        "type": "short"
                    },
                    "deviceKindName": {
                        "type": "keyword"
                    },
                    "deviceName": {
                        "type": "keyword"
                    },
                    "deviceType": {
                        "type": "short"
                    },
                    "deviceTypeName": {
                        "type": "keyword"
                    },
                    "indexSeq": {
                        "type": "date"
                    },
                    "manufacturerId": {
                        "type": "keyword"
                    },
                    "measureVal": {
                        "type": "float"
                    },
                    "meteID": {
                        "type": "keyword"
                    },
                    "meteKind": {
                        "type": "short"
                    },
                    "meteKindName": {
                        "type": "keyword"
                    },
                    "meteName": {
                        "type": "keyword"
                    },
                    "precinctID": {
                        "type": "keyword"
                    },
                    "precinctName": {
                        "type": "keyword"
                    },
                    "provinceID": {
                        "type": "keyword"
                    },
                    "provinceName": {
                        "type": "keyword"
                    },
                    "roomKind": {
                        "type": "short"
                    },
                    "roomKindName": {
                        "type": "keyword"
                    },
                    "signalNumber": {
                        "type": "keyword"
                    },
                    "siteID": {
                        "type": "keyword"
                    },
                    "siteName": {
                        "type": "keyword"
                    },
                    "siteType": {
                        "type": "short"
                    },
                    "siteTypeName": {
                        "type": "keyword"
                    },
                    "temperatureMeteType": {
                        "type": "short"
                    },
                    "temperatureMeteTypeName": {
                        "type": "keyword"
                    },
                    "type": {
                        "type": "keyword"
                    },
                    "unit": {
                        "type": "keyword"
                    }
                }
            }

        }
        

        pload = json.dumps(param)
        print("urlputmapping", urlputmapping)
        # 创建mapping
        # http://10.12.70.61:9200/fsu_20211016_01-01/point_history_data/_mapping
        requests.put(urlputmapping, pload)
        
        r = self.get_provincedata(0)
        

        print("预计写入数据条数==========", len(r))
        
        actions = []
        

        for i in r:
            
            l = list(i)
            if not l:
                break
            # print("l:", l)
            meteID = l[0]
            collectTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            precinctName = l[1]
            # print("l[2],", l[2])
            


            if meteID in ('008349', '008350', '008351'):
                measureVal = random.randint(1, 80)
            elif meteID in ('008318', '008319', '008320'):
                if l[2] is not None:
                    measureVal = random.randint(
                        1, round(float(l[2]) * 0.3) + 2)
                else:
                    measureVal = None
            else:
                if l[2] is not None:
                    measureVal = random.randint(
                        1, round(float(l[2]) * 0.03) + 2)
                else:
                    measureVal = random.randint(
                        1, round(float(100) * 0.03) + 2)
            


            precinctID = l[3]
            temperatureMeteType = l[4]
            manufacturerId = l[5]
            type = 'AI'
            deviceID = l[8]
            deviceName = l[9]

            

            if l[10] is None:
                desc = ''
            else:
                desc = l[10]
            signalNumber = l[6]
            if l[6] is None:
                signalNumber = ''
            else:
                signalNumber = str(l[6])
                desc = ''
            # channelID = meteID + "_" + signalNumber + "_" + desc
            channelID = meteID + "_" + signalNumber + "_"
            indexSeq = int(time.time()) * 1000

            airType = l[11]
            siteType = l[12]
            roomKind = l[13]
            deviceType = l[14]
            deviceKind = l[15]
            centerSiteKind = l[16]
            airTypeName = l[17]
            siteName = l[18]
            centerSiteKindName = l[19]
            provinceID = l[20]
            meteKindName = l[21]
            buildingID = l[22]
            climateName = l[23]
            areaID = l[24]
            cityName = l[25]
            siteTypeName = l[26]
            temperatureMeteTypeName = l[27]
            meteKind = l[28]
            deviceTypeName = l[29]
            cityID = l[30]
            meteName = l[31]
            buildingName = l[32]
            unit = l[33]
            roomKindName = l[34]
            siteID = l[35]
            provinceName = l[36]
            climateType = l[37]
            action = {
                "_index": filename,
                "_type": indetype,
                "_source": {
                    'meteID': meteID,
                    'collectTime': collectTime,
                    'precinctName': precinctName,
                    'measureVal': measureVal,
                    'precinctID': precinctID,
                    'temperatureMeteType': temperatureMeteType,
                    'manufacturerId': manufacturerId,
                    'signalNumber': signalNumber,
                    'indexSeq': indexSeq,
                    'type': type,
                    'deviceID': deviceID,
                    'deviceName': deviceName,
                    'channelID': channelID,
                    'desc': desc,
                    'airType': airType,
                    'siteType': siteType,
                    'roomKind': roomKind,
                    'deviceType': deviceType,
                    'deviceKind': deviceKind,
                    'centerSiteKind': centerSiteKind,
                    'airTypeName': airTypeName,
                    'siteName': siteName,
                    'centerSiteKindName': centerSiteKindName,
                    'provinceID': provinceID,
                    'meteKindName': meteKindName,
                    'buildingID': buildingID,
                    'climateName': climateName,
                    'areaID': areaID,
                    'cityName': cityName,
                    'siteTypeName': siteTypeName,
                    'temperatureMeteTypeName': temperatureMeteTypeName,
                    'meteKind': meteKind,
                    'deviceTypeName': deviceTypeName,
                    'cityID': cityID,
                    'meteName': meteName,
                    'buildingName': buildingName,
                    'unit': unit,
                    'roomKindName': roomKindName,
                    'siteID': siteID,
                    'provinceName': provinceName,
                    'climateType': climateType,
                }
            }
            actions.append(action)

            # print("action行数据",action)
            if len(actions) == 100:
                helpers.bulk(es, actions)
                del actions[0:len(actions)]
        helpers.bulk(es, actions)
        if flush:
            es.indices.refresh(index=filename)



    def del_esdata_province(self):
        '''
        删除特定省份某一天的数据(删除index: fsu_20211021_01-37)
        :return:
        '''
        createim = self.imdate.split("-")
        creattime = createim[0] + createim[1] + createim[2]
        filename = "fsu_" + creattime + "_" + self.precinct_id[0:5]
        urldelindex = self.url + "/" + filename
        requests.delete(urldelindex)  # 删除index






    def del_esdata_query(self, ):
        createim = self.imdate.split("-")
        creattime = createim[0] + createim[1] + createim[2]
        filename = "fsu_" + creattime + "_" + self.precinct_id[0:5]
        indetype = "point_history_data"
        urldelmapping = self.url + "/" + filename + "/" + indetype + "/_delete_by_query"
        param = {
            "query": {
                "wildcard": {
                    "%s" %
                    (self.del_col): "%s" %
                                    (self.del_col_v)}}}
        pload = json.dumps(param)
        requests.post(urldelmapping, pload)





    def esdata_query(self,mete_code,device_id):
        date_str = self.imdate
        date = datetime2.strptime(date_str, "%Y-%m-%d")
        yesterday = date - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        print("昨天的日期是：", yesterday_str)
        createim = yesterday_str.split("-")
        creattime = createim[0] + createim[1] + createim[2]
        filename = "fsu_" + creattime + "_" + self.precinct_id[0:5]
        indetype = "point_history_data"
        urldelmapping = self.url + "/" + filename + "/" + indetype + "/_search"
        param1={
            "query": {
                "bool": {
                    "must": [{
                        "wildcard": {
                            "meteID":  mete_code
                        }
                    },
                    {
                        "wildcard": {
                            "deviceID":  device_id
                        }
                    }],
                    "must_not": [],
                    "should": []
                }
            },
            "from": 0,
            "size": 1,
            "sort": [],
            "aggs": {}
        }
        print("请求数据urldelmapping=",urldelmapping)
        print("请求数据param1=",param1)
        pload = json.dumps(param1)
        data= requests.post(urldelmapping, pload)
        print("查询到数据2", data.text)
        if data.text.__contains__("index_not_found_exception"):
            print("昨天都没有索引")
            return []
        datatexthits=json.loads(data.text)["hits"]["hits"]
        if datatexthits==[]:
            print("没有查询到数据"  )
            return []
        else:
            print("查询到数据",  datatexthits[0]["_source"]["measureVal"])
            if   datatexthits[0]["_source"]["measureVal"] is not None :
                return datatexthits[0]["_source"]["measureVal"]
            pass






if __name__ == '__main__':
        esDB(precinct_id="01-08-08-03-03", mete_code="002330", imdate="2024-07-06", minval=120, maxval=120,
         device_id='17205241694244488', env="gemc").insert_esdata_device_batch()
    esDB(precinct_id="01-08-08-03-03", mete_code="002330", imdate="2024-07-07", minval=240, maxval=240,
         device_id='17205241694244488', env="gemc").insert_esdata_device_batch()
    esDB(precinct_id="01-08-08-03-03", mete_code="002330", imdate="2024-07-08", minval=360, maxval=360,
         device_id='17205241694244488', env="gemc").insert_esdata_device_batch()
    esDB(precinct_id="01-08-08-03-03", mete_code="002330", imdate="2024-07-09", minval=480, maxval=480,
         device_id='17205241694244488', env="gemc").insert_esdata_device_batch()


    #设置区域内的所有测点值
    list_d = lastThreeDays(2)
    print(list_d)
    measureVal = 20000
    for d in list_d:
        # esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002330").del_esdata_query()
        # esDB(precinct_id="01-02-10-04-75-01", mete_code='002330', imdate=d, minval=measureVal, maxval=measureVal + 100,   estime='T00:02:03', env="release").insert_esdata_device_metecode()
        # esDB(precinct_id="01-02-10-04-75-01",imdate=d, estime='T00:02:04', env="release").insert_esdata_device_metecode()
        esDB(precinct_id="01-24-03",imdate=d, estime='T00:02:04', env="release").insert_esdata_device_metecode()
        measureVal = measureVal + 2000
