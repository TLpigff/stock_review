# 根据公开资料整理，不作为买卖依据

import wencai
import pandas as pd
import requests
import json
import datetime


current_date = datetime.datetime.now()
#current_date = current_date - datetime.timedelta(days=1)
formatted_date = current_date.strftime('%Y%m%d')

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
            'secu_codes': 'sh000001,sz399001,sz399006,sh000688,899050.BJ',
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
            'type': 'up_pool',
            'way': 'limit_up_days'
        }
    },
    '个股涨跌': {
        "url": "https://x-quote.cls.cn/v2/quote/a/stock/emotion",
        "param": {
            'app': 'CailianpressWeb',
            'os': 'web',
            'sv': '7.7.5'
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

def 个股涨跌():
    # 发送 GET 请求
    response = requests.get(param_map['个股涨跌']['url'], headers=headers, params=param_map['个股涨跌']['param'])
    return json.loads(response.text)

def wencai1(query,query_type):
    cookie='other_uid=Ths_iwencai_Xuangu_s1e2xtpqi8wty9vgts3up1aeklanhmsa; ta_random_userid=s9cfw1a6ol; cid=5b58f21b2099cb8b327c3c71a9581bb01726156949; PHPSESSID=ddabea4a55168ee404f6f19e9f636e0f; wencai_pc_version=1; v=AysXlKL2yaQYXxXC3FxA3wUgukQQQG-WuUMDbZ0sBqbBh0U6JRDPEskkk2au'
    res = wencai.get(loop=True,query=query, cookie=cookie, query_type=query_type)
    return res

def convert_to_percentage(s):
    num = float(s)
    result = "{:.2f}%".format(num * 100)
    if num >= 0:
        return "+" + result
    else:
        return result

def write_大盘指数():
    markdown_content = "# 大盘\n\n"
    markdown_content += "| 指数 | 涨跌 | 点位 |\n"
    markdown_content += "| ---- | --- | --- |\n"

    data = 指数()
    zhishus = ['sh000001','sz399001','sz399006','sh000688','899050.BJ']
    for zhishu in zhishus:
        zhishu_data = data['data'][zhishu]
        markdown_content += f"| {zhishu_data['secu_name']} | {convert_to_percentage(zhishu_data['change'])} | {zhishu_data['last_px']}\n"

    data = 个股涨跌()['data']
    markdown_content += "两市成交量  " + data['shsz_balance'] + '，'
    markdown_content += "较上日  " + data['shsz_balance_change_px'] + '\n'

    with open('output.md', 'w', encoding='utf-8') as file:
        file.write(markdown_content)

def write_行业板块():
    markdown_content = "# 热点行业概念\n\n"
    markdown_content += "## 行业流入前十\n\n"
    markdown_content += "| 行业 | 净流入  | 涨停家数 |\n"
    markdown_content += "| ---- | --- | --- | \n"

    data = wencai1('二级行业板块主力净流入前十，显示涨停家数','zhishu')

    for index,row in data.iterrows():
        money = "%.2f亿元" % (row['指数@主力资金流向[{}]'.format(formatted_date)] / 100000000)
        markdown_content += f"| {row['指数简称']} | {money} | {row['指数@涨停家数[{}]'.format(formatted_date)]} |\n"

    markdown_content += "## 行业流出前五\n\n"
    markdown_content += "| 行业 | 净流入  |\n"
    markdown_content += "| ---- | --- |\n"

    data = wencai1('二级行业板块主力净流出前五','zhishu')

    for index,row in data.iterrows():
        money = "%.2f亿元" % (row['指数@主力资金流向[{}]'.format(formatted_date)] / 100000000)
        markdown_content += f"| {row['指数简称']} | {money} |\n"

    markdown_content += "## 概念板块涨幅前十\n\n"
    markdown_content += "| 概念名称 | 涨跌幅  | 涨停家数 |\n"
    markdown_content += "| ---- | --- | --- |\n"

    data = wencai1('概念板块涨跌幅排名前十，显示涨停家数','zhishu')

    for index,row in data.iterrows():
        value = "%.2f%%" % (float(row['指数@涨跌幅:前复权[{}]'.format(formatted_date)]))
        markdown_content += f"| {row['指数简称']} | {value} | {row['指数@涨停家数[{}]'.format(formatted_date)]} |\n"    

    markdown_content += "## 概念板块跌幅前五\n\n"
    markdown_content += "| 概念名称 | 涨跌幅  |\n"
    markdown_content += "| ---- | --- |\n"

    data = wencai1('概念板块涨跌幅排名最后五个','zhishu')
    for index,row in data.iterrows():
        value = "%.2f%%" % (float(row['指数@涨跌幅:前复权[{}]'.format(formatted_date)]))
        markdown_content += f"| {row['指数简称']} | {value} |\n"

    markdown_content += "## 主力资金流入前十\n\n"
    markdown_content += "| 股票名称 | 资金流入  |\n"
    markdown_content += "| ---- | --- |\n"

    data = wencai1('主力流入前十','stock')

    for index,row in data.iterrows():
        money = "%.2f亿元" % (row['主力资金流向[{}]'.format(formatted_date)] / 100000000)
        markdown_content += f"| {row['股票简称']} | {money} |\n"    

    markdown_content += "## 主力资金流出前十\n\n"
    markdown_content += "| 股票名称 | 资金流出  |\n"
    markdown_content += "| ---- | --- |\n"

    data = wencai1('主力流出前十','stock')

    for index,row in data.iterrows():
        money = "%.2f亿元" % (row['主力资金流向[{}]'.format(formatted_date)] / 100000000)
        markdown_content += f"| {row['股票简称']} | {money} |\n"        

    with open('output.md', 'a', encoding='utf-8') as file:
        file.write(markdown_content)    

def write_连板天梯():
    markdown_content = "# 涨停复盘\n\n"

    chuangye_data = wencai1('今日创业板涨停,非ST','stock')
    kechuang_data = wencai1('今日科创板涨停,非ST','stock')
    beijiao_data = wencai1('今日北交所涨停,非ST','stock')
    zhuban_data = wencai1('今日主板涨停,非ST','stock')

    if chuangye_data is None:
        markdown_content += "今日创业板涨停0家，"
    else:    
        markdown_content += "今日创业板涨停{}家，".format(len(chuangye_data))
    
    if kechuang_data is None:
        markdown_content += "科创板涨停0家，"
    else:    
        markdown_content += "科创板涨停{}家，".format(len(kechuang_data))
    
    if beijiao_data is None:
        markdown_content += "北交所涨停0家，"
    else:    
        markdown_content += "北交所涨停{}家，".format(len(beijiao_data))
    
    if zhuban_data is None:
        markdown_content += "主板涨停0家。"
    else:    
        markdown_content += "主板涨停{}家。\n".format(len(zhuban_data))

    markdown_content += "## 连板天梯\n\n"
    markdown_content += "| 连续涨停天数 | 股票名称  | 最终涨停时间 | 涨停原因 |\n"
    markdown_content += "| ---- | --- | --- | --- |\n"

    data = wencai1('连板天梯，非ST，显示涨停原因，显示涨停时间','stock')

    for index,row in data.iterrows():
        markdown_content += f"| {row['连续涨停天数[{}]'.format(formatted_date)]} | {row['股票简称']} | {row['最终涨停时间[{}]'.format(formatted_date)]}  | {row['涨停原因类别[{}]'.format(formatted_date)]} |\n"  

    markdown_content += "## 今日首板\n\n"
    markdown_content += "| 股票名称  | 最终涨停时间 | 涨停原因 |\n"
    markdown_content += "| ---- | --- | --- |\n"

    data = wencai1('今日首板，非ST，按首次涨停时间排序，显示涨停原因','stock')

    for index,row in data.iterrows():
        markdown_content += f"| {row['股票简称']} | {row['最终涨停时间[{}]'.format(formatted_date)]}  | {row['涨停原因类别[{}]'.format(formatted_date)]} |\n"  


    with open('output.md', 'a', encoding='utf-8') as file:
        file.write(markdown_content)

def write_个股涨跌():
    markdown_content = "# 个股涨跌\n\n"
    data = 个股涨跌()['data']
    up_down_data = data['up_down_dis']

    markdown_content += "## 涨跌停详情\n\n"
    markdown_content += "涨停家数  " + str(up_down_data['up_num']) + "，"
    markdown_content += "跌停家数  " + str(up_down_data['down_num']) + '，'
    markdown_content += "封板率  " + str(data['up_ratio']) + '\n'

    markdown_content += "## 涨跌详情\n\n"
    markdown_content += "上涨家数  " + str(up_down_data['rise_num']) + '，'
    markdown_content += "下跌家数  " + str(up_down_data['fall_num']) + '，'
    markdown_content += "平盘家数  " + str(up_down_data['flat_num']) + '\n'

    markdown_content += "## 涨跌幅分布\n\n"
    markdown_content += "| 幅度 | 涨幅 | 跌幅 | \n"
    markdown_content += "| ---- | --- | --- |\n"
    markdown_content += f"| 2%-4% | {str(up_down_data['up_2'])} | {str(up_down_data['down_2'])} |\n"
    markdown_content += f"| 4%-6% | {str(up_down_data['up_4'])} | {str(up_down_data['down_4'])} |\n"
    markdown_content += f"| 6%-8% | {str(up_down_data['up_6'])} | {str(up_down_data['down_6'])} |\n"
    markdown_content += f"| 8%-10% | {str(up_down_data['up_8'])} | {str(up_down_data['down_8'])} |\n"
    markdown_content += f"| 超过10% | {str(up_down_data['up_10'])} | {str(up_down_data['down_10'])} |\n"

    with open('output.md', 'a', encoding='utf-8') as file:
        file.write(markdown_content)

def write_热点榜():
    markdown_content = "# 同花顺人气前20\n\n"
    data = renqi_data = wencai1('人气榜前20，几天几板，涨停原因','stock')
    markdown_content += "| 人气榜排名 | 股票名称 | 涨跌幅 | 几天几板 | 涨停原因类别 |\n"
    markdown_content += "| ---- | --- | --- | --- | --- |\n"

    for index,row in renqi_data.iterrows():
        value = "{:.2f}%".format(float(row['最新涨跌幅']))
        jitianjiban = row['几天几板[{}]'.format(formatted_date)]
        if jitianjiban is None:
            jitianjiban = '-'

        zhangtingyuanyin = row['涨停原因类别[{}]'.format(formatted_date)]
        if zhangtingyuanyin is None:
            zhangtingyuanyin = '-'    
        markdown_content += f"| {row['个股热度排名[{}]'.format(formatted_date)]} | {row['股票简称']}  | {value} | {jitianjiban} | {zhangtingyuanyin} | \n"  


    with open('output.md', 'a', encoding='utf-8') as file:
        file.write(markdown_content)

def main():
    write_大盘指数()
    write_个股涨跌()
    write_行业板块()
    write_连板天梯()
    write_热点榜()

if __name__ == "__main__":
    main()