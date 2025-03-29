import requests
import json
import urllib3
# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 设置cookies
cookies = {
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

# 设置请求头，移除可能导致编码问题的复杂JSON字符串
headers = {
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


def convert_jump_url(jump_url: str) -> str:
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
    new_url = f"https://vip.tulingpyton.cn/detail/{resource_id}/4"

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
# 设置请求数据
json_data = {
    'column_id': 'p_67a44a87e4b0694c5a8bd39b',
    'page_size': 20,
    'page_index': 1,
    'content_app_id': None,
}

try:
    for page in range(0, 2):
        json_data['page_index'] = page + 1
        response = requests.post(
            'https://vip.tulingpyton.cn/xe.course.business.column.items.get/2.0.0',
            cookies=cookies,
            headers=headers,
            json=json_data,
            verify=False  # 如果有SSL证书问题，可以添加此参数
        )

        # 设置响应编码
        response.encoding = 'utf-8'

        # 打印响应内容
        datas = response.json()['data']['list']
        for data in datas:
            title = data['resource_title']
            url = data['jump_url']
            url = convert_jump_url(url)
            print(title, url)

except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {str(e)}")