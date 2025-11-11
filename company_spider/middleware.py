from bald_spider.event import spider_opened
from bald_spider.middleware import BaseMiddleware


class TestMiddleware(BaseMiddleware):

    def __init__(self):
        pass

    async def process_request(self, request, spider):
        # print("BaseMiddleware process_request", request, spider)
        # return None
        print(request.proxy)
        return request

    async def process_response(self, request, response, spider):
        # 响应的预处理
        print(request, response)
        return response

    async def process_exception(self, request, exc, spider):
        # 异常处理
        print("process_exception", request, exc, spider)
        # return None


class TestMiddleware1(BaseMiddleware):
    async def process_response(self, request, response, spider):
        # 响应的预处理
        print(request, response)
        return response

    async def process_exception(self, request, exc, spider):
        # 异常处理
        print("process_exception", request, exc, spider)
        # return None


# class TunnelProxyMiddleware:
#     def __init__(self):
#         self.username = "t13632437348639"
#         self.password = "10cc7lx7"
#         self.tunnel = "g184.kdltps.com:15818"
#
#     @classmethod
#     def create_instance(cls, crawler):
#         o = cls()
#         return o
#
#     async def process_request(self, request, spider):
#         pass
#         # request.proxy = 'http://t13632437348639:10cc7lx7@g184.kdltps.com:15818'
#         # if request.url.startswith('https'):
#         #     request.proxy = f"https://{self.username}:{self.password}@{self.tunnel}"
#         # else:
#         #     request.proxy = f"http://{self.username}:{self.password}@{self.tunnel}"
#         # print(request.proxy)
#
#     async def process_exception(self, request, exc, spider):
#         # 异常处理
#         print("process_exception", request, exc, spider)
