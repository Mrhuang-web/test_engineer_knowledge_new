# -*- coding: utf-8 -*-
import logging

from spider_tools.Common.esdata import esDB, lastThreeDays, afterThreeDays

if __name__ == '__main__':
    # 需要修改insert_esdata_device 中某个部分，去重下，关键字：云南ups设备_容量

    metes = ['008315','008316','008317','008318', '008319', '008320', '008338', '008339', '008340', '008322', '008349', '008350', '008351']
    # room_device = [('01-32-01-02-01-03', '00531006000005759877'), ('01-32-01-02-01-03', '37261006000000079739')]
    # room_device = [('01-32-01-02-01-04', '00531006000003792725'), ('01-32-01-02-01-04', '00531006000003792726')]
    room_device = [('01-32-01-02-01-04', '00531006000003792726')]

    for room, device in room_device:
        time = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                '16', '17', '18', '19', '20', '21', '22', '23']
        data = [50, 60, 70, 80, 90, 60, 55, 65, 75, 85, 99, 70, 60, 50, 55, 65, 75, 85, 95, 70, 60, 60, 60]
        for mete in metes:
            for time_iter, data_iter in zip(time, data):
                esDB(precinct_id=room, mete_code=mete, device_id=device,
                     imdate="2025-11-30",
                     minval=data_iter, maxval=data_iter, estime='T{}:00:00'.format(time_iter),
                     env="yunnan").insert_esdata_device()
