#-*- coding:utf-8 -*-
'''任务描述：　每天零时导出头一天的告警列表
外部通过crontab调用，每调用一次，遍历fsu表，每个fsuid均生成一个文件在指定目录下
再遍历alarm表，把该fsu下所有的告警，按序写入\Alarm\YYYYMMDD\${FSUID}_alarmXX.log
其中XX为01, 超过1M就要分文件写，　一般就直接写01吧,　直接生成一个文件好了
'''
EXEC_DIR='/root/sim/sim_fsu'    #crontab下执行时，是没有当前路径一说的
import sys,os,time
from datetime import datetime, date, timedelta
sys.path.append(EXEC_DIR)

from module import queryFtpPassword,queryAllFSUAccount,queryFsuId,queryYestodayAlarm


def main():
    #YYYYMMDD = time.strftime('%Y%m%d',time.localtime())
    #其实应该是生成头一天的告警文件
    yestoday = (date.today() + timedelta(days = -1)).strftime("%Y%m%d")
    for li in queryAllFSUAccount():
        username = li[0]
        fsuid = queryFsuId(username)
        folder = os.path.join(EXEC_DIR,'ftpfolder',fsuid,'Alarm',yestoday)
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = '{}_alarm01.log'.format(fsuid)
        alarm_content = get_yestoday_alarm_content(fsuid)
        open(os.path.join(folder,filename),'w+').write(alarm_content)

def get_yestoday_alarm_content(fsuid):
    result = ''
    result_list = []
    alarm_list = queryYestodayAlarm(fsuid,days=-1)
    if alarm_list != None:
        sn = 1
        for li in alarm_list:
            result_list.append('{}|@{}|@{}|@{}|@{}|@{}|@{}|@{}|@{}|@{}|@{}'.format(li.serialno,
                                                            li.signalid,
                                                            li.deviceid,
                                                            li.nmalarmid,
                                                            li.alarmtime,
                                                            li.alarmlevel,
                                                            li.alarmflag,
                                                            li.alarmdesc,
                                                            li.eventvalue,
                                                            li.signalnumber,
                                                            li.alarmremark))
            sn = sn + 1
    return '\n\r'.join(result_list)
if __name__=="__main__":
    main()