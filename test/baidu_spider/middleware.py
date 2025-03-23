from bald_spider.middleware import BaseMiddleware


class TestMiddleware(BaseMiddleware):

    def __init__(self):
        pass

    async def process_request(self, request, spider):
        print("BaseMiddleware process_request", request, spider)
        # 请求的预处理
        # pass

    def process_response(self):
        # 响应的预处理
        pass

    def process_execption(self):
        # 异常处理
        pass

class TestMiddleware1(BaseMiddleware):
    def process_response(self, request, spider):
        # 响应的预处理
        pass

    def process_execption(self):
        # 异常处理
        pass