from company_spider.spiders.baidu import BaiduSpider
from company_spider.spiders.europa import EuropaSpider
from bald_spider.crawler import CrawlerProcess
import asyncio
from bald_spider.utils.project import get_settings


async def run():
    settings = get_settings()
    process = CrawlerProcess(settings)

    spiders = [
        # BaiduSpider,
        EuropaSpider
    ]

    for spider in spiders:
        await process.crawl(spider)

    await process.start()


if __name__ == "__main__":
    asyncio.run(run())
