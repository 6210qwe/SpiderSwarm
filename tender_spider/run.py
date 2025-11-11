from tender_spider.spiders.nation import NationSpider
from tender_spider.spiders.baidu import BaiduSpider
from bald_spider.crawler import CrawlerProcess
import asyncio
import time
from bald_spider.utils.project import get_settings


# 虽然没有调用，但是导入就是执行，只有在AioDownloader挂代理失败的时候在导入
# from bald_spider.utils import system as _

async def run():
    settings = get_settings()
    process = CrawlerProcess(settings)
    # await process.crawl(BaiduSpider)
    await process.crawl(NationSpider)
    await process.start()
asyncio.run(run())
