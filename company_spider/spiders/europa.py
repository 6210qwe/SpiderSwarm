from bald_spider.spider import Spider
from bald_spider import Request
from get_mysqldb import DatabasePool
from loguru import logger
from bald_spider.event import spider_error
from bald_spider.utils.project import get_settings
import json
from spider_tools.utils import get_proxy, retry
from company_spider.items import MedicalDeviceItem


class EuropaSpider(Spider):
    def __init__(self):
        super().__init__()
        self.BASE_URL = "https://ec.europa.eu/tools/eudamed/api/devices/udiDiData"
        self.cookies = {
            'cck1': '%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Afalse%7D',
        }
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'No-Cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Pragma': 'no-cache',
            'Referer': 'https://ec.europa.eu/tools/eudamed/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'Cookie': 'cck1=%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Afalse%7D',
        }
        self.DB_HOST = "rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com"
        self.DB_PORT = 3306
        self.DB_DATABASE = "yaojianju"
        self.DB_USER = "zhangyanzhen"
        self.DB_PASSWORD = "yutu#2025"
        self.mysql_db = DatabasePool(
            logger=logger,
            DB_HOST=self.DB_HOST,
            DB_PORT=self.DB_PORT,
            DB_DATABASE=self.DB_DATABASE,
            DB_USER=self.DB_USER,
            DB_PASSWORD=self.DB_PASSWORD
        )

    custom_settings = {"CONCURRENCY": 20}

    @classmethod
    def create_instance(cls, crawler):
        o = cls()
        o.crawler = crawler
        crawler.subscriber.subscribe(o.spider_error, event=spider_error)
        return o

    def start_request(self):
        # for page in range(9002, 15000):
        # for page in range(12498, 15000):
        # for page in range(8000, 10000):
        # for page in range(4000, 6000):
        for page in range(9000, 12000):
            print(f"正在爬取第{page}页")
            params = {
                'page': page,
                'pageSize': 50,
                'size': 50,
                'iso2Code': 'en',
                'sort': ['primaryDi,ASC', 'versionNumber,DESC'],
                'deviceStatusCode': 'refdata.device-model-status.on-the-market',
                'languageIso2Code': 'en'
            }
            yield Request(
                url='https://ec.europa.eu/tools/eudamed/api/devices/udiDiData',
                params=params,
                cookies=self.cookies,
                headers=self.headers,
                callback=self.parse_page,
                dont_filter=True
            )

    def parse_page(self, response):
        contents = response.json()['content']
        for content in contents:
            item_data = {}
            # 基础字段（必选，默认值设为None或空字符串）
            item_data['url'] = f"https://ec.europa.eu/tools/eudamed/#/screen/search-device/{content.get('uuid', '')}"
            item_data['basicUdi'] = content.get('basicUdi')
            item_data['primaryDi'] = content.get('primaryDi')
            item_data['uuid'] = content.get('uuid')
            item_data['ulid'] = content.get('ulid')
            item_data['basicUdiDiDataUlid'] = content.get('basicUdiDiDataUlid')
            risk_class = content.get('riskClass', {})
            item_data['riskClass'] = json.dumps(risk_class, ensure_ascii=False)

            device_status_type = content.get('deviceStatusType', {})
            item_data['deviceStatusType'] = json.dumps(device_status_type, ensure_ascii=False)

            manufacturer_status = content.get('manufacturerStatus', {})
            item_data['manufacturerStatus'] = json.dumps(manufacturer_status, ensure_ascii=False)

            item_data['tradeName'] = content.get('tradeName')
            item_data['manufacturerName'] = content.get('manufacturerName')
            item_data['manufacturerSrn'] = content.get('manufacturerSrn')
            item_data['manufacturerNames'] = content.get('manufacturerNames')

            item_data['latestVersion'] = content.get('latestVersion', False)
            item_data['versionNumber'] = content.get('versionNumber', '')
            item_data['basicUdiDataVersionNumber'] = content.get('basicUdiDataVersionNumber', '')
            item_data['containerPackageCount'] = content.get('containerPackageCount', '')

            item_data['basicUdiDataUuid'] = content.get('basicUdiDataUuid')
            item_data['basicUdiDataUlid'] = content.get('basicUdiDataUlid')
            item_data['basicUdiDataVersionState'] = content.get('basicUdiDataVersionState')
            item_data['versionState'] = content.get('versionState')
            item_data['deviceName'] = content.get('deviceName')
            item_data['deviceModel'] = content.get('deviceModel')
            item_data['lastUpdateDate'] = content.get('lastUpdateDate')
            item_data['reference'] = content.get('reference')
            item_data['issuingAgency'] = content.get('issuingAgency')
            item_data['mfOrPrSrn'] = content.get('mfOrPrSrn')
            item_data['applicableLegislation'] = content.get('applicableLegislation')
            item_data['authorisedRepresentativeSrn'] = content.get('authorisedRepresentativeSrn')
            item_data['authorisedRepresentativeName'] = content.get('authorisedRepresentativeName')
            item_data['sterile'] = content.get('sterile')
            item_data['multiComponent'] = content.get('multiComponent')
            item_data['deviceCriterion'] = content.get('deviceCriterion')
            item_data['page_data'] = json.dumps(content, ensure_ascii=False)
            params = {
                'languageIso2Code': 'en',
            }
            yield Request(
                'https://ec.europa.eu/tools/eudamed/api/devices/basicUdiData/udiDiData/' + item_data['uuid'],
                body=params,
                cookies=self.cookies,
                headers=self.headers,
                callback=self.parse_basic_devices_data,
                meta={'item_data': item_data}
            )

    def parse_basic_devices_data(self, response):
        item_data = response.meta['item_data']
        data = response.json()
        uuid = data.get('manufacturer').get('uuid')
        item_data['all_basic_data'] = json.dumps(data, ensure_ascii=False)
        params = {
            'languageIso2Code': 'en',
        }
        yield Request(
            'https://ec.europa.eu/tools/eudamed/api/actors/' + uuid + '/publicInformation',
            body=params,
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse_detail_devices_data,
            meta={'item_data': item_data}
        )

    def parse_detail_devices_data(self, response):
        item_data = response.meta['item_data']
        datas = response.json()
        item_data['all_device_data'] = json.dumps(datas, ensure_ascii=False)
        # item = MedicalDeviceItem()
        # item['item_data'] = item_data
        # yield item
        condition = {"primaryDi": item_data['primaryDi']}
        query_results = self.mysql_db.query("eudamed_device_copy12", condition=condition, get_results=True)
        if not query_results:
            self.mysql_db.insert("eudamed_device_copy12", data_dict=item_data, return_ids=True)
        else:
            print("数据已存在", item_data['primaryDi'])

    async def spider_error(self, exc, spider):
        print(f"爬虫出错了{exc}, 请紧急处理一下.")
