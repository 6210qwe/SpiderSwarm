import requests

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

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://vip.tulingpyton.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://vip.tulingpyton.cn/p/t_pc/course_pc_detail/big_column/p_6401e7b0e4b02685a44cf852',
    'Req-UUID': '20250329190242000691896',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
    'retry': '1',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

# 使用data参数发送请求
data = '{"column_id":"p_67a44a87e4b0694c5a8bd39b","page_size":20,"page_index":2,"content_app_id":null}'

try:
    response = requests.post(
        'https://vip.tulingpyton.cn/xe.course.business.column.items.get/2.0.0',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False  # 添加此参数以忽略SSL证书验证
    )

    # 设置响应编码
    response.encoding = 'utf-8'

    # 打印响应内容
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {str(e)}")