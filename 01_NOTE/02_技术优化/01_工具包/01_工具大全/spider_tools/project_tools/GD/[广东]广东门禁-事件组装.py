import struct
from datetime import datetime

# 定义记录状态含义映射表
STATUS_MAP = {
    # 允许通过
    0x00: {"reader": 1, "operation": "允许通过", "reason": "1号读卡器刷卡开门"},
    0x01: {"reader": 2, "operation": "允许通过", "reason": "2号读卡器刷卡开门"},
    0x02: {"reader": 3, "operation": "允许通过", "reason": "3号读卡器刷卡开门"},
    0x03: {"reader": 4, "operation": "允许通过", "reason": "4号读卡器刷卡开门"},

    # 禁止通过 - 原因不明
    0x80: {"reader": 1, "operation": "禁止通过", "reason": "原因不明"},
    0x81: {"reader": 2, "operation": "禁止通过", "reason": "原因不明"},
    0x82: {"reader": 3, "operation": "禁止通过", "reason": "原因不明"},
    0x83: {"reader": 4, "operation": "禁止通过", "reason": "原因不明"},

    # 禁止通过 - 没有权限
    0x90: {"reader": 1, "operation": "禁止通过", "reason": "没有权限"},
    0x91: {"reader": 2, "operation": "禁止通过", "reason": "没有权限"},
    0x92: {"reader": 3, "operation": "禁止通过", "reason": "没有权限"},
    0x93: {"reader": 4, "operation": "禁止通过", "reason": "没有权限"},

    # 禁止通过 - 密码不对
    0xA0: {"reader": 1, "operation": "禁止通过", "reason": "密码不对"},
    0xA1: {"reader": 2, "operation": "禁止通过", "reason": "密码不对"},
    0xA2: {"reader": 3, "operation": "禁止通过", "reason": "密码不对"},
    0xA3: {"reader": 4, "operation": "禁止通过", "reason": "密码不对"},

    # 禁止通过 - 系统故障
    0xB0: {"reader": 1, "operation": "禁止通过", "reason": "系统有故障"},
    0xB1: {"reader": 2, "operation": "禁止通过", "reason": "系统有故障"},
    0xB2: {"reader": 3, "operation": "禁止通过", "reason": "系统有故障"},
    0xB3: {"reader": 4, "operation": "禁止通过", "reason": "系统有故障"},

    # 禁止通过 - 反潜回/多卡/互锁等
    0xC0: {"reader": 1, "operation": "禁止通过", "reason": "反潜回, 多卡开门或多门互锁"},
    0xC1: {"reader": 2, "operation": "禁止通过", "reason": "反潜回, 多卡开门或多门互锁"},
    0xC2: {"reader": 3, "operation": "禁止通过", "reason": "反潜回, 多卡开门或多门互锁"},
    0xC3: {"reader": 4, "operation": "禁止通过", "reason": "反潜回, 多卡开门或多门互锁"},
    0xC4: {"reader": 1, "operation": "禁止通过", "reason": "反潜回"},
    0xC5: {"reader": 2, "operation": "禁止通过", "reason": "反潜回"},
    0xC6: {"reader": 3, "operation": "禁止通过", "reason": "反潜回"},
    0xC7: {"reader": 4, "operation": "禁止通过", "reason": "反潜回"},
    0xC8: {"reader": 1, "operation": "禁止通过", "reason": "多卡"},
    0xC9: {"reader": 2, "operation": "禁止通过", "reason": "多卡"},
    0xCA: {"reader": 3, "operation": "禁止通过", "reason": "多卡"},
    0xCB: {"reader": 4, "operation": "禁止通过", "reason": "多卡"},
    0xCC: {"reader": 1, "operation": "禁止通过", "reason": "首卡"},
    0xCD: {"reader": 2, "operation": "禁止通过", "reason": "首卡"},
    0xCE: {"reader": 3, "operation": "禁止通过", "reason": "首卡"},
    0xCF: {"reader": 4, "operation": "禁止通过", "reason": "首卡"},

    # 禁止通过 - 门为常闭
    0xD0: {"reader": 1, "operation": "禁止通过", "reason": "门为常闭"},
    0xD1: {"reader": 2, "operation": "禁止通过", "reason": "门为常闭"},
    0xD2: {"reader": 3, "operation": "禁止通过", "reason": "门为常闭"},
    0xD3: {"reader": 4, "operation": "禁止通过", "reason": "门为常闭"},

    # 禁止通过 - 互锁
    0xD4: {"reader": 1, "operation": "禁止通过", "reason": "互锁"},
    0xD5: {"reader": 2, "operation": "禁止通过", "reason": "互锁"},
    0xD6: {"reader": 3, "operation": "禁止通过", "reason": "互锁"},
    0xD7: {"reader": 4, "operation": "禁止通过", "reason": "互锁"},

    # 禁止通过 - 卡过期或不在有效时段
    0xE0: {"reader": 1, "operation": "禁止通过", "reason": "卡过期或不在有效时段"},
    0xE1: {"reader": 2, "operation": "禁止通过", "reason": "卡过期或不在有效时段"},
    0xE2: {"reader": 3, "operation": "禁止通过", "reason": "卡过期或不在有效时段"},
    0xE3: {"reader": 4, "operation": "禁止通过", "reason": "卡过期或不在有效时段"},
}

