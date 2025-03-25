from bald_spider.spider import Spider
from bald_spider import Request
from items import BaiduItem  # type:ignore
from bald_spider.event import spider_error

class NationSpider(Spider):
    # start_url ="https://www.baidu.com"
    # start_urls = ["http://www.baidu.com", "http://www.baidu.com"]

    custom_settings = {"CONCURRENCY": 20}

    @classmethod
    def create_instance(cls,crawler):
        o = cls()
        o.crawler = crawler
        crawler.subscriber.subscribe(o.spider_error, event=spider_error)
        return o


    def parse(self, response):
        """
        其实在这个部分，我们无法预测到用户会怎样书写代码(同步、异步) 我们都需要进行兼容
        若使用异步的方式，得到的其实就是异步生成器
        """
        # print("parse",response)
        for i in range(10):
            url = "http://www.baidu.com"
            request = Request(url=url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        # print("parse_page",response)
        for i in range(10):
            url = "http://www.baidu.com"
            meta = {"test": "waws"}
            request = Request(url=url, callback=self.parse_detail, meta=meta)
            yield request

    def parse_detail(self, response):
        # print("parse_detail",response)
        # print(response.text)
        item = BaiduItem()
        item["url"] = response.url
        item["title"] = response.xpath("//title/text()").get()
        # item.title = "111"
        yield item

    async def spider_error(self, exc, spider):
        print(f"爬虫出错了{exc}, 请紧急处理一下.")

    async def spider_opened(self):
        print("我想在脚本开启的时候做一些事情，这就是我想做的事情")

    async def spider_closed(self):
        print("我想在脚本关闭的时候做一些事情，这就是我想做的事情")
