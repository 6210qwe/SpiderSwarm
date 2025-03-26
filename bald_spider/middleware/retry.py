from typing import List

from httpx import RemoteProtocolError, ConnectError, ReadTimeout

from bald_spider.stats_collector import StatsCollector
from bald_spider.utils.log import get_logger
from asyncio.exceptions import TimeoutError
from aiohttp import ClientConnectionError, ClientTimeout, ClientConnectorError, ClientResponseError
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError
from anyio import EndOfStream
from httpcore import ReadError

_retry_exceptions = [
    ClientConnectionError,
    ClientTimeout,
    # ClientConnectorSSLError,
    ClientResponseError,
    RemoteProtocolError,
    ReadError,
    EndOfStream,
    ConnectError,
    TimeoutError,
    ClientPayloadError,
    ReadTimeout,
    ClientConnectorError,
]


class Retry:

    def __init__(self,
                 *,
                 retry_http_codes: List,
                 ignore_http_codes: List,
                 max_retry_times: int,
                 retry_exceptions: List,
                 stats: StatsCollector,
                 ):
        self.retry_http_codes = retry_http_codes
        self.ignore_http_codes = ignore_http_codes
        self.max_retry_times = max_retry_times
        # self.retry_exceptions = retry_exceptions
        self.retry_exceptions = tuple(retry_exceptions + _retry_exceptions)
        self.stats = stats
        self.logger = get_logger(self.__class__.__name__, "INFO")

    @classmethod
    def create_instance(cls, crawler):
        o = cls(
            retry_http_codes=crawler.settings.getlist("RETRY_HTTP_CODES"),
            ignore_http_codes=crawler.settings.getlist("IGNORE_HTTP_CODES"),
            max_retry_times=crawler.settings.getint("RETRY_TIMES"),
            retry_exceptions=crawler.settings.getlist("RETRY_EXCEPTIONS"),
            stats=crawler.stats,
        )
        return o

    def process_response(self, request, response, spider):
        """在process_response中返回request,请求会重新入队"""
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.ignore_http_codes:
            return response
        if response.status in self.retry_http_codes:
            reason = f"response code: {response.status}"
            # 因为process_response不允许返回None, 所以如果是None的话，就返回response, 但是有问题的response返回给engine会有问题，所以返回response，所以如果出错，回调函数依然可以执行
            # 但是如果是错误的状态码，是没必要扔到engine中去的，这个问题产生的原因就是重试到最大次数的时候会返回None,对process_exception是没有问题的，因为它本身支持返回None
            # process_response 不支持返回None，所以在后面加了 or response
            # 对于状态码是404的响应，对spider脚本是没有任何作用的，反而会影响回调函数中的逻辑，像这种我们是不能要的
            # 写一个中间件处理，需要紧接着我们当前所写的process_response
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exc, spider):
        if (
            isinstance(exc, self.retry_exceptions)
            and not request.meta.get("dont_retry", False)
        ):
            return self._retry(request, type(exc).__name__, spider)

    def _retry(self, request, reason, spider):
        """如果状态码有问题，会重试，第一次进来给默认值0，"""
        # todo 去重的逻辑还没写，要保证重试的请求不要被请求过滤器给过滤掉
        # 重新发起的请求它的请求的优先级应该怎么定
        retry_times = request.meta.get("retry_times", 0)  #因为第一次进来获取不到，给默认值0
        if retry_times < self.max_retry_times:
            retry_times += 1
            self.logger.info(f" {request} {reason} retrying {retry_times}...")
            request.meta["retry_times"] = retry_times
            self.stats.inc_value("retry/count")
            return request
        else:
            self.logger.info(f" {request} {reason} retrying max {self.max_retry_times} times, give up")
            return None























