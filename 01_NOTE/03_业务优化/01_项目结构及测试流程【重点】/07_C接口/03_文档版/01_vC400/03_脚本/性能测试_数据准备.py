#-*- coding:utf-8 -*-
'''
性能测试的要求, 单接入点的背景数据如下：
实时告警：10W；   历史数据100W;
    其中实时告警只用写表： d_activealarm
    历史数据需要写2张表： d_tah  d_tdh
'''
import time
import pymysql

# 偏移值查询数据库：select * from alert_seq_log where seq_type='cinterface_in_alarm401'
d_activealarm_id_SN = 700000

# 偏移值查询redis, 3.5版本：dtah_sync_id_401 或 dtdh_sync_id_401,    4.0版本：signalh_sync_id_110
d_tah_id_SN = 7000000
#d_tdh_id_SN = 6000


def create_activealarm(number=1000,filename='d_activealarm.sql'):
    '''一次856条'''
    global d_activealarm_id_SN
    sql = 'SELECT nodeid, nodename,deviceid,`Describe` FROM m_dic WHERE m_dic.`Describe` LIKE "%-%" ORDER BY nodeid' # 856条
    result = get_sql_result(sql)
    #print(result)
    first_line = '''INSERT INTO d_activealarm (Id, NodeId, LSCId, NMAlarmID, SerialNo, NodeName, AlarmTime, AlarmLevel, AlarmStatus, AlarmDesc, AlarmValue, LscConfirmTime, LscConfirmName, AlarmSN, AlarmParam, AlarmType, BusinessAffect, EquipmentAffect, Sign, StationName) VALUES '''
    f = open(filename,'w+',encoding='utf-8')
    f.write(first_line + '\n')
    
    template_line = '''(%s, %s, '1', '%s', '%s', '%s', '%s', 1, 0, NULL, 1.33, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)'''
    template_line_2 = '''(%s, %s, '1', '%s', '%s', '%s', '%s', 1, 2, NULL, 1.33, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)'''

    line_list=[]
    lines = 0
    iteration = 0
    while lines < number:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.mktime(time.localtime()) + iteration*2))
        time_str_2 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.mktime(time.localtime()) + iteration*2 + 1))        #消警的时间
        for li in result:
            (node_id,node_name,device_id,nmalarmid) = li
            serial_no  = d_activealarm_id_SN
            line = template_line % (d_activealarm_id_SN, node_id, nmalarmid, serial_no,node_name,time_str)
            line_list.append(line)
            d_activealarm_id_SN += 1
            lines = lines+1
            #这里处理消警 id号继续增加
            line_2 = template_line_2 % (d_activealarm_id_SN, node_id, nmalarmid, serial_no,node_name,time_str_2)
            line_list.append(line_2)
            d_activealarm_id_SN += 1
            lines = lines + 1
            if lines != 0 and lines % number == 0:
                break
        iteration = iteration + 1
        print(iteration) 
    f.write(',\n'.join(line_list) + ';')
    f.close()

def create_tah(number=1000,filename='d_tah.sql'):
    '''一次1108条, 这里有个问题，tah只对应M＿AIC表里的测点'''
    global d_tah_id_SN
    sql = 'SELECT nodeid, lscid, nodename FROM m_aic' 
    result = get_sql_result(sql)
    #print(result)
    
    first_line = '''INSERT INTO `d_tah` (`ID`, `NODEID`, `LSCID`, `VALUE`, `UPDATETIME`) VALUES '''
    f = open(filename,'w+',encoding='utf-8')
    f.write(first_line + '\n')
    template_line = '''('%s', '%s', '%s', 14.1, '%s')'''
    line_list=[]
    lines = 0
    iteration = 0
    while lines < number:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.mktime(time.localtime()) + iteration))
        for li in result:
            (node_id,lsc_id,node_name) = li
            line = template_line % (d_tah_id_SN, node_id,lsc_id,time_str)
            line_list.append(line)
            d_tah_id_SN += 1
            lines = lines+1
            if lines != 0 and lines % number == 0:
                break
        iteration = iteration + 1
        print(iteration) 
    f.write(',\n'.join(line_list) + ';')
    f.close()

def create_tdh(number=1000,filename='d_tdh.sql'):
    '''这里有个问题，tdh只对应M＿DIC表里的测点'''
    global d_tdh_id_SN
    sql = 'SELECT nodeid, lscid, nodename FROM m_dic where m_dic.`Describe` not LIKE "%-%"  ' 
    result = get_sql_result(sql)
    #print(result)    
    first_line = '''INSERT INTO `d_tdh` (`ID`, `NODEID`, `LSCID`, `VALUE`, `UPDATETIME`) VALUES '''
    f = open(filename,'w+',encoding='utf-8')
    f.write(first_line + '\n')
    template_line = '''('%s', '%s', '%s', 14.1, '%s')'''
    line_list=[]
    lines = 0
    iteration = 0
    while lines < number:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.mktime(time.localtime()) + iteration))
        for li in result:
            (node_id,lsc_id,node_name) = li
            line = template_line % (d_tdh_id_SN, node_id,lsc_id,time_str)
            line_list.append(line)
            d_tdh_id_SN += 1
            lines = lines + 1
            if lines != 0 and lines % number == 0:
                break
        iteration = iteration + 1
        #print(iteration) 
    f.write(',\n'.join(line_list) + ';')
    f.close()

### 连接数据库
def get_sql_result(sql='select a from b'):
    conn = pymysql.connect(host='10.12.12.186',port=3306,user="root",password="nZ0qJ8kA1aI9",database="test_lsc351",charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return [li for li in result]

if __name__=="__main__":
    create_activealarm(100000)
    create_tah(1000000)
    #create_tdh(500000)