#!/usr/bin/env python3
# gen_signalh.py
import pymysql, random, argparse
from datetime import datetime, timedelta
from dateutil import parser, relativedelta
from typing import List, Tuple, Iterable, Optional

# -------------------- 配置 --------------------
DB_CFG = dict(host='xxx', port=3306, user='root', password='xxx', database='xxx', charset='utf8mb4')


# -------------------- 数据库 --------------------
def get_max_id() -> int:
    sql = 'SELECT MAX(Id) FROM d_signalh'
    (max_id,) = _query(sql)[0]
    return max_id if max_id else 0


def fetch_signals(site: str, room: str, signal_number: str) -> List[Tuple]:
    yl_names = ["'1#工况环境'", "'2#工况环境'", "'系统参数'",
                "'1#一次侧机组（冷机/冷塔）'", "'2#一次侧机组（冷机/冷塔）'", "'CDU'"]
    dev_rows = _query(f"""SELECT DeviceID FROM m_device
                          WHERE SiteID='{site}' AND RoomID='{room}'
                                AND DeviceName IN ({','.join(yl_names)})""")
    if not dev_rows: return []
    dev_ids = ','.join(f"'{d[0]}'" for d in dev_rows)
    return _query(f"""SELECT SCID,SiteID,DeviceID,`Type`,SignalID,SignalNumber
                      FROM m_signal
                      WHERE SiteID='{site}' AND RoomID='{room}'
                            AND DeviceID IN ({dev_ids})
                            AND SignalNumber='{signal_number}'
                            AND `Type`!=4""")


def _query(sql: str):
    conn = pymysql.connect(**DB_CFG, autocommit=True)
    cur = conn.cursor()
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return rs


# -------------------- 时间生成 --------------------
FMT = '%Y-%m-%d %H:%M:%S'
BASE_HOURS = (4, 12, 20)


def gen_times(start: str, end: str, status: int, skip: Iterable[int] = ()):
    st, et = parser.parse(start), parser.parse(end)
    skip = set(skip)
    bases = []
    d = st.date()
    while d <= et.date():
        for h in BASE_HOURS:
            if h in skip: continue
            b = datetime.combine(d, datetime.min.time()) + timedelta(hours=h)
            if b < st or b > et: continue
            bases.append(b)
        d += timedelta(days=1)

    def expand(b, delta_list):
        return [b + d for d in delta_list]

    deltas = {
        0: [timedelta(0), timedelta(seconds=-1), timedelta(seconds=1),
            timedelta(minutes=-30), timedelta(minutes=30)],
        1: [timedelta(seconds=-1), timedelta(seconds=1),
            timedelta(minutes=-30), timedelta(minutes=30)],
        2: [timedelta(hours=-1), timedelta(hours=1)],
        3: [timedelta(hours=-1, seconds=-1), timedelta(hours=1, seconds=1)],
        4: []
    }[status]
    times = sorted({t for b in bases for t in expand(b, deltas) if st <= t <= et})
    return [t.strftime(FMT) for t in times]


# -------------------- 数值生成 --------------------
def rand_value(lo: Optional[float] = None, hi: Optional[float] = None) -> float:
    if lo is not None and hi is not None:
        return round(random.uniform(lo, hi), 1)
    return 10.0


# -------------------- 写文件 --------------------
def write_sql(rows: List[Tuple], file: str):
    head = """INSERT INTO d_signalh
(Id, SCID, SiteID, DeviceID, Type, SignalID, SignalNumber, Value, UpdateTime)
VALUES\n"""
    with open(file, 'w', encoding='utf-8') as f:
        f.write(head + ',\n'.join(
            "('%s','%s','%s','%s',%s,'%s','%s','%s','%s')" % r for r in rows) + ';')


# -------------------- 主逻辑 --------------------
def run(site: str, room: str, signal_number: str,
        start: str, end: str, status: int, skip: Iterable[int],
        number: Optional[int] = None,
        value_min: Optional[float] = None,
        value_max: Optional[float] = None,
        out: str = 'd_signalh.sql'):
    signals = fetch_signals(site, room, signal_number)
    if not signals:
        print('❌  未找到测点，请检查 site/room/signal_number')
        return
    times = gen_times(start, end, status, skip)
    if not times:
        print('❌  时间段 & 策略下无时间点')
        return
    max_id = get_max_id()
    rows, cnt = [], max_id + 1
    for scid, site_id, dev_id, typ, sig_id, sig_num in signals:
        for t in times:
            if number and len(rows) >= number: break
            val = rand_value(value_min, value_max)
            rows.append((cnt, scid, site_id, dev_id, int(sig_id[:3]),
                         sig_id, sig_num or '0', val, t))
            cnt += 1
    write_sql(rows, out)
    print(f'✅  已生成 {len(rows)} 条数据 → {out}')


# -------------------- 命令行 --------------------
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='批量生成 d_signalh 历史数据')
    ap.add_argument('--site', required=True, help='站点ID')
    ap.add_argument('--room', required=True, help='机房ID')
    ap.add_argument('--signal_number', default='1', help='信号编号')
    ap.add_argument('--start', required=True, help='开始时间 2025-09-09 04:00:00')
    ap.add_argument('--end', required=True, help='结束时间 2025-09-10 00:00:00')
    ap.add_argument('--status', type=int, default=1, choices=(0, 1, 2, 3, 4),
                    help='时间策略 0-4')
    ap.add_argument('--skip', type=int, nargs='*', default=[], help='跳过的小时 4 20')
    ap.add_argument('--number', type=int, help='最多生成多少条（不限制则全量）')
    ap.add_argument('--value_min', type=float, help='随机值下限')
    ap.add_argument('--value_max', type=float, help='随机值上限')
    ap.add_argument('-o', '--out', default='d_signalh.sql', help='输出文件名')
    args = ap.parse_args()

    run(args.site, args.room, args.signal_number,
        args.start, args.end, args.status, args.skip,
        args.number, args.value_min, args.value_max, args.out)
