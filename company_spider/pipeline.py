#
import random

import aiomysql
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from bald_spider.event import spider_closed
from bald_spider.utils.log import get_logger
from get_mysqldb import DatabasePool
from async_mysql import AsyncMySQLClient
# class TenderPipeline:
#     def __init__(self):
#         self.logger = get_logger(self.__class__.__name__)
#         self.DB_HOST = "rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com"
#         self.DB_PORT = 3306
#         self.DB_DATABASE = "yaojianju"
#         self.DB_USER = "zhangyanzhen"
#         self.DB_PASSWORD = "yutu#2025"
#         self.mysql_db = DatabasePool(
#             logger=logger,
#             DB_HOST=self.DB_HOST,
#             DB_PORT=self.DB_PORT,
#             DB_DATABASE=self.DB_DATABASE,
#             DB_USER=self.DB_USER,
#             DB_PASSWORD=self.DB_PASSWORD
#         )
#
#     def process_item(self, item, spider):
#         item_data = item['item_data']
#         print(item_data)
#         # condition = {"uuid": item_data['uuid']}
#         # query_results = self.mysql_db.query("eudamed_device_copy1", condition=condition, get_results=True)
#         # if not query_results:
#         #     self.mysql_db.insert("eudamed_device_copy1", data_dict=item_data, return_ids=True)
#         # else:
#         #     print("数据已存在")
#
#
#     @classmethod
#     def create_instance(cls, crawler):
#         return cls()

# class MysqlPipeline:
#     def __init__(self, conn, col):
#         self.conn = conn
#         self.logger = get_logger(self.__class__.__name__)
#
#     @classmethod
#     async def create_instance(cls, crawler):
#         conn = AsyncMySQLClient(host="rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com", user="zhangyanzhen", password="yutu#2025", db="yaojianju")
#         await conn.connect()
#         o = cls(conn)
#         crawler.subscriber.subscribe(o.spider_closed, event=spider_closed)
#         return o
#
#     async def spider_closed(self, spider):
#         self.logger.info("Mysql closed")
#         self.conn.close()
#
#     async def process_item(self, item, spider):
#         item_data = item['item_data']
#         print(item_data)
#         self.conn.insert(table="eudamed_device_copy1", data=item_data)
#         return item
#         # print(item_data)
#         # condition = {"uuid": item_data['uuid']}
#         # query_results = self.mysql_db.query("eudamed_device_copy1", condition=condition, get_results=True)
#         # if not query_results:
#         #     self.mysql_db.insert("eudamed_device_copy1", data_dict=item_data, return_ids=True)
#         # else:
#         #     print("数据已存在")

# from AsyncMysqlClient import MySQLClient
# from motor.motor_asyncio import AsyncIOMotorClient
# class MysqlPipeline:
#     def __init__(self, client):
#         self.client = client
#         self.logger = get_logger(self.__class__.__name__)
#
#     @classmethod
#     async def create_instance(cls, crawler):
#         client = await MySQLClient.create_client(
#             host='rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com',
#             port=3306,
#             user='zhangyanzhen',
#             password='yutu#2025',
#             db='yaojianju'
#         )
#         o = cls(client)
#         crawler.subscriber.subscribe(o.spider_closed, event=spider_closed)
#         return o
#
#     async def spider_closed(self):
#         self.logger.info("Mysql closed")
#         self.client.close()
#
#     async def process_item(self, item, spider):
#         item_data = item['item_data']
#         print(item_data)
#         await self.client.insert(table="eudamed_device_copy1", data=test_data, return_id=True)
#         # self.conn.insert(table="eudamed_device_copy1", data=item_data)
#         # return item

# from loguru import logger
# import aiomysql
# from typing import Dict, Any
#
#
# class AsyncMySQLPipeline:
#     def __init__(self):
#         self.pool = None
#         self.table = "eudamed_device_copy1"
#
#     async def open_spider(self, spider):
#         """爬虫启动时创建数据库连接池"""
#         try:
#             self.pool = await aiomysql.create_pool(
#                 host='rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com',
#                 port=3306,
#                 user='zhangyanzhen',
#                 password='yutu#2025',
#                 db='yaojianju',
#                 autocommit=True
#             )
#             logger.info("MySQL连接池创建成功")
#         except Exception as e:
#             logger.error(f"MySQL连接池创建失败: {str(e)}")
#             raise
#
#     @classmethod
#     def create_instance(cls, crawler):
#         # client = await MySQLClient.create_client(
#         #     host='rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com',
#         #     port=3306,
#         #     user='zhangyanzhen',
#         #     password='yutu#2025',
#         #     db='yaojianju'
#         # )
#         # o = cls(client)
#         # crawler.subscriber.subscribe(o.spider_closed, event=spider_closed)
#         # return o
#
#     async def process_item(self, item: Dict[str, Any]):
#         """处理数据项，插入数据库"""
#         if not self.pool:
#             logger.error("MySQL连接池未初始化")
#             return item
#
#         try:
#             # 构建SQL语句
#             fields = ', '.join(item.keys())
#             placeholders = ', '.join(['%s'] * len(item))
#             sql = f"""
#                 INSERT INTO {self.table} ({fields})
#                 VALUES ({placeholders})
#                 ON DUPLICATE KEY UPDATE
#                 {', '.join(f"{k} = VALUES({k})" for k in item.keys())}
#             """
#
#             # 执行SQL
#             async with self.pool.acquire() as conn:
#                 async with conn.cursor() as cur:
#                     await cur.execute(sql, list(item.values()))
#                     logger.debug(f"数据插入成功: {item}")
#
#         except Exception as e:
#             logger.error(f"数据插入失败: {str(e)}")
#
#         return item
#
#     async def close_spider(self, spider):
#         """爬虫关闭时关闭数据库连接池"""
#         if self.pool:
#             self.pool.close()
#             await self.pool.wait_closed()
#             logger.info("MySQL连接池已关闭")


