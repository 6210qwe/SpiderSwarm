PROJECT_NAME = "company_spider"
CONCURRENCY = 16
ABC = "qqqq"
LOG_LEVEL = "INFO"
# USE_SESSION = False
# DOWNLOADER = "bald_spider.core.downloader.aiohttp_downloader.AioDownloader"
MIDDLEWARES = [
    "bald_spider.middleware.download_delay.DownloadDelay",
    "bald_spider.middleware.retry.Retry",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    # "bald_spider.middleware.request_ignore.RequestIgnore",
    # "company_spider.middleware.TunnelProxyMiddleware",
]

PIPELINES = [
    # "company_spider.pipeline.TenderPipeline",
    # "company_spider.pipeline.MysqlPipeline",
    # "company_spider.pipeline.AsyncMySQLPipeline",
]
