# redis_manager.py
import redis
import hashlib
from typing import Optional, Union


class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0, password: Optional[str] = None):
        """初始化Redis管理器"""
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )

    def get_url_fingerprint(self, url: str) -> str:
        """生成URL的指纹"""
        return hashlib.md5(url.encode()).hexdigest()

    def is_url_crawled(self, url: str) -> bool:
        """检查URL是否已经爬取过"""
        fingerprint = self.get_url_fingerprint(url)
        # 将Redis返回的0或1转换为布尔值
        return bool(self.client.sismember('crawled_urls', fingerprint))

    def mark_url_crawled(self, url: str) -> None:
        """标记URL为已爬取"""
        fingerprint = self.get_url_fingerprint(url)
        self.client.sadd('crawled_urls', fingerprint)

    def clear_crawled_urls(self) -> None:
        """清除所有已爬取的URL记录"""
        self.client.delete('crawled_urls')