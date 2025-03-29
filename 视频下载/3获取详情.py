import requests
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://vip.tulingpyton.cn/p/t_pc/live_pc/pc/l_67ac8139e4b0694c5a905853',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
    'confusion': '2'
}

params = {
    'app_id': 'appssry6rs71641',
    'alive_id': 'l_67ac8139e4b0694c5a905853',
}

try:
    response = requests.get(
        'https://vip.tulingpyton.cn/_alive/api/get_lookback_list',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False  # 忽略SSL证书验证
    )
    response.encoding = 'utf-8'  # 设置响应编码
    m3u8_datas = response.json()['data']
    # for m3u8_data in m3u8_datas:
    #     print(m3u8_data)
    #     line_sharpness = m3u8_data['line_sharpness'][0]
    #     url = line_sharpness.get('url', '')
    #     print(url)
    if m3u8_datas:
        m3u8_data = m3u8_datas[0]  # 只取第一个数据
        line_sharpness = m3u8_data['line_sharpness'][0]
        url = line_sharpness.get('url', '')
        print(url)
except Exception as e:
    print(f"请求发生错误: {str(e)}")