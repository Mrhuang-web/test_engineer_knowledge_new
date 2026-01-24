import time
from random import random
import random
import pymysql
from typing import List, Iterable, Optional

from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

"""
    三个时间段：4点，12点，20点

    单设备：
        单侧点，3测点，5测点
    多设备：
        整点有:    
            eg:04:00:00,04:00:01,03:59:59,03:30:00,04:30:00
        整点没:
            eg:04:00:01,03:59:59,03:30:00,04:30:00
        边界(闭区间/开区间):
            eg:03:00:00,05:00:00
        超过1h
            eg:05:00:01,02:59:59
        缺失时刻
            eg:04:00:00完全没有数据

    引入 status 策略控制：
        status=0：整点前后1秒 + 前后30分
        status=1：整点无值，前后1秒/30分有值
        status=2：边界值（前后1小时整点）
        status=3：超出1小时（前后1小时1秒）
        status=4：缺失（该小时不生成）

"""

FMT = "%Y-%m-%d %H:%M:%S"


# 一、根据站点、信号-通道、设备、设备类型，写活动告警和消除告警数据 way控制是要生成历史还是实时告警【待补充】
# 二、根据站点ID、设备id、信号id写全量历史数据
def create_tah_by_device_signal(f=None, number=100, filename='d_tah_by_device_signal.sql',
                                begin_time="", end_time="", status_time=1, skip_hours=(0,),
                                siteId="", roomId="",
                                deviceid="", signalid="", signal_number="",
                                device_no='', mode='',
                                val_min: Optional[float] = None, val_max: Optional[float] = None):
    # 获取目前历史数据表中最大的id
    global d_tah_id_SN

    re = get_sql_result(sql='SELECT MAX(Id) FROM d_signalh')
    maxId = re[0][0] + 1 if re[0][0] is not None else 1
    d_tah_id_SN = maxId + 1

    # 批量插入
    global line_list
    line_list = []

    # 获取指定站点机房下的液冷设备 -- 区分字典 [公用]
    yl_device_name = ["'1#工况环境'", "'中央空调主机'", "'2#工况环境'", "'系统参数'", "'1#一次侧机组（冷机/冷塔）'",
                      "'2#一次侧机组（冷机/冷塔）'", "'CDU1'" , "'3#冷机'" , "'1#冷机'" , "'2#冷机'",
                      "'室外环境设备'"
                      ]
    to_str = ",".join(yl_device_name)
    device_rows = get_sql_result(
        sql=f"""SELECT DeviceID,DeviceName FROM m_device where SiteID IN ({siteId}) AND DeviceName in ({to_str}) AND RoomID in ({roomId})""")


    # 按具体设备测点插入
    if mode == "0":
        # sql = f'''SELECT SCID, SiteID, DeviceID, `Type`, SignalID, SignalNumber
        #                      FROM m_signal
        #                      WHERE SiteID IN ({siteId})
        #                      AND RoomID IN ({roomId})
        #                      AND `Type` != 4
        #                      AND SignalID IN ({signalid})
        #                      AND DeviceID IN ({deviceid})
        #                      AND SignalNumber IN ({signal_number})'''

        sql = f'''SELECT SCID, SiteID, DeviceID, `Type`, SignalID, SignalNumber ,SignalName
                             FROM m_signal 
                             WHERE SiteID IN ({siteId}) 
                             AND `Type` != 4 
                             AND SignalID IN ({signalid})
                             AND deviceid IN ({deviceid})
                             AND SignalNumber IN ({signal_number})'''
        signal_result = get_sql_result(sql)

        if not signal_result:
            print("生成历史数据：m_signal表，没找到输入站点的测点信息")
            return

        time_list = generate_times_by_status(begin_time, end_time, status_time, skip_hours)
        Signal_v = get_value(val_min=val_min, val_max=val_max)
        write_signal(f, d_tah_id_SN, signal_result, filename, begin_time, end_time, number, time_list, Signal_v)
        return

    # 按站点机房自动匹配
    device_rows = get_sql_result(
        sql=f"""SELECT DeviceID,DeviceName FROM m_device where SiteID IN ({siteId}) AND RoomID in ({roomId})""")

    if mode == "1":


        if device_no == "1":
            seen = set()
            unique_names = []
            unique_devices = []
            all_devices = []


            # 展示不取这个去重
            for device_id, device_name in device_rows:
                key = device_name[2:]  # 去掉前缀
                all_devices.append(device_id)
                if key not in seen:
                    seen.add(key)
                    unique_names.append(device_name)
                    unique_devices.append(device_id)
            device_ids_str = ",".join([f"'{id}'" for id in all_devices])

            # 第三步：构造 DeviceID 列表字符串  (先把unique_devices  换成 all_devices)  todo

            # 第四步：构造 SignalID 列表字符串
            signal_list = ['013351', '013352', '013353', '012325', '012318', '012321', '013323'
            , '013330', '012326', '012329', '012333', '012339', '012340', '012334', '012345', '012344', '013405']
            signal_ids_str = ",".join([f"'{id}'" for id in signal_list])

            # 第五步：构建最终结果字段
            sql = f'''SELECT SCID, SiteID, DeviceID, `Type`, SignalID, SignalNumber ,SignalName
                         FROM m_signal 
                         WHERE 
                         SiteID IN ('{siteId}') 
                         AND `Type` != 4 
                         AND SignalID IN ({signal_ids_str})
                         AND DeviceID IN ({device_ids_str})
                         AND SignalNumber IN ({signal_number})'''
            signal_result = get_sql_result(sql)

            if not signal_result:
                print("生成历史数据：m_signal表，没找到输入站点的测点信息")
                return
            time_list = generate_times_by_status(begin_time, end_time, status_time, skip_hours)
            Signal_v = get_value(val_min=val_min, val_max=val_max)
            write_signal(f, d_tah_id_SN, signal_result, filename, begin_time, end_time, number, time_list, Signal_v)


