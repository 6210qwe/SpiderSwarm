from bald_spider.event import spider_opened


class DefaultHeader:
    def __init__(self, user_agent, headers, spider):
        self.user_agent = user_agent
        self.headers = headers
        self.spider = spider

    @classmethod
    def create_instance(cls, crawler):
        o = cls(
            user_agent=crawler.settings.get("USER_AGENT"),
            headers=crawler.settings.getdict("DEFAULT_HEADERS"),
            spider=crawler.spider
        )
        crawler.subscriber.subscribe(o.spider_opened, event=spider_opened)
        return o

    async def spider_opened(self):
        # 爬虫启动的时候会以支线任务调用spider_opened
        self.headers = getattr(self.spider, "headers", self.headers)
        self.user_agent = getattr(self.spider, "user_agent", self.user_agent)
        if self.user_agent:
            self.headers.setdefault('User-Agent', self.user_agent)

    def process_request(self, request, _spider):
        pass
        # if self.headers:
        #     for k, v in self.headers.items():
        #         request.headers.setdefault(k, v)
















