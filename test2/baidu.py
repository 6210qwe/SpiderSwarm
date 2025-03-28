# main.py
from spider import Spider
from loguru import logger


class BaiduSpider(Spider):
    def run(self):
        """运行爬虫"""
        logger.info("爬虫开始运行...")

        # 生成要爬取的URL列表
        urls = [f"https://www.baidu.com" for _ in range(100)]

        # 处理URL
        for url in urls:
            self.process_url(url)

        # 打印统计信息
        self.print_stats()


if __name__ == "__main__":
    # Redis配置
    redis_config = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None  # 如果有密码在这里设置
    }

    # 创建爬虫实例
    spider = BaiduSpider(
        redis_config=redis_config,
        log_file="baidu_spider.log",
        log_level="INFO"
    )

    try:
        # 如果需要清除历史记录
        # spider.clear_history()

        # 运行爬虫
        spider.run()
    except KeyboardInterrupt:
        logger.info("爬虫被手动停止")