def write_signal(f, d_tah_id_SN, signal_result, filename, begin_time, end_time, number, time_list, Signal_v):
    template_line = '''('%s','%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')'''

    time1 = datetime.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    # 计算时间差（以小时为单位） 提取相减后的时间的是全部秒数  除以3600就是除以一小时的秒数

    # 第一种按小时来循环给值
    delta_hours = (time2 - time1).total_seconds() / 3600
    print('生成历史数据：相差：', delta_hours, '个小时')
    # 第二种按天数来循环给值  要换就换下面的循环days
    delta_days = (time2 - time1).total_seconds() / 86400
    print('生成历史数据：换算成天相差：', delta_days, '天')

    # line_list = []
    lines = 0
    iteration = 0
    # 先遍历时间范围内的每个小时，然后再用对应的时间去循环，那就该站点下所有能查到的设备都会循环赋值一遍 区间的时间段


    for li in signal_result:
        # if number is not None:
        #     if lines >= number:
        #         break
        line_list = []

        filename = 'd_tah_by_device_signal.sql'
        first_line = '''INSERT INTO `d_signalh` (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `Value`, `UpdateTime`, `SignalDesc`) VALUES '''
        # (444638412, '1', '6240405', '22221711954912', 7, '007303', '2', 99, '2024-04-01 16:31:01' , SignalDesc);
        f = open(filename, 'w+', encoding='utf-8')
        f.write(first_line + '\n')

        for day in time_list:
            day_shift = datetime.strptime(day, "%Y-%m-%d %H:%M:%S")
            time_str = day_shift.strftime("%Y-%m-%d %H:%M:%S")
            (SCID, SiteID, DeviceID, Type, SignalID, SignalNumber, SignalName) = li
            if SignalNumber == "000":
                print("SignalNumber是", SignalNumber)
                SignalNumber = 0
            # 写2个小时的数据
            # 测点信号 - 前三位是设备类型
            line = template_line % (
                d_tah_id_SN, SCID, SiteID, DeviceID, int(SignalID[0:3]), SignalID, SignalNumber, str(Signal_v),
                time_str, SignalName)
            print(line)
            line_list.append(line)
            d_tah_id_SN += 1
            lines += 1
            # todo 这里被注释了,原本有的
            # if number is not None and lines >= number:
            #     break
            Signal_v = get_value(val_min=val_min, val_max=val_max)

        print('生成历史数据：执行成功第', iteration, '个result')
        f.write(',\n'.join(line_list) + ';')


            # 补充写入
        conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",
                                   database="cinterdb_400_jt_gz", charset='utf8mb4', autocommit=True)
        cursor = conn.cursor()
        with open(filename, 'r', encoding='utf-8') as f:
            sql_content = f.read().strip()
        # 3. 执行整条 SQL（假设文件中只有一条 INSERT）
        try:
            cursor.execute(sql_content)
            print("✅ INSERT 执行成功-信号编码")

            re = get_sql_result(sql='SELECT MAX(Id) FROM d_signalh')
            maxId = re[0][0] + 1 if re[0][0] is not None else 1
            d_tah_id_SN = maxId + 1

        except Exception as e:
            print("❌ 执行失败：", e)
        cursor.close()
        conn.close()

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                pass  # 写入空内容
                f.close()
            print(f"✅ 文件 {filename} 已清空")
        except Exception as e:
            print(f"❌ 清空文件时出错: {e}")


        iteration = iteration + 1
    #     print('生成历史数据：执行成功第', iteration, '个result')
    # f.write(',\n'.join(line_list) + ';')


