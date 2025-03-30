from bald_spider.utils.log import get_logger
from random import uniform
from asyncio import sleep
from bald_spider.exceptions import NotConfigured


class DownloadDelay:
    def __init__(self, setting, log_level):
        self.delay = setting.getfloat("DOWNLOAD_DELAY")
        if not self.delay:
            raise NotConfigured("DOWNLOAD_DELAY")
        self.randomness = setting.getbool("RANDOMNESS")
        self.floor, self.upper = setting.getlist("RANDOM_RANGE")
        self.logger = get_logger(self.__class__.__name__, log_level)

    @classmethod
    def create_instance(cls, crawler):
        o = cls(
            setting=crawler.settings,
            log_level=crawler.settings.get("LOG_LEVEL")
        )
        return o

    async def process_request(self, _request, _spider):
        if self.randomness:
            # await sleep(uniform(self.delay * self.floor, self.delay * self.upper))
            await sleep(0.01)
        else:
            # await sleep(self.delay)
            await sleep(0.01)







