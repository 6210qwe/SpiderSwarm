from asyncio import create_task
from typing import List, Dict, Callable, Optional
from types import MethodType

from scrapy.signals import response_received

from bald_spider import Request, Response
from bald_spider.utils.log import get_logger
from bald_spider.utils.project import load_class
from bald_spider.exceptions import MiddlewareInitError, InvalidOutput, RequestMethodError, IgnoreRequest
from pprint import pformat
from collections import defaultdict
from bald_spider.middleware import BaseMiddleware
from bald_spider.utils.project import common_call
from bald_spider.event import ignore_request

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
        self._stats = crawler.stats

    async def _process_request(self, request: Request):
        """走完只有三种情况，第一种把返回值返回出去，第二种只对request做预处理，
        第三种报错，也就是说循环走完后request是预处理完的，直接扔过去下载就可以了
        如果返回的是Request或者Response的话，根本走不到下载那一步，因为返回Request的话，会重新入队，返回Response就不需要重新下载了"""
        for method in self.methods["process_request"]:
            # result = method(request, self.crawler.spider)
            result = await common_call(method, request, self.crawler.spider)  # 兼容异步
            if result is None:
                continue
            if isinstance(request, (Request, Response)):
                return result
            raise InvalidOutput(
                f"{method.__qualname__} must return None, Request or Response, got {type(result).__name__}.")
        return await self.download_method(request)

    async def _process_response(self, request: Request, response: Response):
        """只能返回request和response, 因为下载成功不能返回None"""
        for method in reversed(self.methods["process_response"]):
            try:
                response = await common_call(method, request, response, self.crawler.spider)
            except IgnoreRequest as exc:
                create_task(self.crawler.subscriber.notify(ignore_request, exc, request, self.crawler.spider))
            else:
                if isinstance(response, Request):
                    return response
                if isinstance(response, Response):
                    continue
                raise InvalidOutput(
                    f"{method.__qualname__} must return Request or Response, got {type(response).__name__}.")
        return response

    async def _process_exception(self, request: Request, exc: Exception):
        for method in reversed(self.methods["process_exception"]):
            response = await common_call(method, request, exc, self.crawler.spider)
            if response is None:  # 如果返回None, 异常继续向上抛
                continue
            if isinstance(response, (Request, Response)):
                return response
            raise InvalidOutput(
                f"{method.__qualname__} must return None, Request or Response, got {type(response).__name__}.")
        else:
            raise exc

    async def download(self, request: Request) -> Optional[Response]:
        """called in the downloader"""
        try:
            response = await self._process_request(request)
        except KeyError:
            #在下载器的时候有预留东西，self.request_method如果传的不是get或post会抛出keyerror
            raise RequestMethodError(f"{request.method.lower()} is not allowed")
        except IgnoreRequest as exc:
            create_task(self.crawler.subscriber.notify(ignore_request, exc, request, self.crawler.spider))
            self.logger.info(f"{request} ignored.")
            self._stats.inc_value("request_ignore_count")
            response = await self._process_exception(request, exc)
        except Exception as exc:
            self._stats.inc_value(f"download_error/{exc.__class__.__name__}")
            response = await self._process_exception(request, exc)
        else:
            # 临时性代码
            create_task(self.crawler.subscriber.notify(response_received, response, self.crawler.spider))
            self.crawler.stats.inc_value("response_received_count")
        if isinstance(response, Response):
            response = await self._process_response(request, response)
        if isinstance(response, Request):
            await self.crawler.engine.enqueue_request(request)
            return None
        return response

    def _add_method(self):
        for middleware in self.middlewares:
            if hasattr(middleware, "process_request"):
                if self._validate_method("process_request", middleware):
                    self.methods["process_request"].append(middleware.process_request)
            if hasattr(middleware, "process_response"):
                if self._validate_method("process_response", middleware):
                    self.methods["process_response"].append(middleware.process_response)
            if hasattr(middleware, "process_exception"):
                if self._validate_method("process_exception", middleware):
                    self.methods["process_exception"].append(middleware.process_exception)

    def _add_middleware(self, middlewares):
        enable_middlewares = [m for m in middlewares if self._validate_middleware(m)]
        if enable_middlewares:
            self.logger.info(f"enable middlewares:\n {pformat(enable_middlewares)}")

    def _validate_middleware(self, middleware):
        middleware_cls = load_class(middleware)
        if not hasattr(middleware_cls, "create_instance"):
            raise MiddlewareInitError(
                f"Middleware Init failed,must inherit from `BaseMiddleware` or must have `create_instance` method.")
        instance = middleware_cls.create_instance(self.crawler)
        self.middlewares.append(instance)
        return True

    @classmethod
    def create_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @staticmethod
    def _validate_method(method_name, middleware) -> bool:
        method = getattr(type(middleware), method_name)
        base_method = getattr(BaseMiddleware, method_name)
        return False if method == base_method else True
        # if method == base_method:
        #     return False
        # else:
        #     return True
