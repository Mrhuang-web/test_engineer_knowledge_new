from datetime import datetime, timedelta

# ========== 2. 工具函数 ==========
def parse_date(date_str):
    """解析日期字符串为 datetime 对象"""
    if not date_str:
        # 默认前一天
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    return datetime.strptime(date_str, "%Y-%m-%d")

def years_between(start: datetime, end: datetime) -> float:
    """计算两个日期之间相差的年数，保留 1 位小数"""
    days = (end - start).days
    return round(days / 365.0, 2)

def classify_service_period(running_years: float, update_cycle_years: float) -> str:
    """
    根据运行年数和更新周期（年），判断服役年限分区段
    """
    if running_years >= update_cycle_years * 1.5:
        return "超期服役>=1.5倍更新周期"
    elif running_years >= update_cycle_years:
        return "超期服役<1.5倍更新周期"
    else:
        ratio = running_years / update_cycle_years
        if ratio < 0.7:
            return "<70%"
        else:
            return ">70%在超期内"

# ========== 3. 主计算 ==========
def calculate_main():
    start_time = parse_date(START_TIME_STR)
    current_time = parse_date(CURRENT_TIME_STR)
    running_years = years_between(start_time, current_time)
    service_period = classify_service_period(running_years, UPDATE_CYCLE_YEARS)

    print("=== 计算结果 ===")
    print(f"当前时间：{current_time.strftime('%Y-%m-%d')}")
    print(f"上线时间：{start_time.strftime('%Y-%m-%d')}")
    print(f"在网运行时长：{running_years} 年")
    print(f"更新周期：{UPDATE_CYCLE_YEARS} 年")
    print(f"服役年限分区段：{service_period}")

if __name__ == "__main__":
    # ========== 1. 脚本内形参 ==========
    # 请按需手动修改以下参数
    START_TIME_STR = "2021-08-25"  # 设备上线时间，格式：YYYY-MM-DD
    UPDATE_CYCLE_YEARS = 6.0  # 更新周期，单位：年
    CURRENT_TIME_STR = ""  # 留空默认取前一天；也可手动填写，如 "2025-09-20"

    calculate_main()