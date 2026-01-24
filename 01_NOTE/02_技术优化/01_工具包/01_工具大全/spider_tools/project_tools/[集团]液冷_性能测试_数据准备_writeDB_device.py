import time
from random import random
import random
import pymysql
from datetime import datetime
from datetime import timedelta

#一、根据站点、设备，写活动告警和消除告警数据 way控制是要生成历史还是实时告警
def create_activealarm(number=1000, filename='d_activealarm_by_device.sql', siteId="", deviceid="",way="",alert_time_begin="",alert_time_end=""):

    global d_activealarm_id_SN

    re = get_sql_result(sql='SELECT  MAX(Id)  FROM  d_activealarm')
    if re[0][0] is not None:
        maxId = re[0][0] + 1
    else:
        maxId = 1

    d_activealarm_id_SN = maxId + 1

    sql = f'''SELECT  SCID,  SiteID  ,DeviceID ,`Type`, SignalID,SignalNumber,SignalName,AlarmLevel FROM m_signal 
                WHERE  SiteID IN ({siteId}) 
                AND `Type`=0 
                AND DeviceID IN ({deviceid}) '''
    print(sql)
    result = get_sql_result(sql)
    if not result:
        print('生成',way,'数据：m_signal表，没找到输入站点设备或信号的测点信息\n')
        return

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
        time_way = way
        if time_way == "实时告警":
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.mktime(time.localtime()) + iteration * 2))
            time_str_2 = time.strftime('%Y-%m-%d %H:%M:%S',
                                       time.localtime(time.mktime(time.localtime()) + iteration * 2 + 1000))
        elif time_way == "历史告警":
            time_str = alert_time_begin
            time_str_2 = alert_time_end
        else:
            print('请选择是要生成实时告警 or 历史告警\n')
            return

        # 消警的时间
        for li in result:
            # 临时
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
        # print("iteration=", str(iteration))
    f.write(',\n'.join(line_list) + ';')
    #下面这部分是执行直接sql
    '''
        conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",
                               database="cinterdb_400_jt_gz", charset='utf8mb4', autocommit=True)
        cursor = conn.cursor()

        # 2. 读取整个 .sql 文件内容
        with open(filename, 'r', encoding='utf-8') as f:
            sql_content = f.read().strip()
        # 3. 执行整条 SQL（假设文件中只有一条 INSERT）
        try:
            cursor.execute(sql_content)

            print("✅ INSERT 执行成功-alert")
        except Exception as e:
            print("❌ 执行失败：", e)

        cursor.close()
        conn.close()

        '''
    f.close()
    print(way,'数据执行完毕\n')


