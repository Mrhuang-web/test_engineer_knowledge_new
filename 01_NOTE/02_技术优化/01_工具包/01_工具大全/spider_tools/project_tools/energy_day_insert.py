# -*- coding: utf-8 -*-
"""
@Time ： 2024/7/18 15:50
@Auth ： sunzhonghua
@File ：energy_day_insert.py.py
@IDE ：PyCharm
"""
from spider_tools.Common.esdata import  esDB,lastThreeDays,afterThreeDays
if __name__ == '__main__':
    # list_d = lastThreeDays(7) # lastThreeDays(4)  #  afterThreeDays(5)
    # print(list_d)
    # measureVal = 20000
    # for d in list_d:
    #     # esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002330").del_esdata_query()
    #     # esDB(precinct_id="01-02-10-04-75-01", mete_code='002330', imdate=d, minval=measureVal, maxval=measureVal + 100,   estime='T00:02:03', env="release").insert_esdata_device_metecode()
    #     # esDB(precinct_id="01-02-10-04-75-01",imdate=d, estime='T00:02:04', env="release").insert_esdata_device_metecode()
    #     esDB(precinct_id="01-24-09-04-33",imdate=d, estime='T00:02:04', env="release").insert_esdata_device_metecode()
    #     measureVal = measureVal + 2000
    # esDB(precinct_id='01-24-03-02-04', imdate='2024-07-24', del_col='meteID', del_clo_v="006011").del_esdata_query()

    # list_d = lastThreeDays(5) # lastThreeDays(4)  #  afterThreeDays(5)
    # print(list_d)
    # measureVal = 20000
    # for d in list_d:
    #     # esDB(precinct_id="01-02-10-04-11", mete_code='006327', imdate=d, minval=measureVal, maxval=measureVal + 100, estime='T00:02:03', env="release").insert_esdata_device()
    #     esDB(precinct_id="01-02-10-04-11", mete_code='006327',  device_id="16870908024244492",imdate=d, minval=measureVal, maxval=measureVal + 100, estime='T00:02:03', env="release").insert_esdata_device()
    #     esDB(precinct_id="01-02-10-04-11", mete_code='004306',  device_id="16870908024244490",imdate=d, minval=measureVal, maxval=measureVal + 100, estime='T00:02:03', env="release").insert_esdata_device()
    #     esDB(precinct_id="01-02-10-04-75-01", mete_code='002330',  device_id="1688118105429999",imdate=d, minval=measureVal, maxval=measureVal + 100, estime='T00:02:03', env="release").insert_esdata_device()
    #     measureVal = measureVal + 2000

    """
    测点电量报表：1234种异常
    list_d = lastThreeDays(13)
    for d in list_d:
        esDB(precinct_id='01-24-09-04-04', imdate=d, del_col='meteID', del_clo_v="088304").del_esdata_query()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-24", minval=100, maxval=100, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-25", minval=200, maxval=200, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-26", minval=300, maxval=300, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-27", minval=50, maxval=50, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-28", minval=150, maxval=150, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-29", minval=250, maxval=250, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-29", minval=350, maxval=350, estime='T08:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-30", minval=1, maxval=1, estime='T08:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-30", minval=350, maxval=350, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-07-31", minval=1, maxval=1, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-08-01", minval=450, maxval=450, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-08-01", minval=450, maxval=450, estime='T08:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-08-02", minval=550, maxval=550, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-08-02", minval=40001, maxval=40001, estime='T08:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-08-03", minval=40001, maxval=40001, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-08-04", minval=700, maxval=700, estime='T00:02:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-24-09-04-04", mete_code='088304',  device_id="17229117964244508",imdate="2024-08-05", minval=800, maxval=800, estime='T00:02:03', env="release").insert_esdata_device()
    """
    esDB(precinct_id='01-01-17-03-07-03-39', imdate="2024-08-09", del_col='meteID', del_clo_v="013308").del_esdata_query()
    esDB(precinct_id="01-01-17-03-07-03-39", mete_code='013308', imdate="2024-08-09", minval=10, maxval= 10,  device_id="494401061006000004244533",  estime='T18:20:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-01-17-03-07-03-39", mete_code='013308', imdate="2024-08-09", minval=20, maxval= 20,  device_id="494401061006000004244533",  estime='T18:20:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-01-17-03-07-03-39", mete_code='013308', imdate="2024-08-09", minval=120, maxval= 120,  device_id="494401061006000004244536",  estime='T18:20:03', env="release").insert_esdata_device()
    esDB(precinct_id="01-01-17-03-07-03-39", mete_code='013308', imdate="2024-08-09", minval=100, maxval= 100,  device_id="494401061006000004244536",  estime='T18:20:03', env="release").insert_esdata_device()
    esDB(precinct_id='01-39-03-01-01', imdate="2024-08-09", del_col='meteID',  del_clo_v="013348").del_esdata_query()
    esDB(precinct_id="01-39-03-01-01", mete_code='013348', imdate="2024-08-09", minval=20000, maxval= 20000,  device_id="00181006000005626132",  estime='T18:20:03', env="release").insert_esdata_device()
    # esDB(precinct_id="01-39-03-01-01", mete_code='013348', imdate="2024-08-09", minval=20000, maxval= 20000,  device_id="00181006000005626132",  estime='T17:20:03', env="release").insert_esdata_device()

    list_d = lastThreeDays(4) # lastThreeDays(4)  #  afterThreeDays(5)
    print(list_d)
    measureVal = 20000
    for d in list_d:
        # esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002330").del_esdata_query()
        # esDB(precinct_id="01-02-10-04-75-01", mete_code='002330', imdate=d, minval=measureVal, maxval=measureVal + 100,   estime='T00:02:03', env="release").insert_esdata_device_metecode()
        esDB(precinct_id="01-24-09-04-44",imdate=d, estime='T00:02:04', env="release").insert_esdata_device_metecode()
        esDB(precinct_id="01-24-09-04-45",imdate=d, estime='T00:02:04', env="release").insert_esdata_device_metecode()
        esDB(precinct_id="01-24-09-04-46",imdate=d, estime='T00:02:04', env="release").insert_esdata_device_metecode()
        esDB(precinct_id="01-24-09-04-47",imdate=d, estime='T00:02:04', env="release").insert_esdata_device_metecode()
        # esDB(precinct_id="01-39-03-01-01-01",imdate="2024-08-09", estime='T01:02:05', env="release").insert_esdata_device_metecode()
        measureVal = measureVal + 2000