# 定义特殊操作（完整卡号<100）的映射表
SPECIAL_OP_MAP = {
    (0, 0x00): {"door": 1, "operation": "按钮", "reason": "1号门按钮动作"},
    (1, 0x00): {"door": 2, "operation": "按钮", "reason": "2号门按钮动作"},
    (2, 0x00): {"door": 3, "operation": "按钮", "reason": "3号门按钮动作"},
    (3, 0x00): {"door": 4, "operation": "按钮", "reason": "4号门按钮动作"},
    (0, 0x03): {"door": 1, "operation": "远程开门", "reason": "1号门远程开门动作"},
    (1, 0x03): {"door": 2, "operation": "远程开门", "reason": "2号门远程开门动作"},
    (2, 0x03): {"door": 3, "operation": "远程开门", "reason": "3号门远程开门动作"},
    (3, 0x03): {"door": 4, "operation": "远程开门", "reason": "4号门远程开门动作"},
    (5, 0x00): {"reader": 1, "operation": "超级密码开门", "reason": "1号读卡器超级密码开门"},
    (5, 0x01): {"reader": 2, "operation": "超级密码开门", "reason": "2号读卡器超级密码开门"},
    (5, 0x02): {"reader": 3, "operation": "超级密码开门", "reason": "3号读卡器超级密码开门"},
    (5, 0x03): {"reader": 4, "operation": "超级密码开门", "reason": "4号读卡器超级密码开门"},
    (8, 0x00): {"door": 1, "operation": "门打开", "reason": "1号门打开[门磁信号]"},
    (9, 0x00): {"door": 2, "operation": "门打开", "reason": "2号门打开[门磁信号]"},
    (10, 0x00): {"door": 3, "operation": "门打开", "reason": "3号门打开[门磁信号]"},
    (11, 0x00): {"door": 4, "operation": "门打开[门磁信号]", "reason": "4号门打开[门磁信号]"},
    (12, 0x00): {"door": 1, "operation": "门关闭", "reason": "1号门关闭[门磁信号]"},
    (13, 0x00): {"door": 2, "operation": "门关闭", "reason": "2号门关闭[门磁信号]"},
    (14, 0x00): {"door": 3, "operation": "门关闭", "reason": "3号门关闭[门磁信号]"},
    (15, 0x00): {"door": 4, "operation": "门关闭", "reason": "4号门关闭[门磁信号]"},
    (0, 0x81): {"reader": 1, "operation": "胁迫报警", "reason": "1号读卡器胁迫报警"},
    (1, 0x81): {"reader": 2, "operation": "胁迫报警", "reason": "2号读卡器胁迫报警"},
    (2, 0x81): {"reader": 3, "operation": "胁迫报警", "reason": "3号读卡器胁迫报警"},
    (3, 0x81): {"reader": 4, "operation": "胁迫报警", "reason": "4号读卡器胁迫报警"},
    (0, 0x82): {"door": 1, "operation": "门长时间未关报警", "reason": "1号门长时间未关报警"},
    (1, 0x82): {"door": 2, "operation": "门长时间未关报警", "reason": "2号门长时间未关报警"},
    (2, 0x82): {"door": 3, "operation": "门长时间未关报警", "reason": "3号门长时间未关报警"},
    (3, 0x82): {"door": 4, "operation": "门长时间未关报警", "reason": "4号门长时间未关报警"},
    (0, 0x84): {"door": 1, "operation": "非法闯入报警", "reason": "1号门非法闯入报警"},
    (1, 0x84): {"door": 2, "operation": "非法闯入报警", "reason": "2号门非法闯入报警"},
    (2, 0x84): {"door": 3, "operation": "非法闯入报警", "reason": "3号门非法闯入报警"},
    (3, 0x84): {"door": 4, "operation": "非法闯入报警", "reason": "4号门非法闯入报警"},
    (4, 0xA0): {"operation": "火警", "reason": "火警动作[针对整个控制器]"},
    (6, 0xA0): {"operation": "强制", "reason": "强制锁门[针对整个控制器]"},
}


