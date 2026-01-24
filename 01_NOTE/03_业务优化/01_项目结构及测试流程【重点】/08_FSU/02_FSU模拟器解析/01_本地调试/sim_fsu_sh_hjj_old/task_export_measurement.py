#-*- coding:utf-8 -*-
'''任务描述：　每次执行时，直接按FSU来生成对应的Measurement文件。
文件名规则：PM_FSUID_YYYYMMDDHHmm.csv

'''
EXEC_DIR='/root/sim/sim_fsu'    #crontab下执行时，是没有当前路径一说的
import sys,os,time
sys.path.append(EXEC_DIR)

#from module import queryFtpPassword,queryAllFSUAccount,queryFsuId,querySignalsObjsbyDeviceID
from module import *
import random

def main():
    for li in queryAllFSUAccount():
        username = li[0]
        fsuid = queryFsuId(username)
        folder = os.path.join(EXEC_DIR,'ftpfolder',fsuid,'Measurement')
        if not os.path.exists(folder):
            os.makedirs(folder)
        #　从当日零晨开始，每5分钟生成一个文件，直到现在。　－－如果文件已存在就不用生成了
        today = time.strftime('%Y%m%d',time.localtime())
        tmp_time = time.mktime((int(today[:4]),int(today[4:6]),int(today[6:]),0,0,0,0,0,0)) + 5*60
        while tmp_time < time.mktime(time.localtime()):
            min_str = time.strftime('%Y%m%d%H%M',time.gmtime(tmp_time))
            filename = 'PM_{}_{}.csv'.format(fsuid, min_str)
            file_content = gen_file_content(fsuid,min_str)
            if not os.path.exists(os.path.join(folder,filename)):
                open(os.path.join(folder,filename),'w+').write(file_content)
            tmp_time = tmp_time + 5*60

def gen_file_content(fsuid,min_str):
    content_list = []
    content_list.append('序号,性能数据采集时间,DeviceID,监控点ID,SignalNumber,监控点描述,监控点数据类型,监控点数据测量值')
    sn = 1
    result = session.query(Signals).filter(Signals.fsuid==fsuid).all()
    #print(len(result))
    aidi='AI'
    for li in result:
        value = '%.3f' % (random.randrange(1, 56))
        if li.type in ['3','4']:
            if li.type=='3':
                aidi = 'AI'
            else:
                aidi = 'DI'
            line = '{},{}00,{},{},{},{},{},{}'.format(sn,min_str,li.deviceid,li.signalsid,li.signalnumber,li.signalname,aidi,value)
            content_list.append(line)
            sn=sn+1
    return '\n'.join(content_list)

if __name__=="__main__":
    main()
    #print(gen_file_content('1007000000000011','2019040251759'))