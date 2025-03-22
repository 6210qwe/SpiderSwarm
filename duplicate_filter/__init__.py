from abc import ABC, abstractmethod
from bald_spider import Request
from bald_spider.utils.request import request_fingerprint


class BaseFilter(ABC):
    def __init__(self, logger, stats, debug: bool):
        self.logger = logger
        self.stats = stats
        self.debug = debug

    @classmethod
    def create_instance(cls, *args, **kwargs) -> 'BaseFilter':
        return cls(*args, **kwargs)

    def requested(self, request: Request) -> bool:
        fp = request_fingerprint(request)
        if fp in self:
            return True
        self.add(fp)

    # 需要有一个方法判断当前的请求是否被请求过，不管写几个过滤器，必须有方法，判断是否在请求过的容器里面
    # 用内存，文件，数据库，通用条件使用in, 默认会调用__contains__方法

    def filter(self, request: 'Request') -> bool:
        """
        :param request:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def add(self, fp):
        # 具体加的逻辑，交给子类去做
        pass

    def log_stats(self, request: Request) -> None:
        if self.debug:
            self.logger.debug(f"Filtered duplicate request: {request}")
        self.stats.inc_value(f"{self}/filtered")

    @abstractmethod
    def __contains__(self, fp):
        # 具体判断的逻辑，交给子类去做
        pass
