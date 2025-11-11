import re
from datetime import datetime
# import requests
from curl_cffi import requests
from bs4 import BeautifulSoup
from spider_tools.utils import get_proxy, retry
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import time
from loguru import logger
from get_mysqldb import DatabasePool


# def get_proxy():
#     tunnel = "g184.kdltps.com:15818"
#     username = "t13632437348639"
#     password = "10cc7lx7"
#     proxies = {
#         "http": f"http://{username}:{password}@{tunnel}",
#         "https": f"http://{username}:{password}@{tunnel}"
#     }
#     return proxies
#
#
# def retry(max_retries=8, retry_delay=5):
#     """重试装饰器"""
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             last_exception = None
#             for retry_count in range(max_retries):
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception as e:
#                     last_exception = e
#                     if retry_count < max_retries - 1:
#                         time.sleep(retry_delay)
#                         continue
#             if last_exception:
#                 logger.error(f"{func.__name__} 执行失败，{max_retries} 次重试后失败，原因: {last_exception}")
#             return None
#
#         return wrapper
#
#     return decorator


class AlibabaSpider:
    def __init__(self):
        self.DB_HOST = "rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com"
        self.DB_PORT = 3306
        self.DB_DATABASE = "touzi"
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
        self.proxies = get_proxy()
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://s.1688.com/',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cache',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        }
        self.cookies = self.get_cookies()

    @retry(max_retries=5, retry_delay=1)
    def get_cookies(self):
        requests_session = requests.Session()
        cookies = {
            'tfstk': 'gZbZUuAp1PUwMxp9jwTq4aLV3gT9WEyWjZ9XisfD1dvMCsYnxCdMmNT119JcF9YXCSFxunvhpisb6n6BnT62GN_fijRcdFxAfK963E5AUWw7Pz1O6EK0F8a5uljrsEp0lEqB--prOJw7Pz1Gxys4C8_bbgnMdIYDsnAmKWRXgAAcnqv3TIAjIm0GnWPeGQmMsI0i-DAvaEvcnEVFtpdDoCXDoATBnLgeahVbtBuHclG9jLfMLq0rwC-MGzpEoqbe_6Jlsu0mowRwbwjanF8HfifJ2N1bu2L1aMYHgZFo0K-PmNThSJ4kvnjcVnSII56l36Xv5wVmjLj1CebG4j0cTFJecC-tQJJlW6bJ-Haua6bdC1QFGj4DOT9h6NY4r7LwSdYe9ZwKSKShmNt9kA22Hw5hSiSyZxdhzlbAbxm2jBdeFWPFNfZtVsu6iCoxDhIpTLNT6mnvjBdeFWPEDmK9JBJ765C..',
            '_user_vitals_session_data_': '{"user_line_track":true,"ul_session_id":"srcpv0ytpu","last_page_id":"s.1688.com%2Fronuba9x5e"}',
        }
        params = {
            'jsv': '2.5.1',
            'appKey': '12574478',
            't': '1747046133769',
            'sign': 'd0e5aa7cdb94cf0613e1ab9d361b0a0e',
            'api': 'mtop.relationrecommend.WirelessRecommend.recommend',
            'v': '2.0',
            'jsonpIncPrefix': 'reqTppId_32517_getSearchConfig',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'callback': 'mtopjsonpreqTppId_32517_getSearchConfig1',
            # 'data': '{"appId":32517,"params":"{\\"method\\":\\"getSearchConfig\\",\\"pageId\\":\\"8U1owNjOPLUVptVAmf3WLmyGW7mXiIO7yYDtCz26XICFWnVa\\",\\"verticalProductFlag\\":\\"pcmarket\\",\\"searchScene\\":\\"pcOfferSearch\\",\\"charset\\":\\"GBK\\",\\"spm\\":\\"a26352.13672862.searchbox.0\\",\\"keywords\\":\\"%CC%FD%D5%EF%C6%F7\\"}"}',
        }
        response = requests_session.get(
            'https://h5api.m.1688.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/',
            params=params,
            cookies=cookies,
            headers=self.headers,
        )
        # print(response.status_code)
        # print(response.text)
        new_cookies = requests_session.cookies.get_dict()  # 获取新的cookie字典
        requests_session.close()
        return new_cookies

    def generate_signature(self, data):
        # token = "23e9bb4b28b4fdb270de05bdd3043690"
        m_h5_tk = self.cookies.get('_m_h5_tk', '')
        token = m_h5_tk.split('_')[0]
        g = "12574478"
        i = int(time.time() * 1000)
        data_str = json.dumps(data)
        text_to_hash = f"{token}&{i}&{g}&{data_str}"
        md5_hash = hashlib.md5(text_to_hash.encode('utf-8')).hexdigest()
        return {
            'signature': md5_hash,
            'timestamp': i
        }

    def parse_jsonp(self, jsonp_str):
        match = re.match(r'^[^(]+\((.*)\)[^)]*$', jsonp_str)
        if match:
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError as e:
                logger.info(f"JSON解析错误: {e}")
                return None
        else:
            logger.info("未找到有效的JSONP格式")
            return None

    def convert_date(self, date_str: str) -> str:
        """
        将中文格式的日期字符串转换为 MySQL DATE 类型所需的 YYYY-MM-DD 格式
        Args:
            date_str: 中文日期字符串，例如 '2009年01月13日'
        Returns:
            转换后的标准日期字符串，例如 '2009-01-13'
            如果格式不匹配，返回原始字符串
        """
        try:
            date_obj = datetime.strptime(date_str, '%Y年%m月%d日')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            logger.info(f"日期格式转换失败: {date_str}，请检查是否符合 'YYYY年MM月DD日' 格式")
            return date_str

    def extract_title(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(strip=True) if html_content else None

    def extract_and_clean_text(self, response):
        # print(response.text)
        json_match = re.search(r'var offer_details=(\{.*});', response.text)
        if json_match:
            json_str = json_match.group(1)
            if json_str:  # 确保json_str不为None
                soup = BeautifulSoup(json_str, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
                if text:  # 确保text不为None
                    text = text.replace('{"content":"', '').replace('"}', '').strip()
                    text = text.replace('\r\n', '').replace('\r', '').replace('\t', ' ').replace('\n', ' ')
                    text = re.sub(r'[\r\n]+', ' ', text).strip()
                    if text and text is not None:
                        print(text)
                        cleaned_text = " ".join(text.split()).strip().replace('\\r\\n', '\n')
                        return cleaned_text
                    else:
                        return ""
        return ""

    @retry(max_retries=5, retry_delay=1)
    def extract_image_src_from_response(self, response, title):
        json_match = re.search(r'var offer_details=(\{.*});', response.text)
        if not json_match:
            # logger.info(f"未找到offer_details变量 {title}")
            return []
        json_str = json_match.group(1)
        try:
            data = json.loads(json_str)
            html_content = data.get("content")
            if html_content is None:
                return []
        except json.JSONDecodeError as e:
            logger.info(f"JSON解析错误: {e}")
            return []
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all('img')
        src_urls = [img.get('src') for img in img_tags if img.get('src')]
        return src_urls

    @retry(max_retries=5, retry_delay=1)
    def parse_contact_info(self, item_data):
        inner_params = {
            "memberId": item_data.get('memberId')
        }
        data_obj = {
            "componentKey": "wp_pc_contactsmall",
            "params": json.dumps(inner_params)
        }
        params = {
            'jsv': '2.7.0',
            'appKey': '12574478',
            'api': 'mtop.alibaba.alisite.cbu.server.pc.ModuleAsyncService',
            'v': '1.0',
            'type': 'jsonp',
            'valueType': 'string',
            'dataType': 'jsonp',
            'timeout': '10000',
            'callback': 'mtopjsonp1',
            'data': json.dumps(data_obj),
        }
        data = self.generate_signature(data_obj)
        params['t'] = data['timestamp']
        params['sign'] = data['signature']
        response = requests.get(
            'https://h5api.m.1688.com/h5/mtop.alibaba.alisite.cbu.server.pc.moduleasyncservice/1.0/',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            proxies=self.proxies,
            verify=False
        )
        response.raise_for_status()
        match = re.match(r'mtopjsonp1\((.*)\)', response.text)
        if match:
            json_str = match.group(1)
            data_dict = json.loads(json_str)
            contact_info = data_dict.get('data')
            item_data['contact_info'] = json.dumps(contact_info, ensure_ascii=False)
            item_data['companyName'] = contact_info.get('companyName')
            item_data['msg'] = contact_info.get('msg')
            item_data['mobileNo'] = contact_info.get('mobileNo')
            item_data['faxNum'] = contact_info.get('faxNum')
            condition = {"url": item_data["url"]}
            query_results = self.mysql_db.query("alibaba_1688", condition=condition, get_results=True)
            if not query_results:
                self.mysql_db.insert("alibaba_1688", data_dict=item_data, return_ids=True)
            else:
                print("数据已存在")

    @retry(max_retries=5, retry_delay=1)
    def parse_contact_address(self, item_data):
        params = {
            'jsv': '2.7.0',
            'appKey': '12574478',
            'api': 'mtop.1688.map.shop.ulr.query',
            'v': '1.0',
            'type': 'json',
            'valueType': 'string',
            'dataType': 'json',
            'timeout': '10000',
        }
        member_id = item_data.get('memberId')
        data_obj = {
            "appVersion": "11.6",
            "memberId": str(member_id)
        }
        data_ = self.generate_signature(data_obj)
        params['t'] = data_['timestamp']
        params['sign'] = data_['signature']
        data = {
            'data': json.dumps(data_obj),
        }
        response = requests.post(
            'https://h5api.m.1688.com/h5/mtop.1688.map.shop.ulr.query/1.0/',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )
        response.raise_for_status()
        response_json = response.json()
        item_data['entAddress'] = response_json.get('data', {}).get('model', {}).get('entAddress')
        self.parse_contact_info(item_data)

    @retry(max_retries=5, retry_delay=1)
    def parse_factory(self, item_data):
        response = requests.get(item_data.get('factory_url'),
                                cookies=self.cookies,
                                headers=self.headers,
                                verify=False,
                                proxies=self.proxies)
        response.raise_for_status()
        match = re.search(r'window\.\$\$pageData\s*=\s*(\{.*?});', response.text, re.DOTALL)
        if match:
            init_props_str = match.group(1)
            data = json.loads(init_props_str)
            company_info = data.get('3', {}).get('initShopInfo', {})
            item_data['company_info'] = json.dumps(company_info, ensure_ascii=False)
            item_data['company_name'] = company_info.get('loginId')
            companyYearStarted = company_info.get('companyYearStarted')
            if companyYearStarted:
                item_data['establish_date'] = self.convert_date(companyYearStarted)
            employee_info = company_info.get('employeeData', {})
            item_data['employee_info'] = json.dumps(employee_info)
            item_data['employee_count'] = employee_info.get('workerNum2')
            item_data['tags'] = json.dumps(company_info.get('highQualityTagList', []), ensure_ascii=False)
            self.parse_contact_address(item_data)

    @retry(max_retries=5, retry_delay=1)
    def parse_description(self, item_data, url):
        response = requests.get(item_data.get('detail_url'),
                                cookies=self.cookies,
                                headers=self.headers,
                                verify=False,
                                proxies=self.proxies
                                )
        print(item_data)
        # response.raise_for_status()
        # cleaned = self.extract_and_clean_text(response)
        # item_data['description'] = cleaned
        # urls = self.extract_image_src_from_response(response, item_data['title'])
        # item_data['urls'] = json.dumps(urls)
        # # logger.info(item_data)
        # self.parse_factory(item_data)

    @retry(max_retries=5, retry_delay=1)
    def parse_detail_data(self, item_data):
        params = {
            'spm': 'a26352.13672862.offerlist.1.65851e62KlGJjx',
            'cosite': '-',
            'tracelog': 'p4p',
            '_p_isad': '1',
            'clickid': '0ae92ef1984e40da93d173c35324e770',
            'sessionid': 'b78a672290e82d86367be979e6d829dd',
        }
        response = requests.get(item_data.get('url'),
                                params=params,
                                cookies=self.cookies,
                                headers=self.headers,
                                verify=False,
                                proxies=self.proxies
                                )
        response.raise_for_status()
        pattern = r"window.__INIT_DATA=({.*?</script)"
        match = re.search(pattern, response.text, re.DOTALL)
        if match:
            init_props_str = match.group(1).replace("</script", '')
            json_str = json.loads(init_props_str)
            datas = json_str.get('data', {}).get('1081181309201', {}).get('data')
            item_data['detail_url'] = json_str.get('data', {}).get('1081181309894', {}).get('data', {}).get(
                'detailUrl')
            item_data['item_detail'] = json.dumps(datas, ensure_ascii=False)
        pattern2 = r"window.__STORE_DATA=({.*?</script)"
        match2 = re.search(pattern2, response.text, re.DOTALL)
        if match2:
            init_props_str2 = match2.group(1).replace("</script", '')
            json_str2 = json.loads(init_props_str2)
            newMenuObj = json_str2.get('components', {}).get('38229151', {}).get('moduleData', {}).get('newMenuObj', {})
            item_data['newMenuObj'] = json.dumps(newMenuObj, ensure_ascii=False)
        self.parse_description(item_data, item_data.get('url'))

    @retry(max_retries=5, retry_delay=1)
    def parse_list_page(self, page, keyword):
        logger.info(f"正在请求第{page}页")
        data_dict = {
            "appId": 32517,
            "params": json.dumps({
                "verticalProductFlag": "pcmarket",
                "searchScene": "pcOfferSearch",
                "charset": "GBK",
                "beginPage": page,
                "pageSize": 60,
                # "keywords": "%CC%FD%D5%EF%C6%F7",
                "keywords": keyword,
                "spm": "a26352.13672862.searchbox.0",
                "method": "getOfferList"
            })
        }
        # 将字典转换为JSON字符串
        data = json.dumps(data_dict)
        params = {
            'jsv': '2.5.1',
            'appKey': '12574478',
            'api': 'mtop.relationrecommend.WirelessRecommend.recommend',
            'ignoreLogin': 'true',
            'prefix': 'h5api',
            'v': '2.0',
            'dataType': 'jsonp',
            'jsonpIncPrefix': 'fetchTpp_32517_getOfferList',
            'timeout': '20000',
            'type': 'jsonp',
            'callback': 'mtopjsonpfetchTpp_32517_getOfferList4',
            'data': data,
        }
        data = self.generate_signature(data_dict)
        params['t'] = data['timestamp']
        params['sign'] = data['signature']
        response = requests.get(
            'https://h5api.m.1688.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            proxies=self.proxies,
            verify=False,
        )
        # logger.info(response.text)
        response.raise_for_status()
        json_str = self.parse_jsonp(response.text)
        items = json_str.get('data', {}).get('data', {}).get('OFFER', {}).get('items', [])
        logger.info(len(items))
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for data in items:
                executor.submit(self.parse_list, data)
            for future in as_completed(futures):
                future.result()
        # with ThreadPoolExecutor(max_workers=20) as executor:
        #     for data in items:
        #         executor.submit(self.parse_list, data)
        #     executor.shutdown()

    @retry(max_retries=5, retry_delay=1)
    def parse_list(self, data):
        item_data = {}
        item_data['title'] = self.extract_title(data.get('data', {}).get('title'))
        item_data['url'] = "https://detail.1688.com/offer/" + data.get('data', {}).get('offerId',
                                                                                       "") + ".html"
        item_data['memberId'] = data.get('data', {}).get('memberId')
        item_data['factory_url'] = "https://sale.1688.com/factory/card.html?memberId=" + item_data.get('memberId',
                                                                                                       "")
        self.parse_detail_data(item_data)

    def run(self):
        keyword = ["手术刀", "器械", "设备"]
        for keyword in keyword:
            import urllib.parse
            encoded_str = urllib.parse.quote(keyword, encoding="GBK", errors="replace")
            for page in range(1, 35):
                self.parse_list_page(page, encoded_str)

        # self.parse_list_page(1)
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     for page in range(1, 5):
        #         executor.submit(self.parse_list_page, page)
        #     executor.shutdown()


if __name__ == "__main__":
    spider = AlibabaSpider()
    spider.run()
