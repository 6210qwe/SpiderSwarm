from bald_spider import Middleware
from loguru import logger

class BaseMiddleware(Middleware):
    def process_request(self, request):
        pass

    def process_response(self, response):
        return response

    def process_exception(self, request, exception):
        logger.error(f"请求异常: {exception}")
        return request
