from datetime import datetime

# 设置日历文件的基本信息
cal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Name//Your Calendar Name//EN
"""

# 创建一个日历事件
event = """
BEGIN:VEVENT
UID:{}@example.com
DTSTAMP:{}Z
DTSTART:{}Z
DTEND:{}Z
SUMMARY:Your Event Name
DESCRIPTION:Description of your event
LOCATION:Location of your event
END:VEVENT
""".format(
    "uid1",  # 唯一标识符
    datetime.now().strftime("%Y%m%dT%H%M%SZ"),  # 当前时间的时间戳
    datetime(2024, 3, 1, 9, 0, 0).strftime("%Y%m%dT%H%M%SZ"),  # 事件开始时间
    datetime(2024, 3, 1, 10, 0, 0).strftime("%Y%m%dT%H%M%SZ")  # 事件结束时间
)

# 结束日历文件
cal += event  # 将事件添加到日历文件
cal += "END:VCALENDAR"

# 将内容写入文件
with open("your_calendar.ics", "w") as f:
    f.write(cal)

print("Calendar file created.")
