# -*- coding: utf-8 -*-
import logging

from spider_tools.Common.esdata import  esDB,lastThreeDays,afterThreeDays
if __name__ == '__main__':
    # logging.basicConfig(
    #     level=logging.error,
    #     format='%(asctime)s - %(levelname)s - %(message)s',filename='./log.txt')

    # list_d = lastThreeDays(1) # lastThreeDays(4)  #  afterThreeDays(5)
    # print(list_d)
    measureVal = 20000
    # list_d = ['2025-07-16', '2025-07-17', '2025-07-18', '2025-07-19' '2025-07-20', '2025-07-21', '2025-07-22', '2025-07-23']
    list_d = ['2025-07-20','2025-07-21','2025-07-22','2025-07-23','2025-07-24','2025-07-25']


    # 机柜列5
    esDB(precinct_id="01-07-05-02-41-02", mete_code='017301',device_id='00161006000000024874', imdate="2025-09-11",
         minval=30, maxval=40, estime='T11:40:03', env="gx").insert_esdata_device()
    esDB(precinct_id="01-07-05-02-41-02", mete_code='017301',device_id='00161006000000024874', imdate="2025-09-12",
         minval=40, maxval=50, estime='T11:40:03', env="gx").insert_esdata_device()


