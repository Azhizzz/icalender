import calendar
from datetime import datetime
from datetime import timedelta

def get_date(start,end=None):
    return {
        "date": {
            "start": start,
            "end":end,
            # "time_zone": "Asia/Shanghai",
        }
    }


def format_time(time):
    """将秒格式化为 xx时xx分格式"""
    result = ""
    hour = time // 3600
    if hour > 0:
        result += f"{hour}时"
    minutes = time % 3600 // 60
    if minutes > 0:
        result += f"{minutes}分"
    return result

def format_date(date,format="%Y-%m-%d"):
    return date.strftime(format)


def timestamp_to_date(timestamp):
    """时间戳转化为date"""
    return datetime.utcfromtimestamp(timestamp) + timedelta(hours=8)


def get_first_and_last_day_of_month(date):
    # 获取给定日期所在月的第一天
    first_day = date.replace(day=1)

    # 获取给定日期所在月的最后一天
    _, last_day_of_month = calendar.monthrange(date.year, date.month)
    last_day = date.replace(
        day=last_day_of_month
    )

    return first_day, last_day

def get_first_and_last_day_of_quarter(date):
    # 获取给定日期所在季度的第一天
    first_day = date.replace(
        month=(date.month - 1) // 3 * 3 + 1, day=1
    )

    # 获取给定日期所在季度的最后一天
    _, last_day_of_month = calendar.monthrange(date.year, date.month)
    last_day = date.replace(
        month=(date.month - 1) // 3 * 3 + 3, day=last_day_of_month
    )

    return first_day, last_day


def get_first_and_last_day_of_year(date):
    # 获取给定日期所在年的第一天
    first_day = date.replace(month=1, day=1)

    # 获取给定日期所在年的最后一天
    last_day = date.replace(month=12, day=31)

    return first_day, last_day


def get_first_and_last_day_of_week(date):
    # 获取给定日期所在周的第一天（星期一）
    first_day_of_week = (date - timedelta(days=date.weekday()))

    # 获取给定日期所在周的最后一天（星期日）
    last_day_of_week = first_day_of_week + timedelta(days=6)

    return first_day_of_week, last_day_of_week
