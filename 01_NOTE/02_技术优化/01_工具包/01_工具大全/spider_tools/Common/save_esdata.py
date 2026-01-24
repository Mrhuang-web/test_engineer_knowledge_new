from sqlalchemy import *
import requests
import datetime
import time
import random
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
#from Conf.Config import Config
import os


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
        #conf = Config()
        self.precinct_id = precinct_id
        self.mete_code = mete_code
        self.imdate = imdate
        self.minval = minval
        self.maxval = maxval
        self.device_id = device_id
        self.del_col = del_col
        self.del_col_v = del_clo_v
        self.dbip = "10.12.70.61"
        self.dbport = "3306"
        self.dbname = "spider2"
        self.dbuser = "root"
        self.dbpw = "Spider234"
        self.url = "http://10.12.70.61:9200"
        self.estime = estime
        engines = "mysql+mysqldb://" + self.dbuser + ":" + self.dbpw + \
            "@" + self.dbip + "/" + self.dbname + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()
        # es数据列
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
                    "siteId": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
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
        #self.sqlfile= open(str(os.path.dirname(__file__)+'/selectForESList.sql'), encoding='utf-8')
        self.sqlfile = open(str(os.path.abspath('') +
                                '/selectForESList.sql'), encoding='utf-8')
        #self.sqlfile = open(str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) + '/Params/SqlScript/'+'selectForESList.sql', encoding='utf-8')

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

    def get_provincedata(self, sqlindex):
        """
        获取数据库特定区域下的某个测点相关数据
        :return:
        """
        sqlalllist = self.get_sqllist()  # 获取预设sql
        print("sqlalllist[sqlindex]---->", sqlalllist[sqlindex])
        if sqlindex == 1:
            result = self.conn.execute(
                sqlalllist[sqlindex],
                (self.precinct_id + '%'),
                (self.mete_code),
                self.device_id)
        elif sqlindex == 2:
            result = self.conn.execute(
                sqlalllist[sqlindex],
                (self.precinct_id + '%'),
                (self.mete_code))
        elif sqlindex == 0:
            result = self.conn.execute(
                sqlalllist[sqlindex], (self.precinct_id + '%'))
        else:
            print("其他")
        row = result.fetchall()
        return row

    def insert_esdata(self):
        '''
        生成基础数据校验文档,61上的定时任务
        :return:
        '''
        creattime = datetime.datetime.now().strftime('%Y%m%d')
        # 调试用
        #creattime=(datetime.datetime.now() + datetime.timedelta(+3)).strftime("%Y%m%d")
        es = Elasticsearch(self.url, timeout=120)
        filename = "fsu_" + creattime + "_" + self.precinct_id
        indetype = "point_history_data"
        urlputindex = self.url + "/" + filename
        urlputmapping = self.url + "/" + filename + "/" + indetype + "/_mapping"
        requests.put(urlputindex)  # 新增index

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
                    "siteId": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
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
            channelID = meteID + "_" + signalNumber + "_" + desc
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
            siteId = l[35]
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
                    'siteId': siteId,
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
        es.indices.refresh(index=filename)

    def del_esdata_province02(self):
        '''
        删除特定省份某一天的数据(删除index: fsu_20211021_01-37)
        :return:
        '''
        createim = self.imdate.split("-")
        creattime = createim[0] + createim[1] + createim[2]
        filename = "fsu_" + creattime + "_" + self.precinct_id[0:5]
        urldelindex = self.url + "/" + filename
        requests.delete(urldelindex)  # 删除index

    def del_esdata_query02(self):
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


if __name__ == '__main__':
    """
    #删除index
    prelist = (
        "01-02", "01-01", "01-04", "01-05", "01-06", "01-07", "01-08", "01-09", "01-10", "01-11", "01-12", "01-13",
        "01-14",
        "01-15", "01-16", "01-17", "01-19", "01-20", "01-21", "01-22", "01-23", "01-24", "01-25", "01-26", "01-28",
        "01-29",
        "01-31", "01-32", "01-33", "01-37", "01-38",)
    for i in prelist:

        esDB(precinct_id=i, imdate='2021-10-24').del_esdata_province()
    #刪除某个测点的数据
    #esDB(precinct_id='01-38', imdate='2021-10-21', del_col='meteID', del_clo_v="017301").del_esdata_query()

    """

    collectTimestart = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print("collectTimestart:", collectTimestart)
    prelist = (
        "01-01",
        "01-02",
        "01-04",
        "01-05",
        "01-06",
        "01-07",
        "01-08",
        "01-09",
        "01-10",
        "01-11",
        "01-12",
        "01-13",
        "01-14",
        "01-15",
        "01-16",
        "01-17",
        "01-19",
        "01-20",
        "01-21",
        "01-22",
        "01-23",
        "01-24",
        "01-25",
        "01-26",
        "01-28",
        "01-29",
        "01-31",
        "01-32",
        "01-33",
        "01-37",
        "01-38",
    )
    for key in prelist:
        esDB(precinct_id=key).insert_esdata()
    collectTimeend = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print("collectTimeend:", collectTimeend)
