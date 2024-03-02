from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed
from scripts.notion_days import NotionCalendar

# 基于给定的策略设置重试装饰器
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_calendar_with_retry(calendar):
    return calendar.get_calendar()

def main():
    # 创建 NotionCalendar 实例
    calendar = NotionCalendar()

    # 调用带有重试装饰器的 get_calendar_with_retry 方法
    cal = get_calendar_with_retry(calendar)

    # 打印日历事件
    for event in cal.events:
        print(f'Event: {event.name}, Start: {event.begin}, End: {event.end}')

# 如果这个脚本是直接运行的，而不是被导入的，那么运行 main 函数
if __name__ == "__main__":
    main()
