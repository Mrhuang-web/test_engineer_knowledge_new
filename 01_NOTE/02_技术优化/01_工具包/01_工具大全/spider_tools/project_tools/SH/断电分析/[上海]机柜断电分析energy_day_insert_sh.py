# -*- coding: utf-8 -*-
import logging

from spider_tools.Common.esdata import esDB, lastThreeDays, afterThreeDays

if __name__ == '__main__':

    measureVal = 20000
    list_d = ['2025-11-23']
    esDB(precinct_id="01-32-01-02-01-03", mete_code='008320', device_id='00531006000005759877', imdate="2025-11-23",
         minval=75.5, maxval=75.5, estime='T00:00:00', env="yunnan").insert_esdata_device()

    metes = ['008318', '008319', '008320', '008338', '008339', '008340', '008349', '008350', '008351']
    room_device = {'01-32-01-02-01-03': '00531006000005759877', '01-32-01-02-09-01': '37261006000000079739'}

    for room, device in zip(room_device.keys(), room_device.values()):
        time = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                '16', '17', '18', '19', '20', '21', '22', '23']
        index1 = 0
        for mete in metes:
            esDB(precinct_id=room, mete_code=mete, device_id=device,
                 imdate="2025-11-27",
                 minval=50, maxval=70, estime='T{}:00:00'.format(time[index1]), env="yunnan").insert_esdata_device()
            index1 += 1
