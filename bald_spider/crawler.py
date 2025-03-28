import asyncio
from typing import Type, Final, Set, Optional
from bald_spider.spider import Spider
from bald_spider.settings.settings_manager import SettingsManager
from bald_spider.exceptions import SpiderTypeError
from bald_spider.core.engine import Engine
from bald_spider.utils.project import merge_settings
import signal
from bald_spider.utils.log import get_logger
from bald_spider.stats_collector import StatsCollector
from bald_spider.utils.date import now
from bald_spider.subscriber import Subscriber
from bald_spider.event import spider_opened
from bald_spider.event import spider_closed
from bald_spider.extension import ExtensionManager
logger = get_logger(__name__)


class Crawler:
    def __init__(self, spider_cls, settings):
        self.spider_cls = spider_cls
        self.spider: Optional[Spider] = None
        self.engine: Optional[Engine] = None
        self.stats: Optional[StatsCollector] = None
        self.settings: SettingsManager = settings.copy()
        self.subscriber: Optional[Subscriber] = None
        self.extension: Optional[ExtensionManager] = None

    async def crawl(self):
        self.subscriber = self._create_subscriber()
        self.spider = self._create_spider()
        self.engine = self._create_engine()
        self.stats = self._create_stats()
        self.extension = self._create_extension()
        await self.engine.start_spider(self.spider)

    def _create_extension(self):
        extension = ExtensionManager.create_instance(self)
        return extension
    @staticmethod
    def _create_subscriber():
        subscriber = Subscriber()
        return subscriber

    def _create_stats(self):
        stats = StatsCollector(self)
        # stats["start_time"] = now()
        return stats

    # 在这个地方还有个好处就是 engine、spider、crawler之间互相关联，三者都互有对方
    def _create_spider(self):
        # 不合理的原因：因为spider_cls是用户自定义的类，所以可以接受参数等，直接使用()的方式生成欠妥
        spider = self.spider_cls.create_instance(self)
        self._set_spider(spider)
        return spider

    def _create_engine(self):
        # 在这个地方我们可以直接将self.settings扔进engine中，我们的第一版启动方式的确是这样
        # 但是这个部分self是Crawl类，其中包含settings,传self更全面
        engine = Engine(self)
        engine.engine_start()
        return engine

    def _set_spider(self, spider):
        self.subscriber.subscribe(spider.spider_opened, event=spider_opened)
        self.subscriber.subscribe(spider.spider_closed, event=spider_closed)
        merge_settings(spider, self.settings)

    async def close(self, reason="finished"):
        await asyncio.create_task(self.subscriber.notify(spider_closed))
        self.stats.close_spider(self.spider, reason)


class CrawlerProcess:
    def __init__(self, settings=None):
        self.crawlers: Final[Set] = set()
        self._active: Final[Set] = set()
        self.settings = settings
        # `ctrl + c`的信号是SIGINT
        signal.signal(signal.SIGINT, self._shutdown)

    # 在这个地方，我们可以实例化多个爬虫，那么在创建的时候使用的是一个配置文件
    # 配置管理器中使用的是可变的Mapping类型，这样会相互干扰，所以需要对配置管理进行深拷贝
    async def crawl(self, spider: Type[Spider]):
        crawler: Crawler = self._create_crawler(spider)
        self.crawlers.add(crawler)
        task = await self._crawl(crawler)
        self._active.add(task)

    @staticmethod
    async def _crawl(crawler):
        return asyncio.create_task(crawler.crawl())

    # 真正的启动函数
    async def start(self):
        await asyncio.gather(*self._active)

    def _create_crawler(self, spider_cls) -> Crawler:
        # 防止传入的是字符串，类型异常抛出
        if isinstance(spider_cls, str):
            raise SpiderTypeError(f"{type(self)}.crawl args:String is not supported")
        crawler = Crawler(spider_cls, self.settings)
        return crawler

    def _shutdown(self, _signum, _frame):
        for crawler in self.crawlers:
            crawler.engine.running = False
            crawler.engine.normal = False
            crawler.stats.close_spider(crawler.spider, "ctrl c")
        logger.warning(f"spider received `ctrl c` single,closed")
