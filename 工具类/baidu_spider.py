import requests
from bs4 import BeautifulSoup
import time
from redis_spider_utils import RedisSpiderUtils
import logging
from typing import List, Dict, Any
import random

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class BaiduSpider:
    def __init__(self):
        # 初始化Redis工具类
        self.redis_utils = RedisSpiderUtils(host='localhost', port=6379)
        self.spider_name = "baidu_spider"
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_search_results(self, keyword: str, page: int = 1) -> List[Dict[str, Any]]:
        """
        获取百度搜索结果
        :param keyword: 搜索关键词
        :param page: 页码
        :return: 搜索结果列表
        """
        base_url = "https://www.baidu.com/s"
        params = {
            'wd': keyword,
            'pn': (page - 1) * 10
        }

        try:
            response = requests.get(base_url, params=params, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            results = []
            for item in soup.select('.result'):
                title = item.select_one('.t')
                if title:
                    title_text = title.get_text(strip=True)
                    link = title.find('a')['href'] if title.find('a') else ''
                    abstract = item.select_one('.c-abstract')
                    abstract_text = abstract.get_text(strip=True) if abstract else ''

                    result = {
                        'title': title_text,
                        'url': link,
                        'abstract': abstract_text,
                        'keyword': keyword,
                        'page': page
                    }
                    results.append(result)

            return results
        except Exception as e:
            logging.error(f"获取搜索结果失败: {str(e)}")
            return []

    def crawl(self, keyword: str, max_pages: int = 5):
        """
        爬取百度搜索结果
        :param keyword: 搜索关键词
        :param max_pages: 最大爬取页数
        """
        # 获取上次爬取状态
        last_state = self.redis_utils.get_crawl_state(self.spider_name)
        start_page = 1

        if last_state and last_state.get('keyword') == keyword:
            start_page = last_state.get('current_page', 1)
            logging.info(f"从第{start_page}页继续爬取")

        for page in range(start_page, max_pages + 1):
            logging.info(f"正在爬取第{page}页")

            # 获取搜索结果
            results = self.get_search_results(keyword, page)

            for result in results:
                url = result['url']

                # URL去重
                if self.redis_utils.is_url_visited(url, self.spider_name):
                    logging.info(f"URL已访问过: {url}")
                    continue

                # 生成唯一ID
                unique_id = f"{keyword}_{page}_{url}"

                # 检查数据是否已存在
                if not self.redis_utils.is_data_exists(self.spider_name, unique_id):
                    # 保存爬取的数据
                    self.redis_utils.save_crawled_data(self.spider_name, result, unique_id)
                    # 标记URL为已访问
                    self.redis_utils.mark_url_visited(url, self.spider_name)
                    logging.info(f"保存数据: {result['title']}")

                # 随机延时，避免被封
                time.sleep(random.uniform(1, 3))

            # 保存爬虫状态
            state = {
                'keyword': keyword,
                'current_page': page,
                'last_update': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self.redis_utils.save_crawl_state(self.spider_name, state)

            # 页面间延时
            time.sleep(random.uniform(2, 4))

    def get_incremental_results(self, keyword: str, last_update_time: str) -> List[Dict[str, Any]]:
        """
        获取增量搜索结果
        :param keyword: 搜索关键词
        :param last_update_time: 上次更新时间
        :return: 增量数据列表
        """
        return self.redis_utils.get_incremental_data(self.spider_name, last_update_time)

    def clear_spider_data(self):
        """
        清除爬虫数据
        """
        self.redis_utils.clear_spider_data(self.spider_name)
        logging.info("已清除爬虫数据")


def main():
    # 创建爬虫实例
    spider = BaiduSpider()

    # 设置搜索关键词
    keyword = "Python爬虫"

    try:
        # 开始爬取
        spider.crawl(keyword, max_pages=3)

        # 获取增量数据示例
        last_update = "2024-01-01T00:00:00"
        incremental_data = spider.get_incremental_results(keyword, last_update)
        logging.info(f"获取到{len(incremental_data)}条增量数据")

    except KeyboardInterrupt:
        logging.info("爬虫被手动中断")
    except Exception as e:
        logging.error(f"爬虫运行出错: {str(e)}")
    finally:
        # 保存最终状态
        state = {
            'keyword': keyword,
            'status': 'completed',
            'last_update': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        spider.redis_utils.save_crawl_state(spider.spider_name, state)


if __name__ == "__main__":
    main()

# 1、对url进行去重，无论是post还是get请求，将url在第一个队列duplicate_urls中去重, 并且将增加的数据同步到第二个队列requests_urls中
# 2、爬虫发请求的时候是从第二个队列中获取url, 爬取完之后，将第二个队列中的数据去掉
# 3、

# 目前的需求只是
#