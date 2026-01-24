# -*- coding:utf-8 -*-
'''
性能测试的要求, 单接入点的背景数据如下：
实时告警：10W；   历史数据100W;
    其中实时告警只用写表： d_activealarm
    历史数据需要写1张表： d_signalh
    # 偏移值查询数据库：select * from alert_seq_log where seq_type='cinterface_in_alarm401'
d_activealarm_id_SN = 6000

# 偏移值查询redis, 3.5版本：dtah_sync_id_401 或 dtdh_sync_id_401,    4.0版本：signalh_sync_id_110
SELECT   * FROM  spider2.t_cfg_cserverinfo_mapping
select * from spider2.alert_seq_log where seq_type='cinterface_in_alarm732'  0
SELECT   MIN(Id)  FROM  cinterdb400_01.d_activealarm     WHERE  SiteId IN ("620402009","620402010") ;140327
SELECT   MAx(Id)  FROM  cinterdb400_01.d_activealarm     WHERE  SiteId IN ("620402009","620402010"); 280326
SELECT   COUNT(*)  FROM  cinterdb400_01.d_activealarm     WHERE  SiteId IN ("620402009","620402010") AND   Id >=140327  AND  Id <=280326    14w
select * from spider2.alert_seq_log where seq_type='cinterface_in_alarm721' 100326
SELECT   MIN(Id)  FROM  cinterdb_h.d_activealarm     WHERE  SiteId IN ("620402095","620402096") 100228
SELECT   MAx(Id)  FROM  cinterdb_h.d_activealarm     WHERE  SiteId IN ("620402095","620402096") 150227
SELECT   COUNT(*)  FROM  cinterdb_h.d_activealarm     WHERE  SiteId IN ("620402095","620402096") AND   Id >100228  AND  Id <150227     5w
'''
import time
from random import random
import  random
import  pymysql
from datetime import datetime
maId=446190765
d_activealarm_id_SN = maId + 1  # SELECT  MAX(Id)  FROM  d_activealarm
d_tah_id_SN = 446142983 + 1  # SELECT   MAX(Id)   FROM  d_signalh


def create_activealarm(number=1000, filename='d_activealarm.sql', siteId=""):
    '''一次856条'''
    global d_activealarm_id_SN
    re = get_sql_result(sql='SELECT  MAX(Id)  FROM  d_activealarm')
    maxId = re[0][0] + 1
    d_activealarm_id_SN = maxId + 1
    sql = 'SELECT  SCID,  SiteID  ,DeviceID ,`Type`, SignalID,SignalNumber,SignalName,AlarmLevel FROM m_signal  ggg  WHERE  SiteID IN (' + siteId + ') AND  ggg.`Type`=0'
    print(sql)

    result = get_sql_result(sql)

    # print(result)
    # INSERT INTO `d_activealarm`(`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `NMAlarmID`, `SerialNo`, `AlarmTime`, `AlarmLevel`, `AlarmStatus`, `AlarmDesc`, `AlarmValue`, `SynNo`, `AlarmRemark`)
    # VALUES(100027, '1', '6240405', '22221711954912', 0, '006321', '3', '电池总容量过低告警', '006005', 11065418, '2024-04-01 06:53:20', 4, 2, '下限告警-触发值169.5V', 500, 24545837, NULL);
    first_line = '''INSERT INTO d_activealarm (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `NMAlarmID`, `SerialNo`, `AlarmTime`, `AlarmLevel`, `AlarmStatus`, `AlarmDesc`, `AlarmValue`, `SynNo`, `AlarmRemark`) VALUES '''
    # first_line = '''INSERT INTO d_activealarm (Id, NodeId, LSCId, NMAlarmID, SerialNo, NodeName, AlarmTime, AlarmLevel, AlarmStatus, AlarmDesc, AlarmValue, LscConfirmTime, LscConfirmName, AlarmSN, AlarmParam, AlarmType, BusinessAffect, EquipmentAffect, Sign, StationName) VALUES '''

    f = open(filename, 'w+', encoding='utf-8')
    f.write(first_line + '\n')
    template_line = '''(%s, %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s',NULL)'''
    template_line_2 = '''(%s, %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s',NULL)'''

    line_list = []
    lines = 0
    iteration = 0
    while lines < number:
        # time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.mktime(time.localtime()) + iteration))
        # time_str_2 = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.mktime(time.localtime()) + iteration + 122))
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.mktime(time.localtime()) + iteration * 2))
        time_str_2 = time.strftime('%Y-%m-%d %H:%M:%S',
                                   time.localtime(time.mktime(time.localtime()) + iteration * 2 + 1000))
        # 消警的时间
        for li in result:
            (SCID, SiteID, DeviceID, Type, SignalID, SignalNumber, SignalName, AlarmLevel) = li

            serial_no = d_activealarm_id_SN

            line = template_line % (
            d_activealarm_id_SN, SCID, SiteID, DeviceID, Type, SignalID, SignalNumber, SignalName, SignalID, serial_no,
            time_str, AlarmLevel if AlarmLevel != None else 3, 0, '下限告警-触发值169.5V', "500", 24545837)
            line_list.append(line)

            d_activealarm_id_SN += 1
            lines = lines + 1

            # 这里处理消警 id号继续增加
            line_2 = template_line_2 % (
            d_activealarm_id_SN, SCID, SiteID, DeviceID, Type, SignalID, SignalNumber, SignalName, SignalID, serial_no,
            time_str_2, AlarmLevel if AlarmLevel != None else 3, 2, '下限告警-触发值169.5V', "500", 24545837,)

            line_list.append(line_2)
            d_activealarm_id_SN += 1
            lines = lines + 1
            if lines != 0 and lines % number == 0:
                break

        iteration = iteration + 1
        print("iteration=", str(iteration))

    f.write(',\n'.join(line_list) + ';')
    f.close()


