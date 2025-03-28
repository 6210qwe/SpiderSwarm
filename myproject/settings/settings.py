# 爬虫配置
SPIDER_NAME = "my_spider"
SPIDER_DOMAIN = "example.com"

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "spider_db",
    "user": "root",
    "password": "password"
}

# 并发配置
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1

# 中间件配置
MIDDLEWARE = [
    "middleware.user_agent_middleware.RandomUserAgentMiddleware",
    "middleware.proxy_middleware.ProxyMiddleware",
]

# 管道配置
PIPELINE = [
    "pipeline.database_pipeline.DatabasePipeline",
]
