from notion_client import Client
from datetime import datetime, timedelta
import datetime
import os
import logging
import re
from datetime import datetime
TARGET_ICON_URL = "https://www.notion.so/icons/star_gray.svg"
from utils import (
    format_date,
    get_date,
    get_first_and_last_day_of_month,
    get_first_and_last_day_of_week,
    get_first_and_last_day_of_quarter,
    get_first_and_last_day_of_year,
    get_icon,
    get_number,
    get_relation,
    get_rich_text,
    get_title,
    timestamp_to_date,
)


class NotionManager:
    def __init__(self):
        self.__cache = {}
        self.database_name_dict = {
            "DAY_DATABASE_NAME": "Days",
            "WEEK_DATABASE_NAME": "Weeks",
            "MONTH_DATABASE_NAME": "Months",
            "QUARTER_DATABASE_NAME": "Quarters",
            "YEAR_DATABASE_NAME": "Years",
            "TASKS_DATABASE_NAME": "Tasks",
            "FORM_DATABASE_NAME": "Form",
            "DAILY_DATABASE_NAME": "Daily",
        }
        # self.client = Client(auth=os.getenv("NOTION_TOKEN"), log_level=logging.ERROR)
        #
        # # # 从环境变量中获取 URL
        # tasks_notion_url = os.getenv("TASKS_NOTION_PAGE")
        # time_notion_url = os.getenv("DAYS_NOTION_PAGE")
        # self.client = Client(auth=os.getenv("NOTION_TOKEN"), log_level=logging.ERROR)
        self.client = Client(auth="secret_wtQ22gWbsrLhucFqJMdosKPwONVRnTOBgD1MbmUU6p", log_level=logging.ERROR)

        # # 从环境变量中获取 URL
        tasks_notion_url = "https://www.notion.so/ezrilem/Second-Brain-f7990a8b9bd44899ba72b6222e77b427"
        time_notion_url = "https://www.notion.so/ezrilem/Time-Management-9a535ba80e9c458fa31acd8024bea022"
        daily_notion_url = "https://www.notion.so/ezrilem/Daily-Records-677412832a534799aff3f822af613c4b"
        self.__cache = {}
        self.search_database(self.extract_page_id(time_notion_url))
        for key in self.database_name_dict.keys():
            if (os.getenv(key) != None and os.getenv(key) != ""):
                self.database_name_dict[key] = os.getenv(key)
        self.day_database_id = self.database_id_dict.get(self.database_name_dict.get("DAY_DATABASE_NAME"))
        self.week_database_id = self.database_id_dict.get(self.database_name_dict.get("WEEK_DATABASE_NAME"))
        self.month_database_id = self.database_id_dict.get(self.database_name_dict.get("MONTH_DATABASE_NAME"))
        self.quarter_database_id = self.database_id_dict.get(self.database_name_dict.get("QUARTER_DATABASE_NAME"))
        self.year_database_id = self.database_id_dict.get(self.database_name_dict.get("YEAR_DATABASE_NAME"))
        self.search_database(self.extract_page_id(tasks_notion_url))
        for key in self.database_name_dict.keys():
            if (os.getenv(key) != None and os.getenv(key) != ""):
                self.database_name_dict[key] = os.getenv(key)
            self.form_database_id = self.database_id_dict.get(self.database_name_dict.get("FORM_DATABASE_NAME"))
            self.tasks_database_id = self.database_id_dict.get(self.database_name_dict.get("TASKS_DATABASE_NAME"))
        self.search_database(self.extract_page_id(daily_notion_url))
        for key in self.database_name_dict.keys():
            if (os.getenv(key) != None and os.getenv(key) != ""):
                self.database_name_dict[key] = os.getenv(key)
        self.daily_database_id = self.database_id_dict.get(self.database_name_dict.get("DAILY_DATABASE_NAME"))
    database_id_dict = {}
    image_dict = {}

    def extract_page_id(self, notion_url):
        if not isinstance(notion_url, str):
            notion_url = str(notion_url)
        # 正则表达式匹配 32 个字符的 Notion page_id
        match = re.search(r"([a-f0-9]{32}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})", notion_url)
        if match:
            return match.group(0)
        else:
            raise Exception(f"获取NotionID失败，请检查输入的Url是否正确")

    def search_database(self, block_id):
        children = self.client.blocks.children.list(block_id=block_id)["results"]
        # 遍历子块
        for child in children:
            # 检查子块的类型
            if child["type"] == "child_database":
                title = child.get('child_database').get('title')
                # print(f"Processing database: {title}")  # 打印数据库的标题
                self.database_id_dict[title] = child.get("id")
                # print(f"Stored ID: {self.database_id_dict[title]} for database: {title}")  # 打印存储的 ID 和对应的数据库标题
            elif child["type"] == "image":
                if child.get('image') is not None and child.get('image').get('external') is not None:
                    self.image_dict["url"] = child.get('image').get('external').get('url')
                    self.image_dict["id"] = child.get('id')
            # 如果子块有子块，递归调用函数
            if "has_children" in child and child["has_children"]:
                self.search_database(child["id"])
 

