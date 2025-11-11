from loguru import logger
from bald_spider.event import spider_closed
from bald_spider.utils.log import get_logger
import aiomysql
import asyncio
from functools import partial

class AsyncMySQLPipeline:
    def __init__(self):
        self.pool = None
        self.logger = get_logger(self.__class__.__name__)
        self._init_event = asyncio.Event()
        self._loop = asyncio.get_event_loop()

    @classmethod
    def create_instance(cls, crawler):
        """同步创建实例，但延迟初始化连接池"""
        o = cls()
        # 订阅爬虫关闭事件
        crawler.subscriber.subscribe(o.spider_closed, event=spider_closed)
        # 创建异步初始化任务
        asyncio.create_task(o._init_pool())
        return o

    async def _init_pool(self):
        """异步初始化连接池"""
        try:
            self.pool = await aiomysql.create_pool(
                host='rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com',
                port=3306,
                user='zhangyanzhen',
                password='yutu#2025',
                db='yaojianju',
                autocommit=True
            )
            self._init_event.set()
            self.logger.info("MySQL connection pool initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize MySQL pool: {e}")
            raise

    async def spider_closed(self, spider):
        """爬虫关闭时关闭数据库连接"""
        if self.pool:
            self.logger.info("MySQL connection pool closed")
            self.pool.close()
            await self.pool.wait_closed()

    def process_item(self, item, spider):
        """同步包装异步处理"""
        async def _process():
            try:
                # 等待连接池初始化完成
                await self._init_event.wait()
                
                item_data = item['item_data']
                async with self.pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        # 检查数据是否已存在
                        await cur.execute(
                            "SELECT id FROM eudamed_device_copy1 WHERE uuid = %s",
                            (item_data['uuid'],)
                        )
                        result = await cur.fetchone()
                        
                        if not result:
                            # 插入新数据
                            fields = ', '.join(item_data.keys())
                            placeholders = ', '.join(['%s'] * len(item_data))
                            sql = f"INSERT INTO eudamed_device_copy1 ({fields}) VALUES ({placeholders})"
                            await cur.execute(sql, list(item_data.values()))
                            self.logger.info(f"Inserted new record: {item_data['uuid']}")
                        else:
                            self.logger.info(f"Record already exists: {item_data['uuid']}")
                
                return item
            except Exception as e:
                self.logger.error(f"Error processing item: {e}")
                raise

        # 在事件循环中运行异步处理
        future = asyncio.run_coroutine_threadsafe(_process(), self._loop)
        return future.result()  # 等待异步处理完成 