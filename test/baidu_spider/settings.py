PROJECT_NAME = "baidu_spider"
CONCURRENCY = 16
ABC = "qqqq"
LOG_LEVEL = "DEBUG"
# USE_SESSION = False
# DOWNLOADER = "bald_spider.core.downloader.aiohttp_downloader.AioDownloader"
MIDDLEWARES = [
    "bald_spider.middleware.download_delay.DownloadDelay",
    "bald_spider.middleware.default_header.DefaultHeader",
    "bald_spider.middleware.retry.Retry",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    "bald_spider.middleware.request_ignore.RequestIgnore",
    # "test.baidu_spider.middleware.TestMiddleware",
    # "test.baidu_spider.middleware.TestMiddleware1",
]

PIPELINES = [
    "test.baidu_spider.pipeline.TestPipeline",
]

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
 }