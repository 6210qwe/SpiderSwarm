from bald_spider.duplicate_filter import BaseFilter
from bald_spider.utils.log import get_logger


class NoFilter(BaseFilter):
    def __init__(self, crawler):
        debug: bool = crawler.settings.getbool("FILTER_DEBUG")
        logger = get_logger(f"{self}", crawler.settings.get("LOG_LEVEL"))
        super().__init__(logger, crawler.stats, debug)

    def __str__(self):
        return "NoFilter"

    def add(self, fp):
        pass

    def __contains__(self, item):
        return False  # 始终返回 False，表示从不过滤任何请求

    async def closed(self):
        pass 