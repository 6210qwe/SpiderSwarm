from typing import Set

from bald_spider.duplicate_filter import BaseFilter
from bald_spider.utils.log import get_logger


class MemoryFilter(BaseFilter):
    def __init__(self, crawler):
        self.fingerprints: Set[str] = set()
        debug: bool = crawler.settings.getbool("FILTER_DEBUG")
        logger = get_logger(f"{self}", crawler.settings.get("LOG_LEVEL"))
        super().__init__(logger, crawler.stats, debug)

    def __str__(self):
        return "MemoryFilter"

    def add(self, fp):
        self.fingerprints.add(fp)

    def __contains__(self, item):
        return item in self.fingerprints
# 使用集合进行过滤，因为不允许重复
# crawler中没必要持有一份过滤器，在哪里实例化，取决于过滤器要在那里用，本质上说，是在调度器上用的