def parse_short_time(time_bytes):
    """
    解析短时间格式的字节为datetime对象
    假设短时间格式：高字节为年月日（编码规则：年(7位)+月(4位)+日(5位)），低字节为时分秒（编码规则：时(5位)+分(6位)+秒(5位)）
    这里使用通用的门禁短时间编码规则，你可根据实际设备调整
    """
    # 解析年月日（2字节）
    year_month_day = (time_bytes[0] << 8) | time_bytes[1]
    year = ((year_month_day >> 9) & 0x7F) + 2000  # 7位年，假设是2000年后
    month = (year_month_day >> 5) & 0x0F  # 4位月
    day = year_month_day & 0x1F  # 5位日

    # 解析时分秒（2字节）
    hour_min_sec = (time_bytes[2] << 8) | time_bytes[3]
    hour = (hour_min_sec >> 11) & 0x1F  # 5位时
    minute = (hour_min_sec >> 5) & 0x3F  # 6位分
    second = hour_min_sec & 0x1F  # 5位秒

    try:
        return datetime(year, month, day, hour, minute, second)
    except ValueError:
        return None


def assemble_access_event(raw_data):
    """
    组装门禁事件：将8字节原始数据解析为结构化的事件信息
    :param raw_data: 8字节的原始数据（bytes类型，长度必须为8）
    :return: 结构化的事件字典
    """
    if len(raw_data) != 8:
        raise ValueError("原始数据必须为8字节")

    # 1. 按协议拆分各字段
    id_bytes = raw_data[0:2]  # ID号（2字节）
    area_no = raw_data[2]  # 区号（1字节）
    record_status = raw_data[3]  # 记录状态（1字节）
    date_bytes = raw_data[4:6]  # 刷卡年月日（2字节）
    time_bytes = raw_data[6:8]  # 刷卡时分秒（2字节）

    # 2. 转换数值
    id_num = (id_bytes[0] << 8) | id_bytes[1]  # 2字节ID号转整数
    full_card_no = (area_no << 16) | id_num  # 完整卡号 = 区号 + ID号
    card_time = parse_short_time(date_bytes + time_bytes)  # 解析刷卡时间

    # 3. 组装事件基础信息
    event = {
        "原始数据": raw_data.hex(),
        "ID号": id_num,
        "区号": area_no,
        "完整卡号": full_card_no,
        "记录状态(16进制)": hex(record_status),
        "刷卡时间": card_time.strftime("%Y-%m-%d %H:%M:%S") if card_time else "解析失败",
        "操作类型": "",
        "读卡器/门号": "",
        "事件原因": ""
    }

    # 4. 区分正常刷卡和特殊操作
    if full_card_no > 100:
        # 正常刷卡操作（允许/禁止通过）
        status_info = STATUS_MAP.get(record_status, {"reader": "未知", "operation": "未知", "reason": "未知状态码"})
        event["操作类型"] = status_info["operation"]
        event["读卡器/门号"] = f"读卡器{status_info['reader']}" if "reader" in status_info else "未知"
        event["事件原因"] = status_info["reason"]
    else:
        # 特殊操作（完整卡号<100）
        special_key = (full_card_no, record_status)
        special_info = SPECIAL_OP_MAP.get(special_key, {"operation": "未知", "reason": "未知特殊操作"})
        event["操作类型"] = special_info["operation"]
        if "door" in special_info:
            event["读卡器/门号"] = f"门{special_info['door']}"
        elif "reader" in special_info:
            event["读卡器/门号"] = f"读卡器{special_info['reader']}"
        else:
            event["读卡器/门号"] = "全局"
        event["事件原因"] = special_info["reason"]

    return event


# ------------------- 测试示例 -------------------
if __name__ == "__main__":
    # 测试1：正常刷卡 - 1号读卡器允许通过（完整卡号>100）
    # 构造原始数据：ID号(0x09969的低2字节)=0x9969, 区号=0xFE(254), 状态=0x00, 时间=2025-12-20 14:30:20
    test_data1 = bytes([0x99, 0x69, 0xFE, 0x00, 0x70, 0xE4, 0x5B, 0x28])
    event1 = assemble_access_event(test_data1)
    print("测试1 - 正常刷卡事件：")
    for key, value in event1.items():
        print(f"  {key}: {value}")

    print("-" * 50)

    # 测试2：特殊操作 - 1号门按钮动作（完整卡号=0）
    # 构造原始数据：ID号=0x0000, 区号=0x00, 状态=0x00, 时间=2025-12-20 15:00:00
    test_data2 = bytes([0x00, 0x00, 0x00, 0x00, 0x70, 0xE4, 0x60, 0x00])
    event2 = assemble_access_event(test_data2)
    print("测试2 - 特殊操作事件：")
    for key, value in event2.items():
        print(f"  {key}: {value}")

    print("-" * 50)

    # 测试3：禁止通过 - 2号读卡器没有权限
    # 构造原始数据：ID号=0x1234, 区号=0x01, 状态=0x91, 时间=2025-12-20 16:20:10
    test_data3 = bytes([0x12, 0x34, 0x01, 0x91, 0x70, 0xE4, 0x68, 0x28])
    event3 = assemble_access_event(test_data3)
    print("测试3 - 禁止通过事件：")
    for key, value in event3.items():
        print(f"  {key}: {value}")