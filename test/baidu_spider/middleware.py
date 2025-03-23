from bald_spider.middleware import BaseMiddleware


class TestMiddleware(BaseMiddleware):

    def __init__(self):
        pass

    async def process_request(self, request, spider):
        print("BaseMiddleware process_request", request, spider)
        # return None

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
