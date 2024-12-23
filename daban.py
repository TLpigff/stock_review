# 根据公开资料整理，不作为买卖依据

import wencai
import pandas as pd
import time
import datetime

current_date = datetime.datetime.now()
#current_date = current_date - datetime.timedelta(days=1)
formatted_date = current_date.strftime('%Y%m%d')

def wencai1(query,query_type):
    cookie='other_uid=Ths_iwencai_Xuangu_s1e2xtpqi8wty9vgts3up1aeklanhmsa; ta_random_userid=s9cfw1a6ol; cid=5b58f21b2099cb8b327c3c71a9581bb01726156949; PHPSESSID=ddabea4a55168ee404f6f19e9f636e0f; wencai_pc_version=1; v=AysXlKL2yaQYXxXC3FxA3wUgukQQQG-WuUMDbZ0sBqbBh0U6JRDPEskkk2au'
    res = wencai.get(loop=True,query=query, cookie=cookie, query_type=query_type)
    return res

def convert_to_percentage(s):
    num = float(s)
    result = "{:.2f}%".format(num)
    if num >= 0:
        return "+" + result
    else:
        return result

yestoday_stocks = {}
stocks = {}

def find_yestoday():
    liuru_data = wencai1('昨日主力资金流入前50','stock')
    renqi_data = wencai1('人气榜前50','stock')

    liuru_stocks = {}

    for index,row in liuru_data.iterrows():
        liuru_stocks[row['股票简称']] = row['最新涨跌幅']

    for index,row in renqi_data.iterrows():
        if row['股票简称'] in liuru_stocks.keys():
            yestoday_stocks[row['股票简称']] = row['最新涨跌幅']

    print("昨日主力流入前50且今日人气榜前50\n")

    for key,value in yestoday_stocks.items():
        print(key,convert_to_percentage(value))    

    print('--------------------------------')    

def find():
    liuru_data = wencai1('主力资金流入前50','stock')
    renqi_data = wencai1('人气榜前50','stock')

    liuru_stocks = {}

    for index,row in liuru_data.iterrows():
        liuru_stocks[row['股票简称']] = "%.2f亿元" % (row['主力资金流向[{}]'.format(formatted_date)] / 100000000)

    for index,row in renqi_data.iterrows():
        if row['股票简称'] in liuru_stocks.keys():
            if row['股票简称'] not in stocks.keys():
                print('新加入的股票',row['股票简称'], convert_to_percentage(row['最新涨跌幅']),liuru_stocks[row['股票简称']])    
                stocks[row['股票简称']] = {"涨幅":row['最新涨跌幅'],"流入": liuru_stocks[row['股票简称']]}

    print('--------------------------------')


def write_连板天梯():
    find_yestoday()
    find()
    count = 0
    while True:
       find()
       count += 1
       if count == 5:
        count = 0
        for key,value in stocks.items():
            print(key,convert_to_percentage(value['涨幅']),value['流入'])

def main():
    write_连板天梯()

if __name__ == "__main__":
    main()