# 二、根据站点id、设备id写历史数据
def create_tah_by_device(number=100, filename='d_tah_by_device.sql', siteId="", begin_time="", ent_time="",deviceid=''):

    ''' '''
    global d_tah_id_SN

    re = get_sql_result(sql='SELECT MAX(Id) FROM d_signalh')
    maxId = re[0][0] + 1 if re[0][0] is not None else 1
    d_tah_id_SN = maxId + 1
    # 获取站点下的测点编码
    # sql='SELECT nodeid, lscid, nodename FROM m_aic UNION SELECT nodeid, lscid, nodename FROM m_aoc' # 1108条
    # sql = 'SELECT  SCID,  SiteID  ,DeviceID ,`Type`, SignalID,SignalNumber FROM m_signal  ggg  WHERE  SiteID IN (' + siteId + ') AND  ggg.`Type`!=4'


    # 2. 根据siteId和deviceid查询信号数据
    sql = f'''SELECT SCID, SiteID, DeviceID, `Type`, SignalID, SignalNumber 
                 FROM m_signal 
                 WHERE SiteID IN ({siteId}) 
                 AND `Type` != 4 
                 AND DeviceID IN ({deviceid})'''
    signal_result = get_sql_result(sql)
    print(sql)
    if not signal_result:
        print("m_signal表，没找到输入站点的测点信息")
        return
    #统计sql有多少个结果执行
    sql3= f'''SELECT count(*) FROM m_signal WHERE SiteID IN ('{siteId}') 
                 AND `Type` != 4 
                 AND DeviceID IN ({deviceid})'''
    #print(sql3)
    count=get_sql_result(sql3)
    print('生成历史数据：查询结果为：', count[0][0],'个')

    # first_line = '''INSERT INTO `d_tah` (`ID`, `NODEID`, `LSCID`, `VALUE`, `UPDATETIME`) VALUES '''
    first_line = '''INSERT INTO `d_signalh` (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `Value`, `UpdateTime`) VALUES '''
    # (444638412, '1', '6240405', '22221711954912', 7, '007303', '2', 99, '2024-04-01 16:31:01');
    f = open(filename, 'w+', encoding='utf-8')
    f.write(first_line + '\n')
    # current_time = datetime.now()
    # current_hour = current_time.hour
    template_line = '''('%s','%s', '%s', '%s', '%s','%s','%s','%s','%s')'''

    time1 = datetime.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.strptime(ent_time, "%Y-%m-%d %H:%M:%S")
    # 计算时间差（以小时为单位） 提取相减后的时间的是全部秒数  除以3600就是除以一小时的秒数
    #第一种按小时来循环给值
    delta_hours = (time2 - time1).total_seconds() / 3600
    print('生成历史数据：时间相差：', delta_hours, '个小时')
    # 第二种按天数来循环给值  要换就换下面的循环days
    delta_days = (time2 - time1).total_seconds() / 86400
    print('生成历史数据：换算成天的话相差：', delta_days, '天')

    line_list = []
    lines = 0
    iteration = 0
    # 先遍历时间范围内的每个小时，然后再用对应的时间去循环，那就该站点下所有能查到的设备都会循环赋值一遍 区间的时间段
    for li in signal_result:
        if lines >= number:
            break
        for day in range(int(delta_days) + 1):
            current_time = time1 + timedelta(days=day)
            time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            # print(time_str)可以改为秒为单位

            (SCID, SiteID, DeviceID, Type, SignalID, SignalNumber) = li
            if SignalNumber == "000":
                print("SignalNumber是", SignalNumber)
                SignalNumber = 0
            Signal_v = 99
            # 历史数据递增的编码-能耗、水资源
            current = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            # print('今天日期:', current)
            day = int(current[-2:])
            # 根据 DD 计算 value,天的300倍
            value = 300 * day
            # print(f'value = {value}')
            # 电表-递增、归零
            if SignalID in ('002330', '004306', '006327', '009312', '009332', '078315', '078331', '088304',
                            '088305', '088308', '092316', '092324', '001328', '013337'):
                Signal_v = value
                # print(Signal_v)
            # 开关电源
            elif SignalID in ("006301", "006302", "006303"):
                Signal_v = random.randint(180, 260)
                # print(Signal_v)
            elif SignalID in ('011301', '012301', '015201', '015203', '015303', '015403', '017301'):  # 温度明细
                Signal_v = random.randint(5, 60)
            elif SignalID in ("006304", "006305"):
                Signal_v = 200
            elif SignalID in ("006313", "006314", "006314"):
                Signal_v = 3000
            elif SignalID in ("006306"):
                Signal_v = 300
                # print(Signal_v)
            elif SignalID in ("006308"):
                Signal_v = 200
            elif SignalID in ("006309"):
                Signal_v = 500
            elif SignalID in ("006310"):
                Signal_v = 200
            elif SignalID in ("006312"):
                Signal_v = 100
            # 高压直流
            elif SignalID in ("087301", "087302", "087303"):
                Signal_v = random.randint(180, 260)
                # print(Signal_v)
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

            # 写2个小时的数据

            line = template_line % (
                d_tah_id_SN, SCID, SiteID, DeviceID, int(SignalID[0:3]), SignalID, SignalNumber, str(Signal_v),
                time_str)
            line_list.append(line)
            d_tah_id_SN += 1
            lines += 1

            if lines >= number:
                break

        iteration = iteration + 1
        print('历史数据执行完第', iteration, '个result')
        # print("iteration=", str(iteration))

    f.write(',\n'.join(line_list) + ';')
    # print(line_list)
    # conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",database="cinterdb_400_jt_gz", charset='utf8mb4',autocommit=True)
    # 下面这部分是直接执行sql
    '''
    conn = pymysql.connect(host='10.1.203.120', port=3306, user="root", password="GPGAErA%ZkhMk59*jaD",
                           database="test_lsc352", charset='utf8mb4', autocommit=True)

    cursor = conn.cursor()

    # 2. 读取整个 .sql 文件内容
    with open(filename, 'r', encoding='utf-8') as f:

        sql_content = f.read().strip()

    # 3. 执行整条 SQL（假设文件中只有一条 INSERT）
    try:
        cursor.execute(sql_content)
        print("✅ INSERT 执行成功-信号编码")
    except Exception as e:
        print("❌ 执行失败：", e)

    cursor.close()
    conn.close()
    '''
    f.close()


### 连接数据库
def get_sql_result(sql='select a from b'):
    #conn = pymysql.connect(host='10.1.203.120', port=3306, user="root", password="GPGAErA%ZkhMk59*jaD",
                          #database="test_lsc352", charset='utf8mb4', autocommit=True)

    conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",
    database="cinterdb_400_jt_gz", charset='utf8mb4', autocommit=True)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return [li for li in result]


if __name__ == "__main__":

    create_activealarm(
        # filename='',
        number=100,
        siteId='2011',
        deviceid='43031,43035',
        way='历史告警',
        # 生成实时告警时，way输入实时告警，时间参数无效
        # 生成历史告警时，way输入历史告警，会根据时间参数生成
        alert_time_begin="2025-09-09 00:00:00",
        alert_time_end="2025-09-15 00:00:00"
            
    )

    create_tah_by_device(
        # filename='',
        deviceid='43031,3032',
        number=100,
        siteId='2011',
        begin_time="2025-09-09 00:00:00",
        ent_time="2025-09-15 00:00:00"
    )