def create_activealarm_by_time(number=1000, filename='d_activealarm.sql', siteId="", alert_time_begin="",
                               alert_time_end=""):
    '''一次856条'''
    global d_activealarm_id_SN
    re = get_sql_result(sql='SELECT  MAX(Id)  FROM  d_activealarm')
    maxId = re[0][0] + 1
    d_activealarm_id_SN = maxId + 1

    sql = 'SELECT  SCID,  SiteID  ,DeviceID ,`Type`, SignalID,SignalNumber,SignalName,AlarmLevel FROM m_signal  ggg  WHERE  SiteID IN (' + siteId + ') AND  ggg.`Type`=4'
    print(sql)
    result = get_sql_result(sql)
    # print(result)
    # INSERT INTO `d_activealarm`(`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `NMAlarmID`, `SerialNo`, `AlarmTime`, `AlarmLevel`, `AlarmStatus`, `AlarmDesc`, `AlarmValue`, `SynNo`, `AlarmRemark`)
    # VALUES(100027, '1', '6240405', '22221711954912', 0, '006321', '3', '电池总容量过低告警', '006005', 11065418, '2024-04-01 06:53:20', 4, 2, '下限告警-触发值169.5V', 500, 24545837, NULL);
    first_line = '''INSERT INTO d_activealarm (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `NMAlarmID`, `SerialNo`, `AlarmTime`, `AlarmLevel`, `AlarmStatus`, `AlarmDesc`, `AlarmValue`, `SynNo`, `AlarmRemark`) VALUES '''
    # first_line = '''INSERT INTO d_activealarm (Id, NodeId, LSCId, NMAlarmID, SerialNo, NodeName, AlarmTime, AlarmLevel, AlarmStatus, AlarmDesc, AlarmValue, LscConfirmTime, LscConfirmName, AlarmSN, AlarmParam, AlarmType, BusinessAffect, EquipmentAffect, Sign, StationName) VALUES '''
    f = open(filename, 'w+', encoding='utf-8')
    f.write(first_line + '\n')
    template_line = '''(%s, %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s',NULL)'''
    template_line_2 = '''(%s, %s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s',NULL)'''

    line_list = []
    lines = 0
    iteration = 0
    while lines < number:
        # time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.mktime(time.localtime()) + iteration))
        # time_str_2 = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.mktime(time.localtime()) + iteration + 122))
        time_str = alert_time_begin  # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.mktime(time.localtime()) + iteration * 2))
        time_str_2 = alert_time_end  # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.mktime(time.localtime()) + iteration * 2 + 1))
        # 消警的时间
        for li in result:
            (SCID, SiteID, DeviceID, Type, SignalID, SignalNumber, SignalName, AlarmLevel) = li
            serial_no = d_activealarm_id_SN
            line = template_line % (
            d_activealarm_id_SN, SCID, SiteID, DeviceID, Type, SignalID, SignalNumber, SignalName, SignalID, serial_no,
            time_str, AlarmLevel if AlarmLevel != None else 3, 0, '下限告警-触发值169.5V', "500", 24545837)
            line_list.append(line)
            d_activealarm_id_SN += 1
            lines = lines + 1
            # 这里处理消警 id号继续增加
            line_2 = template_line_2 % (
            d_activealarm_id_SN, SCID, SiteID, DeviceID, Type, SignalID, SignalNumber, SignalName, SignalID, serial_no,
            time_str_2, AlarmLevel if AlarmLevel != None else 3, 2, '下限告警-触发值169.5V', "500", 24545837,)
            line_list.append(line_2)
            d_activealarm_id_SN += 1
            lines = lines + 1
            if lines != 0 and lines % number == 0:
                break
        iteration = iteration + 1
        print("iteration=", str(iteration))
    f.write(',\n'.join(line_list) + ';')
    f.close()

