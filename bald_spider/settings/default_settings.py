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

FILTER_DEBUG = True
# FILTER_CLS = "bald_spider.duplicate_filter.memory_filter.MemoryFilter"
FILTER_CLS = "bald_spider.duplicate_filter.redis_filter.RedisFilter"
# FILTER_CLS = "bald_spider.duplicate_filter.aioredis_filter.AioRedisFilter"

# redis_filter
REDIS_URL = "redis://localhost/0" # redis://[[username]:[password]]@host:port/db
DECODE_RESPONSES = True
REDIS_KEY = "request_fingerprint"
SAVE_FP = True
# SAVE_FP = False  # redis在去重后将键删掉
REQUEST_DIR = '.'




















