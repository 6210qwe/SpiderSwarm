"""
default config
"""
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
IGNORE_HTTP_CODES = [403]
MAX_RETRY_TIMES = 3

MIDDLEWARES = [
    "bald_spider.middleware.request_ignore.RequestIgnore",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    # "bald_spider.middleware.request_delay.RequestDelay",
    # "bald_spider.middleware.request_random_delay.RequestRandomDelay",
    # "bald_spider.middleware.request_random_user_agent.RequestRandomUserAgent",
    # "bald_spider.middleware.request_random_cookie.RequestRandomCookie",
]


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
