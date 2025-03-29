import requests
from bs4 import BeautifulSoup
import time
from redis_spider_utils import RedisSpiderUtils
import logging
from typing import List, Dict, Any
import random
import json
from datetime import datetime
import hashlib

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DistributedSpider:
    def __init__(self, spider_name: str, max_empty_retries: int = 3, empty_queue_sleep: int = 60):
        """
        初始化爬虫
        :param spider_name: 爬虫名称
        :param max_empty_retries: 最大空队列重试次数
        :param empty_queue_sleep: 空队列等待时间（秒）
        """
        # 初始化Redis工具类
        self.redis_utils = RedisSpiderUtils(host='localhost', port=6379)
        self.spider_name = spider_name
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 空队列控制参数
        self.max_empty_retries = max_empty_retries
        self.empty_queue_sleep = empty_queue_sleep
        self.empty_retries = 0
        # 运行状态
        self.is_running = True
        
    def _get_url_md5(self, url: str) -> str:
        """
        获取URL的MD5哈希值
        :param url: URL地址
        :return: MD5哈希值
        """
        return hashlib.md5(url.encode('utf-8')).hexdigest()
        
    def add_initial_urls(self, urls: List[str], method: str = 'GET', data: Dict = None):
        """
        添加初始URL到队列
        :param urls: URL列表
        :param method: 请求方法
        :param data: POST请求数据
        """
        for url in urls:
            self.redis_utils.add_url_to_queues(url, self.spider_name, method, data)
            
    def process_request(self, request_info: Dict) -> Dict:
        """
        处理单个请求
        :param request_info: 请求信息
        :return: 处理结果
        """
        url = request_info['url']
        method = request_info['method']
        data = request_info['data']
        url_md5 = request_info['url_md5']
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            else:
                response = requests.post(url, headers=self.headers, data=data)
                
            response.raise_for_status()
            
            # 解析响应
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取数据（示例）
            result = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'content': soup.get_text()[:200],  # 只取前200个字符
                'crawl_time': datetime.now().isoformat()
            }
            
            # 保存数据
            self.redis_utils.save_crawled_data(self.spider_name, result, url_md5)
            
            # 标记请求完成
            self.redis_utils.mark_request_completed(self.spider_name, url_md5)
            
            return result
            
        except Exception as e:
            logging.error(f"处理请求失败: {url}, 错误: {str(e)}")
            return None
            
    def stop(self):
        """
        停止爬虫
        """
        self.is_running = False
        logging.info("爬虫停止运行")
            
    def crawl(self):
        """
        持续从队列中获取并处理请求
        """
        while self.is_running:
            try:
                # 获取下一个请求
                request_info = self.redis_utils.get_next_request(self.spider_name)
                
                if not request_info:
                    self.empty_retries += 1
                    logging.info(f"队列为空，等待新请求... (第{self.empty_retries}次)")
                    
                    # 检查是否达到最大重试次数
                    if self.empty_retries >= self.max_empty_retries:
                        logging.info(f"队列持续空置{self.max_empty_retries}次，爬虫停止运行")
                        self.stop()
                        break
                        
                    # 等待一段时间后继续
                    time.sleep(self.empty_queue_sleep)
                    continue
                    
                # 重置空队列计数
                self.empty_retries = 0
                    
                # 处理请求
                result = self.process_request(request_info)
                
                if result:
                    logging.info(f"成功处理URL: {request_info['url']}")
                    
                # 随机延时
                # time.sleep(random.uniform(1, 3))
                
            except KeyboardInterrupt:
                logging.info("爬虫被手动中断")
                self.stop()
                break
            except Exception as e:
                logging.error(f"爬虫运行出错: {str(e)}")
                time.sleep(5)
                
    def get_queue_status(self) -> Dict[str, int]:
        """
        获取队列状态
        :return: 队列状态信息
        """
        duplicate_length, request_length = self.redis_utils.get_queue_length(self.spider_name)
        return {
            'duplicate_queue_length': duplicate_length,
            'request_queue_length': request_length,
            'empty_retries': self.empty_retries
        }
        
    def clear_spider_data(self):
        """
        清除爬虫数据
        """
        self.redis_utils.clear_spider_data(self.spider_name)
        logging.info("已清除爬虫数据")

def main():
    # 创建爬虫实例
    spider = DistributedSpider(
        spider_name="distributed_spider",
        max_empty_retries=3,  # 最多等待3次
        empty_queue_sleep=60  # 每次等待60秒
    )
    
    # 添加初始URL
    initial_urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
    spider.add_initial_urls(initial_urls)
    
    try:
        # 开始爬取
        spider.crawl()
    except KeyboardInterrupt:
        logging.info("爬虫被手动中断")
    finally:
        # 获取最终状态
        status = spider.get_queue_status()
        logging.info(f"爬虫状态: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    main() 