from loguru import logger
from bald_spider.event import spider_closed
from bald_spider.utils.log import get_logger
import aiomysql

# from loguru import logger
# from bald_spider.event import spider_closed
# from bald_spider.utils.log import get_logger
# import aiomysql
# import asyncio
#
#
# class AsyncMySQLPipeline:
#     def __init__(self):
#         self.pool = None
#         self.logger = get_logger(self.__class__.__name__)
#         self._init_event = asyncio.Event()
#
#     @classmethod
#     def create_instance(cls, crawler):
#         """同步创建实例，但延迟初始化连接池"""
#         o = cls()
#         # 订阅爬虫关闭事件
#         crawler.subscriber.subscribe(o.spider_closed, event=spider_closed)
#         # 创建异步初始化任务
#         asyncio.create_task(o._init_pool())
#         return o
#
#     async def _init_pool(self):
#         """异步初始化连接池"""
#         try:
#             self.pool = await aiomysql.create_pool(
#                 host='rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com',
#                 port=3306,
#                 user='zhangyanzhen',
#                 password='yutu#2025',
#                 db='yaojianju',
#                 autocommit=True
#             )
#             self._init_event.set()
#             self.logger.info("MySQL connection pool initialized")
#         except Exception as e:
#             self.logger.error(f"Failed to initialize MySQL pool: {e}")
#             raise
#
#     async def spider_closed(self):
#         """爬虫关闭时关闭数据库连接"""
#         if self.pool:
#             self.logger.info("MySQL connection pool closed")
#             self.pool.close()
#             await self.pool.wait_closed()

    # async def process_item(self, item, spider):
    #     """处理数据项"""
    #     try:
    #         # 等待连接池初始化完成
    #         await self._init_event.wait()
    #         item_data = item['item_data']
    #         async with self.pool.acquire() as conn:
    #             async with conn.cursor() as cur:
    #                 # 检查数据是否已存在
    #                 await cur.execute(
    #                     "SELECT id FROM eudamed_device_copy1 WHERE uuid = %s",
    #                     (item_data['uuid'],)
    #                 )
    #                 result = await cur.fetchone()
    #
    #                 if not result:
    #                     # 插入新数据
    #                     fields = ', '.join(item_data.keys())
    #                     placeholders = ', '.join(['%s'] * len(item_data))
    #                     sql = f"INSERT INTO eudamed_device_copy1 ({fields}) VALUES ({placeholders})"
    #                     await cur.execute(sql, list(item_data.values()))
    #                     self.logger.info(f"Inserted new record: {item_data['uuid']}")
    #                 else:
    #                     self.logger.info(f"Record already exists: {item_data['uuid']}")
    #
    #         return item
    #     except Exception as e:
    #         self.logger.error(f"Error processing item: {e}")
    #         raise

    # def process_item(self, item, spider):
    #     """同步包装异步处理"""
    #
    #     async def _process():
    #         try:
    #             # 等待连接池初始化完成
    #             await self._init_event.wait()
    #
    #             item_data = item['item_data']
    #             async with self.pool.acquire() as conn:
    #                 async with conn.cursor() as cur:
    #                     # 检查数据是否已存在
    #                     await cur.execute(
    #                         "SELECT id FROM eudamed_device_copy1 WHERE uuid = %s",
    #                         (item_data['uuid'],)
    #                     )
    #                     result = await cur.fetchone()
    #
    #                     if not result:
    #                         # 插入新数据
    #                         fields = ', '.join(item_data.keys())
    #                         placeholders = ', '.join(['%s'] * len(item_data))
    #                         sql = f"INSERT INTO eudamed_device_copy1 ({fields}) VALUES ({placeholders})"
    #                         await cur.execute(sql, list(item_data.values()))
    #                         self.logger.info(f"Inserted new record: {item_data['uuid']}")
    #                     else:
    #                         self.logger.info(f"Record already exists: {item_data['uuid']}")
    #
    #             return item
    #         except Exception as e:
    #             self.logger.error(f"Error processing item: {e}")
    #             raise
    #
    #     # 在事件循环中运行异步处理
    #     future = asyncio.run_coroutine_threadsafe(_process(), self._loop)
    #     return future.result()  # 等待异步处理完成