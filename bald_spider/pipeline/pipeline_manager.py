from pprint import pformat
from typing import List

from bald_spider.execptions import PipelineInitError
from bald_spider.utils.log import get_logger
from bald_spider.utils.project import load_class


# from bald_spider.utils.project import common_call

class PipelineManager:
    def __init__(self, crawler):
        self.crawler = crawler
        self.pipelines: List = []
        self.methods: List = []

        self.logger = get_logger(self.__class__.__name__, crawler.settings.get("LOG_LEVEL"))
        pipelines = crawler.settings.get("PIPELINES")
        self._add_pipelines(pipelines)
        self._add_methods()

    @classmethod
    def create_instance(cls, *args, **kwargs):
        o = cls(*args, **kwargs)
        return o

    def _add_pipelines(self, pipelines):
        for pipeline in pipelines:
            pipeline_cls = load_class(pipeline)
            if not hasattr(pipeline_cls, "create_instance"):
                raise PipelineInitError(
                    f"pipeline init failed, must inherit from `BasePipeline` or have `create_instance` method")

            self.pipelines.append(pipeline_cls.create_instance(self.crawler))
        if pipelines:
            self.logger.info(f"enabled pipelines: \n {pformat(pipelines)}")

    def _add_methods(self):
        for pipeline in self.pipelines:
            if hasattr(pipeline, "process_item"):
                self.methods.append(pipeline.process_item)

    async def process_item(self, item):
        # 中间件是归好类，排好队，挨个调用
        # 在这里只需要排队调用就行，通过_add_methods已经排好队了
        for method in self.methods:
            method(item, self.crawler.spider)
            # 我们要用common_call来调，因为要做异步兼容
            # await common_call(method, item, self.crawler.spider)
        # for method in self.methods:
        #     item = method(item)
        # return item
