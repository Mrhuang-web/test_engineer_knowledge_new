import time
from random import random
import random
import pymysql
from typing import List, Iterable, Optional

from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

FMT = "%Y-%m-%d %H:%M:%S"


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

    if status == 8:
        return []

    # 1. 生成每天 3 个基准整点
    base_times: List[datetime] = []
    cur_date = start.date()
    end_date = end.date()
    while cur_date <= end_date:
        for hh in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24):
            # for hh in (4, 12, 20):
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
        elif status == 5:
            candidates.extend([
                base + relativedelta(seconds=-3)
            ])
        elif status == 6:
            candidates.extend([
                base + relativedelta(seconds=0)
            ])
        elif status == 7:
            candidates.extend([
                base + relativedelta(hours=23),  # 当天23:00
                base + relativedelta(days=1),  # 次日00:00 (跨天)
                base + relativedelta(days=1, hours=1)  # 次日01:00
            ])
    # 3. 去重 + 排序 + 转字符串
    filtered = sorted({t for t in candidates if start <= t <= end})
    return [t.strftime(FMT) for t in filtered]


start_str = "2025-12-15 00:00:00"
end_str = "2025-12-19 23:59:59"
status_time = 7
# skip_hours = [12]
time_list = generate_times_by_status(start_str, end_str, status_time)
print(time_list)