# 获取插入时间数
def generate_times_by_status(start_str: str, end_str: str, status: int, skip_hours: Iterable[int] = (), ) -> List[str]:
    """
    字符串版：在 [start_str, end_str] 区间内，
    每天 04、12、20 点按 status 规则批量生成插值时间点，
    并剔除整组“跳过小时”的所有衍生时刻。

    参数
    ----
    start_str / end_str : str
        格式 "YYYY-MM-DD HH:MM:SS"
    status : int
        0 -> 整点+前后1秒+前后30分 (5 条)
        1 -> 前后1秒+前后30分     (4 条)
        2 -> 前后1小时整点       (2 条)
        3 -> 前后1小时再多1秒     (2 条)
        4
        5 -> 缺失（直接返回空）
    skip_hours : Iterable[int], optional
        需要跳过的小时列表，例如 {4, 20} 表示每天 4 点和 20 点整组都不要；
        只影响当天对应小时，其他小时不受影响。

    返回
    ----
    List[str]
        升序、去重、已剔除跳过小时、且全部落在 [start_str, end_str] 内的结果
    """
    try:
        start = parser.parse(start_str)
        end = parser.parse(end_str)
    except Exception as e:
        raise ValueError(f"日期格式错误: {e}，正确示例: 2023-02-01 00:00:00")

    if start > end:
        raise ValueError("start_str 必须 ≤ end_str")

    skip_set = {int(h) for h in skip_hours}

    if status == 5:
        return []

    # 1. 生成每天 3 个基准整点
    base_times: List[datetime] = []
    cur_date = start.date()
    end_date = end.date()
    while cur_date <= end_date:
        for hh in (4, 12, 20):
            if hh in skip_set:  # 整组跳过
                continue
            base = datetime.combine(cur_date, datetime.min.time()) + timedelta(hours=hh)
            if base < start or base > end:
                continue
            base_times.append(base)
        cur_date += timedelta(days=1)

    # 2. 按 status 展开候选点
    candidates: List[datetime] = []
    for base in base_times:
        if status == 0:
            candidates.extend([
                base,
                base + relativedelta(seconds=-1),
                base + relativedelta(seconds=+1),
                base + relativedelta(minutes=-30),
                base + relativedelta(minutes=+30),
            ])
        elif status == 1:
            candidates.extend([
                base + relativedelta(seconds=-1),
                base + relativedelta(seconds=+1),
                base + relativedelta(minutes=-30),
                base + relativedelta(minutes=+30),
            ])
        elif status == 2:
            candidates.extend([
                base + relativedelta(hours=-1),
                base + relativedelta(hours=+1),
            ])
        elif status == 3:
            candidates.extend([
                base + relativedelta(hours=-1, seconds=-1),
                base + relativedelta(hours=+1, seconds=+1),
            ])
        elif status == 4:
            candidates.extend([
                base + relativedelta(seconds=-1)
            ])

    # 3. 去重 + 排序 + 转字符串
    filtered = sorted({t for t in candidates if start <= t <= end})
    return [t.strftime(FMT) for t in filtered]


