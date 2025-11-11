PROJECT_NAME = "tender_spider"
CONCURRENCY = 16
ABC = "qqqq"
LOG_LEVEL = "INFO"
# USE_SESSION = False
# DOWNLOADER = "bald_spider.core.downloader.aiohttp_downloader.AioDownloader"
MIDDLEWARES = [
    "bald_spider.middleware.download_delay.DownloadDelay",
    "bald_spider.middleware.retry.Retry",
    "bald_spider.middleware.response_code.ResponseCodeStats",
    "bald_spider.middleware.request_ignore.RequestIgnore",
]

PIPELINES = [
    "tender_spider.pipeline.TenderPipeline",
]

KEYWORDS = ['医疗', '器械', '耗材', '疫苗', '诊断试剂']