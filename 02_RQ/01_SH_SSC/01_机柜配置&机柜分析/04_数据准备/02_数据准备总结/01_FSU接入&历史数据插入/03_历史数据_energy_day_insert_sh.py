# -*- coding: utf-8 -*-


from Common.esdata import  esDB,lastThreeDays,afterThreeDays
import datetime
if __name__ == '__main__':

    list_d = lastThreeDays(0) # lastThreeDays(4)  #  afterThreeDays(5)
    print(list_d)
    measureVal = 20000
    for d in list_d:
        # esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002330").del_esdata_query()
        esDB(precinct_id="01-01-23-03-18-01-01",imdate=d, estime='T00:02:04', env="sh").insert_esdata_device_metecode()
        # esDB(precinct_id="01-01-23-03-06-01-02",imdate=d, estime='T00:02:04', env="sh").insert_esdata_device_metecode()

        measureVal = measureVal + 2000


