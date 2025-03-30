import base64

import requests
import json
import urllib3
from typing import Dict, List, Optional
from hs_m3u8 import M3u8Downloader
import asyncio
import os
from pathlib import Path
from loguru import logger
# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TulingSpider:
    def __init__(self):
        self.base_url = 'https://vip.tulingpyton.cn'
        self.cookies = {
            'anonymous_user_key': 'dV9hbm9ueW1vdXNfNjY5YTVhMTAzYzQ3ZV9SZ0xhcDdHdVJE',
            'sensorsdata2015jssdkcross': '%7B%22%24device_id%22%3A%22190caefeb8a659-071b051a9cfd55-4c657b58-1474560-190caefeb8b58c%22%7D',
            'Hm_lvt_68a51533e634d0e8a2ec721a36d779fd': '1723462863',
            'sa_jssdk_2015_vip_tulingpyton_cn': '%7B%22distinct_id%22%3A%22u_65d66599d5049_zHFstwoMln%22%2C%22first_id%22%3A%22190caefeb8a659-071b051a9cfd55-4c657b58-1474560-190caefeb8b58c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D',
            'shop_version_type': '8',
            'LANGUAGE_appssry6rs71641': 'cn',
            'appId': '"appssry6rs71641"',
            'pc_user_key': '15022a7a8d52cb4f5966e82d73ac6c55',
            'xenbyfpfUnhLsdkZbX': '0',
            'show_user_icon': '1',
            'app_id': '"appssry6rs71641"'
        }

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://vip.tulingpyton.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://vip.tulingpyton.cn/p/t_pc/course_pc_detail/big_column/p_6401e7b0e4b02685a44cf852',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

    def convert_jump_url(self, jump_url: str) -> str:
        """
        将jump_url转换为完整的详情页URL
        :param jump_url: 原始jump_url
        :return: 转换后的完整URL
        """
        # 移除开头的斜杠
        jump_url = jump_url.lstrip('/')

        # 解析URL参数
        params = {}
        if '?' in jump_url:
            base_url, query = jump_url.split('?', 1)
            for param in query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value
        else:
            base_url = jump_url

        # 从base_url中提取resource_id
        resource_id = base_url.split('/')[-1]

        # 构建新的URL
        new_url = f"{self.base_url}/detail/{resource_id}/4"

        # 添加必要的参数
        new_params = {
            'from': params.get('pro_id', ''),
            'content_app_id': params.get('app_id', ''),
            'type': '8',
            'parent_pro_id': 'p_6401e7b0e4b02685a44cf852'
        }

        # 将参数添加到URL
        query_string = '&'.join([f"{k}={v}" for k, v in new_params.items() if v])
        if query_string:
            new_url += f"?{query_string}"

        return new_url

    def get_course_list(self, column_id: str, page_size: int = 20, page_index: int = 1) -> List[Dict]:
        """
        获取课程列表
        :param column_id: 专栏ID
        :param page_size: 每页数量
        :param page_index: 页码
        :return: 课程列表数据
        """
        json_data = {
            'column_id': column_id,
            'page_size': page_size,
            'page_index': page_index,
            'content_app_id': None,
        }

        try:
            response = requests.post(
                f'{self.base_url}/xe.course.business.column.items.get/2.0.0',
                cookies=self.cookies,
                headers=self.headers,
                json=json_data,
                verify=False
            )
            print(response.text)
            response.encoding = 'utf-8'
            return response.json()['data']['list']
        except requests.exceptions.RequestException as e:
            logger.info(f"请求发生错误: {str(e)}")
            return []

    def extract_id_from_url(self, url: str) -> str:
        """
        从URL中提取detail后面的ID
        :param url: 完整的URL
        :return: ID字符串
        """
        try:
            # 分割URL获取detail后面的部分
            parts = url.split('/detail/')
            if len(parts) > 1:
                # 获取ID部分（到下一个斜杠之前）
                id_part = parts[1].split('/')[0]
                return id_part
            return ''
        except Exception:
            return ''

    def crawl_courses(self, column_id: str, max_pages: int = 2):
        """
        爬取课程信息
        :param column_id: 专栏ID
        :param max_pages: 最大页数
        """
        for page in range(max_pages):
            courses = self.get_course_list(column_id, page_index=page + 1)
            for course in courses:
                title = course['resource_title']
                url = self.convert_jump_url(course['jump_url'])
                logger.info(f"{title}, 链接为: {url}")
                alive_id = self.extract_id_from_url(url)
                if alive_id.startswith("ey"):
                    alive_id = self.decode_base64(alive_id)
                    self.get_m3u8(title, alive_id)
                else:
                    self.get_m3u8_new(title, alive_id)

    def get_m3u8(self, title, alive_id):
        import requests

        """
        获取m3u8地址
        :param title: 视频标题
        :param alive_id: 视频ID
        """
        # 简化的headers
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://vip.tulingpyton.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://vip.tulingpyton.cn/p/t_pc/course_pc_detail/video/v_62c6a194e4b00a4f37234bca',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }

        # 简化的cookies
        cookies = {
            'anonymous_user_key': 'dV9hbm9ueW1vdXNfNjY5YTVhMTAzYzQ3ZV9SZ0xhcDdHdVJE',
            'sensorsdata2015jssdkcross': '%7B%22%24device_id%22%3A%22190caefeb8a659-071b051a9cfd55-4c657b58-1474560-190caefeb8b58c%22%7D',
            'Hm_lvt_68a51533e634d0e8a2ec721a36d779fd': '1723462863',
            'shop_version_type': '8',
            'LANGUAGE_appssry6rs71641': 'cn',
            'appId': '"appssry6rs71641"',
            'pc_user_key': '15022a7a8d52cb4f5966e82d73ac6c55',
            'xenbyfpfUnhLsdkZbX': '0',
            'show_user_icon': '1',
            'app_id': '"appssry6rs71641"'
        }

        data = {
            'resource_id': str(alive_id),
        }
        print(data)
        response = requests.post(
            'https://vip.tulingpyton.cn/xe.course.business.video.mutli_line/1.0.0',
            cookies=cookies,
            headers=headers,
            data=data,
        )
        response.encoding = 'utf-8'  # 设置响应编码
        cloud_data = response.json().get('data', {}).get('cloud_data', {})
        if cloud_data:
            platform_data = cloud_data.get("hw", {})
            if platform_data:
                url = platform_data.get('encrypt_url', '')
                if url:
                    print(f"开始下载视频: {title}, url为: {url}")
                    self.download_video(title, url)
                else:
                    print(f"未找到视频地址: {title}")
        else:
            print(f"未找到云数据: {title}")

        # print(response.text)
        # m3u8_datas = response.json()['data']['cloud_data']
        # if m3u8_datas:
        #     m3u8_data = m3u8_datas[0]  # 只取第一个数据
        #     line_sharpness = m3u8_data['line_sharpness'][0]
        #     url = line_sharpness.get('url', '')
        #     logger.info(title, url)
        #     self.download_video(title, url)


    def decode_base64(self, base64_str: str) -> dict:
        """
        解码base64字符串
        :param base64_str: base64编码的字符串
        :return: 解码后的字典
        """
        try:
            # 添加正确的填充
            padding = 4 - (len(base64_str) % 4)
            if padding != 4:
                base64_str += '=' * padding

            # 解码base64
            decoded_bytes = base64.b64decode(base64_str)
            decoded_str = decoded_bytes.decode('utf-8')
            # 解析JSON
            return json.loads(decoded_str)['resource_id']
        except Exception as e:
            print(f"解码失败: {str(e)}")
            return {}

    def get_m3u8_new(self, title, alive_id):
        params = {
            'app_id': 'appssry6rs71641',
            'alive_id': str(alive_id),
        }
        response = requests.get(
            'https://vip.tulingpyton.cn/_alive/api/get_lookback_list',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            verify=False  # 忽略SSL证书验证
        )
        response.encoding = 'utf-8'  # 设置响应编码
        m3u8_datas = response.json()['data']
        if m3u8_datas:
            m3u8_data = m3u8_datas[0]  # 只取第一个数据
            line_sharpness = m3u8_data['line_sharpness'][0]
            url = line_sharpness.get('url', '')
            logger.info(title, url)
            self.download_video(title, url)

    def download_video(self, title: str, url: str):
        """
        下载视频
        :param title: 视频标题
        :param url: m3u8地址
        """
        # 获取桌面路径
        desktop_path = Path.home() / "Desktop/安卓第二期"

        # 创建异步事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # 创建下载器实例
            dl = M3u8Downloader(
                m3u8_url=url,
                save_path=str(desktop_path / title),
                max_workers=64,
            )
            # # 创建下载器实例
            # downloader = m3u8_downloader.M3U8Downloader(
            #     url=url,
            #     save_path=save_path,
            #     max_workers=64
            # )
            # 运行下载任务
            loop.run_until_complete(dl.run(del_hls=False, merge=True))
            logger.info(f"视频 {title} 下载完成")
        except Exception as e:
            logger.info(f"下载视频 {title} 时发生错误: {str(e)}")
        finally:
            loop.close()


def main():
    spider = TulingSpider()
    # spider.crawl_courses('p_67a44a87e4b0694c5a8bd39b')
    # spider.crawl_courses('p_629db4b9e4b0812e17a2f4bc', 7)
    spider.crawl_courses('p_6540bba5e4b064a863bf3127', 8)


if __name__ == '__main__':
    main()
