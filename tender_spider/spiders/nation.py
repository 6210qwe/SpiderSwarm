from datetime import datetime, timedelta

from bald_spider.spider import Spider
from bald_spider import Request
from loguru import logger

from tender_spider.items import TenderItem
from bald_spider.event import spider_error
from bald_spider.utils.project import get_settings


class NationSpider(Spider):
    def __init__(self):
        super().__init__()
        self.cookies = {
            'JSESSIONID': '65f542abfb203af95459bb0d7d04',
            'JSESSIONID': '65f542abfb203af95459bb0d7d04',
            'insert_cookie': '61459989',
        }
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://deal.ggzy.gov.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://deal.ggzy.gov.cn/ds/deal/dealList.jsp',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'Cookie': 'JSESSIONID=65f542abfb203af95459bb0d7d04; JSESSIONID=65f542abfb203af95459bb0d7d04; insert_cookie=61459989',
        }

    custom_settings = {"CONCURRENCY": 20}

    @classmethod
    def create_instance(cls, crawler):
        o = cls()
        o.crawler = crawler
        crawler.subscriber.subscribe(o.spider_error, event=spider_error)
        return o

    def generate_request_data(self, page=1, keyword='医疗', deal_type='政府采购'):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # 基础参数
        data = {
            'TIMEBEGIN_SHOW': start_date_str,
            'TIMEEND_SHOW': end_date_str,
            'TIMEBEGIN': start_date_str,
            'TIMEEND': end_date_str,
            'SOURCE_TYPE': '1',
            'DEAL_TIME': '06',
            'DEAL_CLASSIFY': '00',
            'DEAL_STAGE': '0000',
            'DEAL_PROVINCE': '0',
            'DEAL_CITY': '0',
            'DEAL_PLATFORM': '0',
            'BID_PLATFORM': '0',
            'DEAL_TRADE': '0',
            'isShowAll': '1',
            'PAGENUMBER': str(page),
            'FINDTXT': keyword,
        }

        if deal_type == '政府采购':
            data.update({
                'DEAL_CLASSIFY': '02',
                'DEAL_STAGE': '0200',
            })
        elif deal_type == '药品采购':
            data.update({
                'DEAL_CLASSIFY': '23',
                'DEAL_STAGE': '2300',
            })
        elif deal_type == '二类疫苗':
            data.update({
                'DEAL_CLASSIFY': '24',
                'DEAL_STAGE': '2400',
            })
        else:
            data.update({
                'DEAL_CLASSIFY': '90',
                'DEAL_STAGE': '9000',
            })
        return data

    def start_request(self):
        settings = get_settings()
        keywords = settings.getlist('KEYWORDS')
        deal_types = ['政府采购', '药品采购', '二类疫苗', '其他']
        for keyword in keywords:
            for deal_type in deal_types:
                form_data = self.generate_request_data(keyword=keyword, deal_type=deal_type)
                yield Request(
                    url='https://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp',
                    body=form_data,
                    cookies=self.cookies,
                    headers=self.headers,
                    callback=self.parse_total_pages,
                    method="POST",
                    meta={'keyword': keyword, 'deal_type': deal_type},
                    dont_filter=True
                )

    def parse_total_pages(self, response):
        if response.status == 200:
            json_data = response.json()
            total_rows = json_data.get('ttlrow', 0)
            total_pages = (total_rows // 20) + 1
            logger.info(f"总页数: {total_pages}, 总条数{total_rows}, 类型: {response.meta['deal_type']}")
            keyword = response.meta['keyword']
            deal_type = response.meta['deal_type']
            if total_pages != 0:
                for page in range(1, total_pages + 1):
                    new_data = self.generate_request_data(page, keyword=keyword, deal_type=deal_type)
                    yield Request(
                        url='https://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp',
                        body=new_data,
                        cookies=self.cookies,
                        headers=self.headers,
                        callback=self.parse_page,
                        method="POST",
                        meta={'keyword': keyword, 'deal_type': deal_type},
                        dont_filter=True
                    )
        else:
            logger.error(f"请求失败，状态码: {response.status}")

    def parse_page(self, response):
        # for i in range(10):
        #     url = "http://www.baidu.com"
        #     meta = {"test": "waws"}
        #     request = Request(url=url, callback=self.parse_detail, meta=meta)
        #     yield request

    def parse_detail(self, response):
        # item = BaiduItem()
        item = {}
        item["url"] = response.url
        item["title"] = response.xpath("//title/text()").get()
        yield item

    async def spider_error(self, exc, spider):
        print(f"爬虫出错了{exc}, 请紧急处理一下.")
