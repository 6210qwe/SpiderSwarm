PROJECT_NAME = "baidu_spider"
CONCURRENCY = 16
ABC = "qqqq"
LOG_LEVEL = "DEBUG"
# USE_SESSION = False
# DOWNLOADER = "bald_spider.core.downloader.aiohttp_downloader.AioDownloader"
MIDDLEWARES = [
    "bald_spider.middleware.request_ignore.RequestIgnore",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    # "test.baidu_spider.middleware.TestMiddleware",
    # "test.baidu_spider.middleware.TestMiddleware1",
]

PIPELINES = [
    "test.baidu_spider.pipeline.TestPipeline",
]