#历史数据
def create_tah(times="", number=2, filename='d_tah.sql', siteId="" ):
    # siteId=620402005
    ''' '''
    global d_tah_id_SN
    re = get_sql_result(sql='SELECT   MAX(Id)   FROM  d_signalh')
    print(re)
    if  re[0][0] is  not None :
        maxId = re[0][0] + 1
    else:
        maxId = 1
    d_tah_id_SN = maxId + 1
    # 获取站点下的测点编码
    # sql='SELECT nodeid, lscid, nodename FROM m_aic UNION SELECT nodeid, lscid, nodename FROM m_aoc' # 1108条
    sql = 'SELECT  SCID,  SiteID  ,DeviceID ,`Type`, SignalID,SignalNumber FROM m_signal  ggg  WHERE  SiteID IN (' + siteId + ') AND  ggg.`Type`!=4'
    # print(sql)
    result = get_sql_result(sql)
    # print(result)
    if result == []:
        print("没找到测点")
        return

    # first_line = '''INSERT INTO `d_tah` (`ID`, `NODEID`, `LSCID`, `VALUE`, `UPDATETIME`) VALUES '''
    first_line = '''INSERT INTO `d_signalh` (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `Value`, `UpdateTime`) VALUES '''
    # (444638412, '1', '6240405', '22221711954912', 7, '007303', '2', 99, '2024-04-01 16:31:01');
    f = open(filename, 'w+', encoding='utf-8')
    f.write(first_line + '\n')
    current_time = datetime.now()
    current_hour = current_time.hour
    template_line = '''('%s','%s', '%s', '%s', '%s','%s','%s','%s','%s')'''
    line_list = []
    lines = 0
    iteration = 0

    while lines < number:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.mktime(time.localtime()) + iteration))
        print(time_str)
        if times != "":
            time_str = times
        for li in result:
            # print(d_tah_id_SN)
            (SCID, SiteID, DeviceID, Type, SignalID, SignalNumber) = li
            if SignalNumber == "000":
                print("SignalNumber是", SignalNumber)
                SignalNumber = 0
            Signal_v = 99
            #历史数据递增的编码-能耗、水资源
            current  = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            # print('今天日期:', current)
            day = int(current[-2:])
            #根据 DD 计算 value,天的300倍
            value = 300 * day
            # print(f'value = {value}')

            if SignalID in ( '002330', '004306', '006327', '009312', '009332', '078315', '078331', '088304',
            '088305', '088308', '092316', '092324', '001328', '013337'):
                Signal_v = value
                print(Signal_v)
            # 开关电源
            if SignalID in ("006301", "006302", "006303"):
                Signal_v = random.randint(180, 260)
                print(Signal_v)
            elif SignalID in ("006304", "006305"):
                Signal_v = 200
            elif SignalID in ("006313", "006314", "006314"):
                Signal_v = 3000
            elif SignalID in ("006306"):
                Signal_v = 300
                print(Signal_v)
            elif SignalID in ("006308"):
                Signal_v = 200
            elif SignalID in ("006309"):
                Signal_v = 500
            elif SignalID in ("006310"):
                Signal_v = 200
            elif SignalID in ("006312"):
                Signal_v = 100
            # 高压直流
            if SignalID in ("087301", "087302", "087303"):
                Signal_v = random.randint(180, 260)
                print(Signal_v)
            elif SignalID in ("087304", "087305"):
                Signal_v = 200
            elif SignalID in ("087315", "087316", "087317"):
                Signal_v = 3000
            elif SignalID in ("087306"):
                Signal_v = 300
                print(Signal_v)
            elif SignalID in ("087308"):
                Signal_v = 200
            elif SignalID in ("087309"):
                Signal_v = 500
            elif SignalID in ("087310"):
                Signal_v = 200
            elif SignalID in ("087312"):
                Signal_v = 100

            elif SignalID in ("008322", "008311"):
                Signal_v = random.uniform(0, 1)
            elif SignalID in ("008342"):
                Signal_v = random.randint(90, 120)
            elif SignalID in ("008344"):
                Signal_v = random.randint(120, 150)
            else:
                Signal_v = random.randint(20, 150)

            #写2个小时的数据
            for i in range(0,2):
                if i==current_hour:
                    pass
                else:
                    time_str = time_str.split(' ')[0] + " "+f"{i:02}"+":01:02"
                line = template_line % (
                d_tah_id_SN, SCID, SiteID, DeviceID, int(SignalID[0:3]), SignalID, SignalNumber, str(Signal_v),
                time_str)
                line_list.append(line)
                d_tah_id_SN += 1
                lines = lines + 1
                if lines != 0 and lines % number == 0:
                    break
        iteration = iteration + 1
        print("iteration=", str(iteration))
    f.write(',\n'.join(line_list) + ';')
    # print(line_list)
    conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",
                           database="cinterdb_400_sha1nxi", charset='utf8mb4',autocommit=True)
    cursor = conn.cursor()
    # 2. 读取整个 .sql 文件内容
    with open('d_tah.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read().strip()
    # 3. 执行整条 SQL（假设文件中只有一条 INSERT）
    try:
        cursor.execute(sql_content)

        print("✅ INSERT 执行成功")
    except Exception as e:
        print("❌ 执行失败：", e)

    cursor.close()
    conn.close()
    f.close()


### 连接数据库
def get_sql_result(sql='select a from b'):
    # conn = pymysql.connect(host='10.1.203.38',port=3306,user="root",password="nZ0qJ8kA1aI9",database="cinterdb_h",charset='utf8mb4')
    # conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",database="cinterdb_400_gx", charset='utf8mb4')
    # conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",  database="cinterdb_400_dcim", charset='utf8mb4')
    #集团山西
    conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",  database="cinterdb_400_sha1nxi", charset='utf8mb4')
    # conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",  database="cinterdb_400_dcim_out", charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return [li for li in result]




if __name__ == "__main__":
    """
    中间库查询ID，
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

    # create_tah(times="2025-05-20 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-05-21 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-05-22 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-06-20 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-06-21 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-06-22 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-20 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-21 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-19 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-06-18 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-06-19 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-06-20 00:29:02",number=2,siteId='"2006"')

    # create_tah(times="2025-07-29 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-28 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-27 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-26 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-25 00:29:02",number=2,siteId='"2006"')

    # create_tah(times="2025-07-21 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-22 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-23 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-24 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-25 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-26 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-27 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-28 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-29 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-30 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-07-31 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-08-01 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-08-02 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-08-03 00:29:02",number=2,siteId='"2006"')
    # create_tah(times="2025-08-04 00:29:02",number=2,siteId='"2006"')

    #告警

    # create_activealarm(1000, siteId='"2006"')
    # cinterdb_h已接入哈尔滨道里区
    # 620402091, 620402092  C站点202404091651051  C站点202404091651052
    # [620402095, 620402096] ['C站点202404091714121', 'C站点202404091714122']

    # cinterdb400_01已经接入在-大庆-萨克图
    # [620402009, 620402010] ['C站点202404091719271', 'C站点202404091719272'
    # [620402011, 620402012] ['C站点202404091722151', 'C站点202404091722152']

    create_activealarm_by_time(number=1000, filename='d_activealarm_bytime.sql', siteId="2006", alert_time_begin="2025-08-01 02:00:00", alert_time_end="2025-08-04 00:00:20")
    # create_activealarm_by_time(number=10, filename='d_activealarm_bytime.sql', siteId="2013",alert_time_begin="2025-01-01 01:00:00",alert_time_end="2025-01-01 01:00:20")
    # create_activealarm_by_time(number=10, filename='d_activealarm_bytime.sql', siteId="2013",alert_time_begin="2025-01-01 02:00:00",alert_time_end="2025-01-01 02:00:20")
    # create_activealarm_by_time(number=10, filename='d_activealarm_bytime.sql', siteId="2013",alert_time_begin="2025-01-01 03:00:00",alert_time_end="2025-01-01 03:00:20")
    # create_activealarm_by_time(number=10, filename='d_activealarm_bytime.sql', siteId="2013",alert_time_begin="2025-01-01 04:00:00",alert_time_end="2025-01-01 04:00:20")
    # create_tah(number=20,siteId='"2013"')