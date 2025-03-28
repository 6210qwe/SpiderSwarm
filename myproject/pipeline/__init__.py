from bald_spider import Pipeline
from loguru import logger

class BasePipeline(Pipeline):
    def process_item(self, item):
        logger.info(f"处理数据: {item}")
        return item

    def open_spider(self, spider):
        logger.info(f"爬虫 {spider.name} 启动")

    def close_spider(self, spider):
        logger.info(f"爬虫 {spider.name} 关闭")
