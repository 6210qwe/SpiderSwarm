#
import random

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from bald_spider.event import spider_closed
from bald_spider.exceptions import *
from bald_spider.utils.log import get_logger
from get_mysqldb import DatabasePool

#  此处需要自行配置
DB_HOST = "localhost"
DB_PORT = 3306
DB_DATABASE = "py_spider"
DB_USER = "root"
DB_PASSWORD = "root"


class TestPipeline:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.mysql_db = DatabasePool(logger=logger, DB_HOST=DB_HOST, DB_PORT=DB_PORT, DB_DATABASE=DB_DATABASE,
                                     DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD)

    def process_item(self, item, spider):
        # {'title': '百度一下，你就知道', 'url': 'http://www.baidu.com'}
        print(item)
        item_data = {}
        item_data['url'] = item['url']
        item_data['title'] = item['title']
        self.mysql_db.insert("baidu", data_dict=item_data)


    @classmethod
    def create_instance(cls, crawler):
        return cls()
