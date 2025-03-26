# 在当前中间件中，把错误的状态码拦截掉，不要让它回到引擎，那么回调函数就不会被调用了
# 还需要提供一个接口，方便开发者调试
from bald_spider.exceptions import IgnoreRequest
from bald_spider.utils.log import get_logger


class ResponseFilter:
    def __init__(self, allowed_codes, log_level):
        self.allowed_codes = allowed_codes
        self.logger = get_logger(self.__class__.__name__, log_level)

    @classmethod
    def create_instance(cls, crawler):
        return cls(
            allowed_codes=crawler.settings.get("ALLOWED_CODES"),
            log_level=crawler.settings.get("LOG_LEVEL")
        )

    def process_response(self, request, response, spider):
        if 200 <= response.status < 300:
            return response
        if response.status in self.allowed_codes:
            return response
        # 当抛出异常的时候，在中间件_process_response的地方，会notify一下，然后request_ignore会启动，然后统计计数
        raise IgnoreRequest(f"response_status/non-200")















