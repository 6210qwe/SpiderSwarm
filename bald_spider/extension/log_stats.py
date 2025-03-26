from bald_spider import event

class LogStats:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def create_instance(cls, crawler):
        o = cls(crawler.stats)
        crawler.subscriber.subscribe(o.response_received, event=event.response_received)
        crawler.subscriber.subscribe(o.request_scheduled, event=event.request_scheduled)
        return o

    async def request_scheduled(self, request):
        # 将请求的数量 +1
        self.stats.inc_value("request_Scheduled_count")

    async def response_received(self, response):
        # 将响应的数量 +1
        self.stats.inc_value("response_received_count")



















