# 获取插入值
def get_value(val_min: Optional[float] = None, val_max: Optional[float] = None, default: float = 10.0,
              seed: Optional[float] = None, ) -> float:
    """
    统一获取数值的入口。

    规则
    ----
    1. 同时给出 val_min 和 val_max → 在 [val_min, val_max] 内随机返回 int
    2. 否则直接返回 default
    3. 支持外部随机种子（可选）
    """
    if val_min is not None and val_max is not None:
        if val_min > val_max:
            raise ValueError("val_min 必须 ≤ val_max")
        if seed is not None:
            random.seed(seed)
        return round(random.uniform(val_min, val_max), 3)
    return default


### 连接数据库
def get_sql_result(sql='select a from b'):
    conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",
                           database="cinterdb_400_jt_gz", charset='utf8mb4', autocommit=True)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return [li for li in result]


if __name__ == "__main__":
    """
        1#工况环境，2#工况环境，1#一次侧机组（冷机/冷塔），系统参数，2#一次侧机组（冷机/冷塔），CDU
        signle 可以传单个，也可以传多个
        device_no 空值为单设备还是多设备
        由site和room决定是哪个机房下设备
        mode = 1 不指定设备测点，= 0 时指定

        status : int
            0 -> 整点+前后1秒+前后30分 (5 条)
            1 -> 前后1秒+前后30分     (4 条)
            2 -> 前后1小时整点       (2 条)
            3 -> 前后1小时再多1秒     (2 条)
            4 -> 缺失（直接返回空）
    """

    # 全局文件开启
    # filename = 'd_tah_by_device_signal.sql'
    # first_line = '''INSERT INTO `d_signalh` (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `Value`, `UpdateTime`, `SignalDesc`) VALUES '''
    # # (444638412, '1', '6240405', '22221711954912', 7, '007303', '2', 99, '2024-04-01 16:31:01' , SignalDesc);
    # f = open(filename, 'w+', encoding='utf-8')
    # f.write(first_line + '\n')


    # # 方式1：指定测点
    # create_tah_by_device_signal(
    #     # filename='',
    #     f=f,
    #     mode="0",
    #     device_no="1",
    #     siteId="2025",
    #     roomId="202507",
    #     deviceid='57886',  # 57934  012325   012321   012318   57933
    #     signalid='012325',
    #     signal_number='1,2,3,4,5',
    #     val_max=100, val_min=100,
    #     begin_time="2025-11-02 00:00:00",
    #     end_time="2025-11-03 23:59:59"
    # )
    # f.close()

    # 方式2：站点机房指定到测点  -- 循环
    # for x in range(2025, 2028):  # 站点控制
    #     for y in range(1, 2):  # 机房控制
    #         if y < 10:
    #             roomid = f"{x}" + "0" + f"{y}"
    #         else:
    #             roomid = f"{x}" + f"{y}"
    #
    #         # 单设备，类型0 -
    #         create_tah_by_device_signal(
    #             # filename='',
    #             f=f,
    #             mode="1",
    #             device_no="1",
    #             siteId=f"{x}",
    #             roomId=roomid,
    #             signal_number='1,2,3,4,5',
    #             begin_time="2025-11-02 00:00:00",
    #             end_time="2025-11-03 23:59:59",
    #             status_time=0,
    #             # skip_hours=(4,),
    #             val_max=50, val_min=20,
    #             # number=10
    #         )
    # f.close()

    # # 不循环版本
    # create_tah_by_device_signal(
    #     # filename='',
    #     f=f,
    #     mode="1",
    #     device_no="1",
    #     siteId='2028',
    #     roomId='202801',
    #     signal_number='1,2,3,4,5',
    #     begin_time="2025-09-06 00:00:00",
    #     end_time="2025-11-07 23:59:59",
    #     status_time=1,
    #     # skip_hours=(4, 12),
    #     val_max=10, val_min=10,
    #     # number=10
    # )
    # f.close()







    start_time = time.time()

    from datetime import datetime, timedelta

    # 基础参数配置
    device_no = "1"
    siteId = '2028'
    roomId = '202801'
    signal_number = '0,1,2,3,4,5'
    status_time = 1
    val_min = 20
    val_max = 50

    # 时间范围
    # start_str = "2025-09-08 00:00:00"
    start_str = "2025-11-01 00:00:00"
    end_str = "2025-11-02 23:59:59"

    # 转换为datetime对象
    current_start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
    overall_end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")

    # 3天间隔
    interval = timedelta(days=3)

    # 文件
    filename = 'd_tah_by_device_signal.sql'

    # 循环处理每个时间段
    while current_start < overall_end:
        # 计算本次结束时间（3天-1秒）
        current_end = min(current_start + interval - timedelta(seconds=1), overall_end)

        # 格式化时间字符串
        begin_time = current_start.strftime("%Y-%m-%d %H:%M:%S")
        end_time = current_end.strftime("%Y-%m-%d %H:%M:%S")


        # 文件
        filename = 'd_tah_by_device_signal.sql'
        first_line = '''INSERT INTO `d_signalh` (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `Value`, `UpdateTime`, `SignalDesc`) VALUES '''
        # (444638412, '1', '6240405', '22221711954912', 7, '007303', '2', 99, '2024-04-01 16:31:01' , SignalDesc);
        f = open(filename, 'w+', encoding='utf-8')
        f.write(first_line + '\n')


        # 每次循环创建并关闭新文件
        create_tah_by_device_signal(
                f=f,
                mode="1",
                device_no=device_no,
                siteId=siteId,
                roomId=roomId,
                signal_number=signal_number,
                begin_time=begin_time,
                end_time=end_time,
                status_time=status_time,
                val_max=val_max,
                val_min=val_min,
        )

        # # 方式1：指定测点
        # create_tah_by_device_signal(
        #     # filename='',
        #     f=f,
        #     mode="0",
        #     device_no="1",
        #     siteId="2028",
        #     roomId="202806",
        #     deviceid='60366',  # 57934  012325   012321   012318   57933
        #     signalid='013323',
        #     signal_number='0,1,2,3,4,5',
        #     val_max=26, val_min=24,
        #     begin_time=begin_time,
        #     end_time=end_time,
        # )

        f.close()
        # 推进到下一个3天周期
        current_start += interval


        # conn = pymysql.connect(host='10.1.203.38', port=3306, user="root", password="G$SGp!8L3O",
        #                        database="cinterdb_400_jt_gz", charset='utf8mb4', autocommit=True)
        # cursor = conn.cursor()
        # with open(filename, 'r', encoding='utf-8') as f:
        #     sql_content = f.read().strip()
        # # 3. 执行整条 SQL（假设文件中只有一条 INSERT）
        # try:
        #     cursor.execute(sql_content)
        #     print("✅ INSERT 执行成功-信号编码")
        # except Exception as e:
        #     print("❌ 执行失败：", e)
        # cursor.close()
        # conn.close()
        # time.sleep(1)

    stop_time = time.time()

    print(f"✅ 所有时间段文件生成完成！共{stop_time - start_time}秒")