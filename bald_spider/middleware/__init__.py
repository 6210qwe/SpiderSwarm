from typing import Union

from bald_spider import Request, Response


class BaseMiddleware:
    # def process_request(self, request, spider) -> None | Request | Response:
    def process_request(self, request, spider) -> Union[None, Request, Response]:
        # 请求的预处理
        pass

    def process_response(self, request, response, spider) -> Union[Request, Response]:
        # 响应的预处理
        pass

    def process_exception(self, request, exc, spider) -> Union[None, Request, Response]:
        # 异常处理
        pass

    @classmethod
    def create_instance(cls, crawler):
        return cls()

