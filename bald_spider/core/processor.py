from asyncio import Queue
from typing import Union, Optional
from bald_spider import Item, Request
from bald_spider.pipeline.pipeline_manager import PipelineManager

class Processor:
    def __init__(self, crawler):
        self.queue: Queue = Queue()
        self.crawler = crawler
        self.pipelines: Optional[PipelineManager] = None

    def open(self):
        self.pipelines = PipelineManager.create_instance(self.crawler)

    async def process(self):
        while not self.idle():
            result = await self.queue.get()
            if isinstance(result, Request):
                await self.crawler.engine.enqueue_request(result)
            else:
                assert isinstance(result, Item)
                await self._process_item(result)

    async def _process_item(self, item: Item):
        # 首先当程序走到这里，代表这里都是数据，因为process方法有做断言
        self.crawler.stats.inc_value("item_successful_count")
        # print(item)
        await self.pipelines.process_item(item)

    async def enqueue(self, output: Union[Request, Item]):
        await self.queue.put(output)
        await self.process()

    def idle(self):
        return len(self) == 0

    def __len__(self):
        return self.queue.qsize()
