# -*- coding: utf-8 -*-
import logging

from spider_tools.Common.esdata import esDB, lastThreeDays, afterThreeDays

if __name__ == '__main__':

    # 电表
    # metes = ['092316', '092324', '092334']
    # 高压配电
    # metes = ['002330', '092316', '092324', '092334']
    metes = ['001328']
    room_device = {'01-07-05-01-01-01': '00771006000002943028'}
    # room_device_filter = {'01-07-05-02-41-01': '00771006000002943028',
    #                       '01-07-05-02-39-02-01': '00161006000000023354',
    #                       '01-07-05-02-39-02-02': '00161006000000023401',
    #                       '01-07-05-02-39-02-03': '00161006000000023513',
    #                       '01-07-05-02-39-02-04': '00161006000000023607'}
    room_device_filter = {'01-07-05-02-42-02': '00161006000000024647'}

    for room, device in zip(room_device_filter.keys(), room_device_filter.values()):
        index1 = 0
        # time = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
        #         '16', '17', '18', '19', '20', '21', '22', '23', '00']
        # time_filter = ['00', '01', '23']
        # time_filter = ['23']
        time_filter = ['00']
        for mete in metes:
            for iters in time_filter:
                esDB(precinct_id=room, mete_code=mete, device_id=device,
                     imdate="2025-12-29",
                     minval=50, maxval=70, estime='T{}:00:00'.format(iters), env="gx").insert_esdata_device()
                index1 += 1
