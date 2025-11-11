from tender_spider.spiders.nation import NationSpider
from bald_spider.crawler import CrawlerProcess
import asyncio
from bald_spider.utils.project import get_settings


async def run():
    settings = get_settings()
    process = CrawlerProcess(settings)

    spiders = [
        NationSpider,
    ]

    # 批量添加爬虫
    for spider in spiders:
        await process.crawl(spider)

    # 启动所有爬虫
    await process.start()


if __name__ == "__main__":
    asyncio.run(run())