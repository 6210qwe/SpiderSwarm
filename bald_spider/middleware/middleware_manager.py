from typing import List, Dict, Callable
from types import MethodType

from bald_spider import Request, Response
from bald_spider.utils.log import get_logger
from bald_spider.utils.project import load_class
from bald_spider.execptions import MiddlewareInitError, InvalidOutput
from pprint import pformat
from collections import defaultdict
from bald_spider.middleware import BaseMiddleware
from bald_spider.utils.spider import common_call

class MiddlewareManager:
    def __init__(self, crawler):
        self.crawler = crawler
        self.logger = get_logger(self.__class__.__name__, crawler.settings.get("LOG_LEVEL"))
        self.middlewares: List = []
        self.methods: Dict[str:List[MethodType]] = defaultdict(list)
        middlewares = self.crawler.settings.getlist("MIDDLEWARES")
        self._add_middleware(middlewares)
        self._add_method()
        self.download_method: Callable = crawler.engine.downloader.download

    async def _process_request(self, request):
        for method in self.methods["process_request"]:
            # result = method(request, self.crawler.spider)
            result = await common_call(method,request, self.crawler.spider)  # 兼容异步
            if result is None:
                continue
            if isinstance(request, (Request, Response)):
                return result
            raise InvalidOutput(f"{method.__qualname__} must return None, Request or Response, got {type(result).__name__}")

    def _process_response(self):
        pass

    def _process_exception(self):
        pass

    async def download(self, request):
        """called in the downloader"""
        await self._process_request(request)
        response = await self.download_method(request)
        return response

    def _add_method(self):
        for middleware in self.middlewares:
            if hasattr(middleware, "process_request"):
                if self._validate_method("process_request", middleware):
                    self.methods["process_request"].append(middleware.process_request)
            if hasattr(middleware, "process_response"):
                if self._validate_method("process_response", middleware):
                    self.methods["process_response"].append(middleware.process_response)
            if hasattr(middleware, "process_execption"):
                if self._validate_method("process_execption", middleware):
                    self.methods["process_execption"].append(middleware.process_execption)

    def _add_middleware(self, middlewares):
        enable_middlewares = [m for m in middlewares if self._validate_middleware(m)]
        if enable_middlewares:
            self.logger.info(f"enable middlewares:\n {pformat(enable_middlewares)}")

    def _validate_middleware(self, middleware):
        middleware_cls = load_class(middleware)
        if not hasattr(middleware_cls, "create_instance"):
            raise MiddlewareInitError(
                f"Middleware Init failed,must inherit from `BaseMiddleware` or must have `create_instance` method")
        instance = middleware_cls.create_instance(self.crawler)
        self.middlewares.append(instance)
        return True

    @classmethod
    def create_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @staticmethod
    def _validate_method(method_name, middleware):
        method = getattr(type(middleware), method_name)
        base_method = getattr(BaseMiddleware, method_name)
        if method == base_method:
            return False
        else:
            return True
