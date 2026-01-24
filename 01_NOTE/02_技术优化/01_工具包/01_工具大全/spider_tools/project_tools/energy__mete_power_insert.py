# -*- coding: utf-8 -*-
from spider_tools.Common.esdata import  esDB,lastThreeDays,afterThreeDays
if __name__ == '__main__':
    list_d = lastThreeDays(1)  # lastThreeDays(4)  #  afterThreeDays(5)
    print(list_d)
    for d in list_d:
        estime1='T14:02:04'
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="088306").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="088307").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="088309").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="001325").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="001311").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="001312").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="001313").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002345").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002321").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002314").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002307").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002339").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="002307").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="004307").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="005316").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="005317").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="005318").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="005352").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="092330").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="009307").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="009308").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="009309").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="009313").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="092308").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="092309").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="092310").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="092330").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="078307").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="078308").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="078309").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="009326").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="009327").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="009328").del_esdata_query()
        esDB(precinct_id='01-24', imdate=d, del_col='meteID', del_clo_v="009331").del_esdata_query()

        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957844244508' AND precinct_id = "01-24-09-04-44";
        esDB(precinct_id="01-24-09-04-44-02", mete_code="088306", imdate=d, minval=50, maxval=50,device_id='17242957844244508', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="088307", imdate=d, minval=50, maxval=50,device_id='17242957844244508', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="088309", imdate=d, minval=50, maxval=50,device_id='17242957844244508', estime=estime1, env="release").insert_esdata_device()

        #高压配电 正向有功电能 001328
        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957834244487' AND precinct_id = "01-24-09-04-44";
        #esDB(precinct_id="01-24-09-04-44-02", mete_code="001325", imdate=d, minval=50, maxval=50,device_id='17242957834244487', estime=estime1, env="release").insert_esdata_device()
        #或者
        esDB(precinct_id="01-24-09-04-44-02", mete_code="001311", imdate=d, minval=50, maxval=50,device_id='17242957834244487', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="001312", imdate=d, minval=50, maxval=50,device_id='17242957834244487', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="001313", imdate=d, minval=50, maxval=50,device_id='17242957834244487', estime=estime1, env="release").insert_esdata_device()

        #低压交流配电	正向有功电能 002330	--》002307+002314+002321 或者	002345
        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957834244488' AND precinct_id = "01-24-09-04-44";
        #esDB(precinct_id="01-24-09-04-44-02", mete_code="002345", imdate=d, minval=50, maxval=50,device_id='17242957834244488', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="002321", imdate=d, minval=50, maxval=50,device_id='17242957834244488', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="002314", imdate=d, minval=50, maxval=50,device_id='17242957834244488', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="002307", imdate=d, minval=50, maxval=50,device_id='17242957834244488', estime=estime1, env="release").insert_esdata_device()
        
        #低压交流配电	分路XX有功电能	002338(不在关键测点)	无	无	无	002339
        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957834244488' AND precinct_id = "01-24-09-04-44";
        esDB(precinct_id="01-24-09-04-44-02", mete_code="002339", imdate=d, minval=50, maxval=50,device_id='17242957834244488', estime=estime1, env="release").insert_esdata_device()
        
        #低压直流配电	分路XX电能	004306	无	无	无	004307
        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957834244490' AND precinct_id = "01-24-09-04-44";
        esDB(precinct_id="01-24-09-04-44-02", mete_code="004307", imdate=d, minval=50, maxval=50,device_id='17242957834244490', estime=estime1, env="release").insert_esdata_device()
                
        
        #发电机组  总发电量 005353(不在关键测点)  005316 005317 005318 005352
        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957834244491' AND precinct_id = "01-24-09-04-44";
        esDB(precinct_id="01-24-09-04-44-02", mete_code="005316", imdate=d, minval=50, maxval=50, device_id='17242957834244491', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="005317", imdate=d, minval=50, maxval=50, device_id='17242957834244491', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="005318", imdate=d, minval=50, maxval=50, device_id='17242957834244491', estime=estime1, env="release").insert_esdata_device()
        #esDB(precinct_id="01-24-09-04-44-02", mete_code="005352", imdate=d, minval=50, maxval=50, device_id='17242957834244491', estime=estime1, env="release").insert_esdata_device()
        

        #UPS配电 分路XX有功电能009312 009307 009308 009309 009313
        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957844244495' AND precinct_id = "01-24-09-04-44";
        esDB(precinct_id="01-24-09-04-44-02", mete_code="009307", imdate=d, minval=50, maxval=50, device_id='17242957844244495', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="009308", imdate=d, minval=50, maxval=50, device_id='17242957844244495', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="009309", imdate=d, minval=50, maxval=50, device_id='17242957844244495', estime=estime1, env="release").insert_esdata_device()
        #esDB(precinct_id="01-24-09-04-44-02", mete_code="009313", imdate=d, minval=50, maxval=50, device_id='17242957844244495', estime=estime1, env="release").insert_esdata_device()

        #UPS配电 输入XX正向有功电能 009332 009326 009327 009328 009331
        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957844244495' AND precinct_id = "01-24-09-04-44";
        esDB(precinct_id="01-24-09-04-44-02", mete_code="009326", imdate=d, minval=50, maxval=50, device_id='17242957844244495', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="009327", imdate=d, minval=50, maxval=50, device_id='17242957844244495', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="009328", imdate=d, minval=50, maxval=50, device_id='17242957844244495', estime=estime1, env="release").insert_esdata_device()

        #esDB(precinct_id="01-24-09-04-44-02", mete_code="009331", imdate=d, minval=50, maxval=50, device_id='17242957844244495', estime=estime1, env="release").insert_esdata_device()

        #风光设备 总发电量 078331 078307 078308 078309
        #风光设备 正向有功电能 078315 078307 078308 078309
        #SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957844244506' AND precinct_id = "01-24-09-04-44";
        esDB(precinct_id="01-24-09-04-44-02", mete_code="078307", imdate=d, minval=50, maxval=50, device_id='17242957844244506', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="078308", imdate=d, minval=50, maxval=50, device_id='17242957844244506', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="078309", imdate=d, minval=50, maxval=50, device_id='17242957844244506', estime=estime1, env="release").insert_esdata_device()
         
        #智能电表 正向有功电能 092316  092308 092309 092310 092330
        # SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957844244509' AND precinct_id = "01-24-09-04-44";
        #3个没写进去
        esDB(precinct_id="01-24-09-04-44-02", mete_code="092308", imdate=d, minval=50, maxval=50, device_id='17242957844244509', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="092309", imdate=d, minval=50, maxval=50, device_id='17242957844244509', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="092310", imdate=d, minval=50, maxval=50, device_id='17242957844244509', estime=estime1, env="release").insert_esdata_device()
        # esDB(precinct_id="01-24-09-04-44-02", mete_code="092330", imdate=d, minval=50, maxval=50, device_id='17242957844244509', estime=estime1, env="release").insert_esdata_device()

        #智能电表 总电度 092324  092330
        # SELECT * FROM  energy_device_mete_power  WHERE device_id = '17242957844244509' AND precinct_id = "01-24-09-04-44";
        esDB(precinct_id="01-24-09-04-44-02", mete_code="092330", imdate=d, minval=5000000000, maxval=32924834.5, device_id='17242957844244509', estime=estime1, env="release").insert_esdata_device()

        #智能电表  第XX路正向有功电能  092334  092308 092309  092310
        esDB(precinct_id="01-24-09-04-44-02", mete_code="092308", imdate=d, minval=50, maxval=50, device_id='17242957844244509', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="092309", imdate=d, minval=50, maxval=50, device_id='17242957844244509', estime=estime1, env="release").insert_esdata_device()
        esDB(precinct_id="01-24-09-04-44-02", mete_code="092310", imdate=d, minval=50, maxval=50, device_id='17242957844244509', estime=estime1, env="release").insert_esdata_device()

