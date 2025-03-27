"""
default config
"""
VERSION = 1.0
CONCURRENCY = 8
ABC = "wwww"

LOG_LEVEL = "INFO"
VERIFY_SSL = True
REQUEST_TIMEOUT = 60
USE_SESSION = True
DOWNLOADER = "bald_spider.core.downloader.aiohttp_downloader.AioDownloader"
# DOWNLOADER = "bald_spider.core.downloader.httpx_downloader.HttpxDownloader"

INTERVAL = 5
STATS_DUMP = True

# retry
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
IGNORE_HTTP_CODES = [403, 404]
MAX_RETRY_TIMES = 3

# MIDDLEWARES = [
#     "bald_spider.middleware.request_ignore.RequestIgnore",
#     "bald_spider.middleware.response_code.ResponseCodeStats",
#     # "bald_spider.middleware.request_delay.RequestDelay",
#     # "bald_spider.middleware.request_random_delay.RequestRandomDelay",
#     # "bald_spider.middleware.request_random_user_agent.RequestRandomUserAgent",
#     # "bald_spider.middleware.request_random_cookie.RequestRandomCookie",
# ]


DOWNLOAD_DELAY = 0
RANDOMNESS = True
RANDOM_RANGE = (0.75, 1.25)

FILTER_DEBUG = True
# FILTER_CLS = "bald_spider.duplicate_filter.memory_filter.MemoryFilter"
# FILTER_CLS = "bald_spider.duplicate_filter.redis_filter.RedisFilter"
# FILTER_CLS = "bald_spider.duplicate_filter.aioredis_filter.AioRedisFilter"

# redis_filter
REDIS_URL = "redis://localhost/0"  # redis://[[username]:[password]]@host:port/db
DECODE_RESPONSES = True
REDIS_KEY = "request_fingerprint"
SAVE_FP = True
# SAVE_FP = False  # redis在去重后将键删掉
REQUEST_DIR = '.'
# 先状态码收集，然后重试，然后过滤掉
MIDDLEWARES = [

    "bald_spider.middleware.download_delay.DownloadDelay",
    "bald_spider.middleware.default_header.DefaultHeader",
    "bald_spider.middleware.response_filter.ResponseFilter",
    "bald_spider.middleware.retry.Retry",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    "bald_spider.middleware.request_ignore.RequestIgnore",
    # "test.baidu_spider.middleware.TestMiddleware",
    # "test.baidu_spider.middleware.TestMiddleware1",
]

EXTENSIONS = [
    "bald_spider.extension.log_interval.LogInterval",
    "bald_spider.extension.log_stats.LogStats",
]
PIPELINES = [
    "test.baidu_spider.pipeline.TestPipeline",
]

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}
ALLOWED_CODES = [404]