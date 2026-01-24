# -*- coding: utf-8 -*-
import logging

from spider_tools.Common.esdata import esDB, lastThreeDays, afterThreeDays

if __name__ == '__main__':

    # metes = ['002307', '002314', '002321', '002306', '002313', '002320', '002344', '002345', '002324']
    metes = ['001311', '001312', '001313', '001314', '001315', '001316', '001325', '001326', '001323']
    # room_device = {'01-32-11-02-02-01': '00531006000002591949'}
    room_device = {'01-32-11-02-02-11': '00531006000002597878'}

    for room, device in zip(room_device.keys(), room_device.values()):
        time = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                '16', '17', '18', '19', '20', '21', '22', '23']
        minute = ['00', '15', '30', '45']
        index1 = 0
        for mete in metes:
            for min in minute:
                esDB(precinct_id=room, mete_code=mete, device_id=device,
                     imdate="2025-12-22",
                     minval=50, maxval=70, estime='T{}:{}:00'.format(time[index1], min),
                     env="yunnan").insert_esdata_device()
            index1 += 1
