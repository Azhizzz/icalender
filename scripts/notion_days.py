from notion_client import Client
from ics import Calendar, Event
from datetime import datetime
import os
class NotionCalendar:

    def __init__(self):
        self.client = Client(auth="secret_wtQ22gWbsrLhucFqJMdosKPwONVRnTOBgD1MbmUU6p")
        self.tasks_database_id = "e853106c709a470da4d7ffb8e6d3ad1a"
        self.daily_database_id = "249a9ae39eb5456da9bedf4ca74b491e"
        self.gtd_database_id = "b8802ab7a10347fc80386c782bd422e6"

    def get_calendar(self):
        color_mapping = {
            "Tasks": "purple",
            "Gtd": "skyblue",
            "Social": "orange",
            "Sleep": "lightgreen",
            "Wash": "lightgreen",
            "Eating": "lightgreen",
            "Swipe Phone": "darkgreen",
            "Read": "darkgreen"
        }
        if os.path.exists('notion.ics'):
            with open('notion.ics', 'r') as f:
                ics_content = f.read()

        # 创建Calendar对象
        cal = Calendar()
        database_ids = [
            self.daily_database_id,
            self.gtd_database_id,
            self.tasks_database_id
        ]
        # for database_id in [self.daily_database_id, self.gtd_database_id, self.tasks_database_id]:
        # 查询数据库并处理事件
        # 查询所有数据库并处理事件
        for database_id in database_ids:
            results = self.client.databases.query(database_id=database_id)
            for page in results["results"]:
                print(page)
                page_data = self.client.pages.retrieve(page_id=page["id"])
                e = Event()
                e.name = page["properties"]["Name"]["title"][0]["text"]["content"]
                # 获取Description属性
                description = page.get("properties", {}).get("Description", {})
                if "rich_text" in description and description["rich_text"]:
                    # 如果rich_text存在且非空，获取第一个元素的plain_text
                    e.description = description["rich_text"][0].get("plain_text", "")
                else:
                    # 如果rich_text不存在或为空，设置描述为空字符串
                    e.description = ""
                e.color = color_mapping.get(
                    page["properties"].get("Type", {}).get("name") if "Type" in page["properties"] else "")

                # # 获取StartTime属性
                # start_time_property = page.get("properties", {}).get("StartTime", {})
                # # 获取EndTime属性
                # end_time_property = page.get("properties", {}).get("EndTime", {})
                #
                # # 设置开始时间
                # if "date" in start_time_property and "start" in start_time_property["date"]:
                #     start_time = start_time_property["date"]["start"]
                #     if start_time:  # 确保start_time不是None
                #         e.begin = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f%z")
                #     else:
                #         e.begin = None
                #
                # # 设置结束时间
                # if "date" in end_time_property:
                #     if "end" in end_time_property["date"]:
                #         end_time = end_time_property["date"]["end"]
                #         if end_time:  # 确保end_time不是None
                #             e.end = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f%z")
                #         else:
                #             e.end = None  # 如果end_time是None，设置e.end为None
                #     elif "start" in end_time_property:
                #         # 如果只有开始时间，使用开始时间作为结束时间
                #         e.end = e.begin
                #     else:
                #         e.end = None  # 如果没有结束时间，设置e.end为None
                #
                # # 如果开始时间和结束时间都为空，跳过添加此事件
                # if e.begin is None and e.end is None:
                #     continue
                # 获取StartTime属性
                start_time_property = page.get("properties", {}).get("StartTime", {})
                # 获取EndTime属性
                end_time_property = page.get("properties", {}).get("EndTime", {})

                # 设置开始时间
                if "date" in start_time_property and start_time_property["date"]:
                    start_time = start_time_property["date"].get("start")
                    if start_time:  # 确保start_time不是None
                        e.begin = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f%z")
                    else:
                        e.begin = None

                # 设置结束时间
                if "date" in end_time_property and end_time_property["date"]:
                    end_time = end_time_property["date"].get("end")
                    if end_time:  # 确保end_time不是None
                        e.end = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f%z")
                    else:
                        e.end = None  # 如果end_time是None，设置e.end为None
                elif "start" in end_time_property and end_time_property["date"]:
                    # 如果EndTime的date属性中只有start，使用StartTime的值
                    e.end = e.begin

                # 如果开始时间和结束时间都为空，跳过添加此事件
                if e.begin is None and e.end is None:
                    continue

                # Add the event to the calendar
                for existing_event in cal.events:
                    if existing_event.uid == e.uid:
                        # 更新现有事件
                        existing_event.name = e.name
                        existing_event.begin = e.begin
                        existing_event.end = e.end
                        existing_event.description = e.description
                        # ... 更新其他属性 ...
                        break
                else:
                    # 添加新事件
                    cal.events.add(e)

        # Write the calendar to the notion.ics file
        with open('notion.ics', 'w') as f:
            f.writelines(cal)

        return cal