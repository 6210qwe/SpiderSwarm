import redis
import json
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import hashlib
from w3lib.url import canonicalize_url


class RedisSpiderUtils:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        """
        初始化Redis连接
        :param host: Redis主机地址
        :param port: Redis端口
        :param db: Redis数据库编号
        :param password: Redis密码
        """
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )

    def _get_url_md5(self, url: str) -> str:
        """
        获取URL的MD5哈希值
        :param url: URL地址
        :return: MD5哈希值
        """
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def add_url_to_queues(self, url: str, spider_name: str, method: str = 'GET', data: Dict = None) -> bool:
        """
        将URL添加到去重队列和请求队列
        :param url: URL地址
        :param spider_name: 爬虫名称
        :param method: 请求方法（GET/POST）
        :param data: POST请求的数据
        :return: 是否添加成功
        """
        # 获取URL的MD5哈希值
        url_md5 = self._get_url_md5(url)

        # 检查URL是否已存在
        if self.redis_client.sismember(f"spider:{spider_name}:duplicate_urls", url_md5):
            return False

        # 构建请求信息
        request_info = {
            'url': url,
            'method': method,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'url_md5': url_md5
        }

        # 添加到去重队列
        self.redis_client.sadd(f"spider:{spider_name}:duplicate_urls", url_md5)

        # 添加到请求队列
        self.redis_client.rpush(f"spider:{spider_name}:request_urls", json.dumps(request_info))

        return True

    def get_next_request(self, spider_name: str) -> Optional[Dict]:
        """
        从请求队列中获取下一个请求
        :param spider_name: 爬虫名称
        :return: 请求信息
        """
        # 从队列中获取并移除第一个请求
        request_str = self.redis_client.lpop(f"spider:{spider_name}:request_urls")
        if request_str:
            return json.loads(request_str)
        return None

    def mark_request_completed(self, spider_name: str, url_md5: str):
        """
        标记请求已完成
        :param spider_name: 爬虫名称
        :param url_md5: URL的MD5哈希值
        """
        self.redis_client.srem(f"spider:{spider_name}:duplicate_urls", url_md5)

    def save_crawl_state(self, spider_name: str, state_data: Dict[str, Any]):
        """
        保存爬虫状态
        :param spider_name: 爬虫名称
        :param state_data: 状态数据
        """
        key = f"spider:{spider_name}:state"
        state_data['last_update'] = datetime.now().isoformat()
        self.redis_client.set(key, json.dumps(state_data))

    def get_crawl_state(self, spider_name: str) -> Optional[Dict[str, Any]]:
        """
        获取爬虫状态
        :param spider_name: 爬虫名称
        :return: 状态数据
        """
        key = f"spider:{spider_name}:state"
        state_str = self.redis_client.get(key)
        if state_str:
            return json.loads(state_str)
        return None

    def save_crawled_data(self, spider_name: str, data: Dict[str, Any], url_md5: str):
        """
        保存爬取的数据
        :param spider_name: 爬虫名称
        :param data: 爬取的数据
        :param url_md5: URL的MD5哈希值
        """
        key = f"spider:{spider_name}:data:{url_md5}"
        data['crawl_time'] = datetime.now().isoformat()
        self.redis_client.set(key, json.dumps(data))

    def get_crawled_data(self, spider_name: str, url_md5: str) -> Optional[Dict[str, Any]]:
        """
        获取已爬取的数据
        :param spider_name: 爬虫名称
        :param url_md5: URL的MD5哈希值
        :return: 爬取的数据
        """
        key = f"spider:{spider_name}:data:{url_md5}"
        data_str = self.redis_client.get(key)
        if data_str:
            return json.loads(data_str)
        return None

    def is_data_exists(self, spider_name: str, url_md5: str) -> bool:
        """
        检查数据是否已存在
        :param spider_name: 爬虫名称
        :param url_md5: URL的MD5哈希值
        :return: 是否存在
        """
        key = f"spider:{spider_name}:data:{url_md5}"
        return self.redis_client.exists(key)

    def get_incremental_data(self, spider_name: str, last_update_time: str) -> List[Dict[str, Any]]:
        """
        获取增量数据
        :param spider_name: 爬虫名称
        :param last_update_time: 上次更新时间
        :return: 增量数据列表
        """
        pattern = f"spider:{spider_name}:data:*"
        keys = self.redis_client.keys(pattern)
        incremental_data = []

        for key in keys:
            data_str = self.redis_client.get(key)
            if data_str:
                data = json.loads(data_str)
                if data['crawl_time'] > last_update_time:
                    incremental_data.append(data)

        return incremental_data

    def clear_spider_data(self, spider_name: str):
        """
        清除爬虫数据
        :param spider_name: 爬虫名称
        """
        pattern = f"spider:{spider_name}:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)

    def get_queue_length(self, spider_name: str) -> Tuple[int, int]:
        """
        获取队列长度
        :param spider_name: 爬虫名称
        :return: (去重队列长度, 请求队列长度)
        """
        duplicate_length = self.redis_client.scard(f"spider:{spider_name}:duplicate_urls")
        request_length = self.redis_client.llen(f"spider:{spider_name}:request_urls")
        return duplicate_length, request_length
