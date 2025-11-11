from loguru import logger
from bald_spider.event import spider_closed
from bald_spider.exceptions import *
from bald_spider.utils.log import get_logger
from get_mysqldb import DatabasePool




class TenderPipeline:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.DB_HOST = "rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com"
        self.DB_PORT = 3306
        self.DB_DATABASE = "yaojianju"
        self.DB_USER = "zhangyanzhen"
        self.DB_PASSWORD = "yutu#2025"
        self.mysql_db = DatabasePool(
            logger=logger,
            DB_HOST=self.DB_HOST,
            DB_PORT=self.DB_PORT,
            DB_DATABASE=self.DB_DATABASE,
            DB_USER=self.DB_USER,
            DB_PASSWORD=self.DB_PASSWORD
        )

    def process_item(self, item, spider):
        condition = {"uuid": item['uuid']}
        query_results = self.mysql_db.query("eudamed_device_copy1", condition=condition, get_results=True)
        if not query_results:
            self.mysql_db.insert("eudamed_device_copy1", data_dict=item, return_ids=True)
        else:
            print("数据已存在")

    @classmethod
    def create_instance(cls, crawler):
        return cls()
