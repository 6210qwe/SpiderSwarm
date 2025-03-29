from pprint import pformat
from typing import Optional

from bald_spider import Item
from bald_spider.spider import Spider
from bald_spider.utils.log import get_logger


class DebugPipeline:

    def __init__(self, logger):
        self.logger = logger

    @classmethod
    def create_instance(cls, crawler):
        logger = get_logger(cls.__name__, crawler.settings.get("LOG_LEVEL"))
        return cls(logger)

    def process_item(self, item: Item, spider: Spider) -> Optional[Item]:
        # 此处书写有误, 返回值应该就是Item, 而不是Optional[Item], 因为process_item返回None是不支持的
        self.logger.debug(pformat(item.to_dict()))
        return item
