from bald_spider import Spider, Request
from loguru import logger

class ExampleSpider(Spider):
    name = "example"
    allowed_domains = ["example.com"]
    
    def start_requests(self):
        urls = []
        for url in urls:
            yield Request(url=url, callback=self.parse)
    
    def parse(self, response):
        # 解析页面
        pass

