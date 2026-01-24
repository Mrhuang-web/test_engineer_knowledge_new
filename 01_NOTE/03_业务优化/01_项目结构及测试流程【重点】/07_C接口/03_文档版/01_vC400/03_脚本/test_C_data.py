# -*- coding:utf-8 -*-
import  C_data  as CD
CD.d_activealarm_id_SN=446143093 + 1  # SELECT  MAX(Id)  FROM  d_activealarm
CD.d_tah_id_SN = 446142984 + 1  # SELECT   MAX(Id)   FROM  d_signalh
if __name__ == "__main__":
    """
    中间库查询ID,ID要比当前最大的大，
    d_activealarm_id_SN = 23233+1 # SELECT  MAX(Id)  FROM  d_activealarm
    d_tah_id_SN = 446142983+1      #SELECT   MAX(Id)   FROM  d_signalh
    """
    # create_tah(times="2024-11-26 04:29:02",number=2000,siteId='"1"')
    # create_tah(times="2024-11-26 07:01:01",number=2000,siteId='"1"')
    # create_tah(times="2024-11-27 07:01:02",number=2000,siteId='"1"')
    # create_tah(times="2025-01-14 12:01:02",number=300,siteId='"2013"')
    # create_tah(times="2024-11-23 21:01:02",number=2000,siteId='"1"')
    # create_activealarm(100, siteId='"2013"')
    # create_tah(times="2024-11-26 21:01:03",number=2000,siteId='"1"')

    # create_tah(times="2024-11-25 16:29:02",number=2,siteId='"1"')
    # create_activealarm(10, siteId='"1"')
    #
    CD.create_tah(number=20,siteId='"2013"')
    # create_activealarm(100000, siteId='"620402029"')

    # cinterdb_h已接入哈尔滨道里区
    # 620402091, 620402092  C站点202404091651051  C站点202404091651052
    # [620402095, 620402096] ['C站点202404091714121', 'C站点202404091714122']

    # cinterdb400_01已经接入在-大庆-萨克图
    # [620402009, 620402010] ['C站点202404091719271', 'C站点202404091719272'
    # [620402011, 620402012] ['C站点202404091722151', 'C站点202404091722152']


    CD.create_activealarm_by_time(number=10, filename='d_activealarm_bytime.sql', siteId="2013",alert_time_begin="2025-01-01 01:00:00",alert_time_end="2025-01-01 01:00:20")
    # create_activealarm_by_time(number=10, filename='d_activealarm_bytime.sql', siteId="2013",alert_time_begin="2025-01-01 02:00:00",alert_time_end="2025-01-01 02:00:20")
    # create_activealarm_by_time(number=10, filename='d_activealarm_bytime.sql', siteId="2013",alert_time_begin="2025-01-01 03:00:00",alert_time_end="2025-01-01 03:00:20")
    # create_activealarm_by_time(number=10, filename='d_activealarm_bytime.sql', siteId="2013",alert_time_begin="2025-01-01 04:00:00",alert_time_end="2025-01-01 04:00:20")
