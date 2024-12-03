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

# ['股票代码', '股票简称', '换手率[20241203]', '涨跌幅:前复权[20241203]',
#       'a股市值(不含限售股)[20241203]', '量比[20241203]', '收盘价:不复权[20241203]',
#       '均价:不复权[20241203]', '{(}收盘价:不复权[20241203]{-}均价:不复权[20241203]{)}',
#       '上市板块', '开盘价:不复权[20241203]', '最高价:不复权[20241203]', '最低价:不复权[20241203]',
#       '振幅[20241203]', '注册地址', '经营范围', '总市值[20241203]', '所属同花顺行业',
#       '涨跌[20241203]', '成交量[20241203]', '成交额[20241203]', 'market_code',
#       'code'] 


def find():
    尾盘_data = wencai1('换手在5%-10%；涨幅在3%-5%；流通市值50-200亿；量比大于2；当前价大于在当日均价；主板和创业板，非ST；按个股热度排名从小到大排序，','stock')

    print('股票名称','量比')
    print('------ |  -----')

    for index,row in 尾盘_data.iterrows():
        print(row['股票简称'],row['量比[{}]'.format(formatted_date)])

    print('--------------------------------')


def write_尾盘():
    while True:
        find()
        time.sleep(2)

def main():
    write_尾盘()

if __name__ == "__main__":
    main()