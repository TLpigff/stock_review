# 根据公开资料整理，不作为买卖依据

import pywencai
import pandas as pd
import requests
import json

file_name = '复盘.csv'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'DNT': '1',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"
}

param_map = {
    '指数': {
        "url": "https://x-quote.cls.cn/quote/stocks/basic",
        "param": {
            'app': 'CailianpressWeb',
            'fields': 'secu_name,secu_code,trade_status,change,change_px,last_px',
            'os': 'web',
            'secu_codes': 'sh000001,sz399001,sz399006',
            'sv': '7.7.5'
        }
    },
    '连板天梯': {
        "url": "https://x-quote.cls.cn/quote/index/up_down_analysis",
        "param": {
            'app': 'CailianpressWeb',
            'os': 'web',
            'sv': '7.7.5',
            'rever': '1',
            'type':'continuous_up_pool',
            'way': 'limit_up_days'
        }
    }
}

def 指数():
    # 发送 GET 请求
    response = requests.get(param_map['指数']['url'], headers=headers, params=param_map['指数']['param'])
    content = response.text.encode('utf-8').decode('unicode_escape')
    return json.loads(content)

def 连板天梯():
    # 发送 GET 请求
    response = requests.get(param_map['连板天梯']['url'], headers=headers, params=param_map['连板天梯']['param'])
    return json.loads(response.text)

def wencai(**kwargs):
    query = kwargs.get('query')
    query_type = kwargs.get('query_type','stock')
    cookie='other_uid=Ths_iwencai_Xuangu_s1e2xtpqi8wty9vgts3up1aeklanhmsa; ta_random_userid=s9cfw1a6ol; cid=5b58f21b2099cb8b327c3c71a9581bb01726156949; PHPSESSID=ddabea4a55168ee404f6f19e9f636e0f; wencai_pc_version=1; v=AysXlKL2yaQYXxXC3FxA3wUgukQQQG-WuUMDbZ0sBqbBh0U6JRDPEskkk2au'
    res = pywencai.get(query=query, cookie=cookie, query_type=query_type)
    return res

def convert_to_percentage(s):
    num = float(s)
    result = "{:.2f}%".format(num * 100)
    if num >= 0:
        return "+" + result
    else:
        return result

def write_大盘指数():
    markdown_content = "# 大盘指数\n\n"
    markdown_content += "| 指数 | 点位 | 涨跌 |\n"
    markdown_content += "| ---- | --- | --- |\n"

    data = 指数()
    zhishus = ['sh000001','sz399001','sz399006']
    for zhishu in zhishus:
        zhishu_data = data['data'][zhishu]
        markdown_content += f"| {zhishu_data['secu_name']} | {zhishu_data['last_px']} | {convert_to_percentage(zhishu_data['change'])} |\n"

    with open('output.md', 'w', encoding='utf-8') as file:
        file.write(markdown_content)    

def write_连板天梯():
    markdown_content = "# 连板天梯\n\n"
    markdown_content += "| 连续涨停数 | 股票 | 涨停原因 |\n"
    markdown_content += "| ---- | --- | --- |\n"

    data = 连板天梯()
    for stock in data['data']:
        if 'ST' in stock['secu_name']:
            continue
        markdown_content += f"| {stock['limit_up_days']} | {stock['secu_name']} | {stock['up_reason'].split('|')[0]} |\n"

    with open('output.md', 'w', encoding='utf-8') as file:
        file.write(markdown_content)

def main():
    write_连板天梯()

if __name__ == "__main__":
    main()