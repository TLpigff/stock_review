# 根据公开资料整理，不作为买卖依据

import pywencai
import pandas as pd

file_name = '复盘.csv'

def wencai(**kwargs):
    query = kwargs.get('query')
    query_type = kwargs.get('query_type','stock')
    cookie='other_uid=Ths_iwencai_Xuangu_s1e2xtpqi8wty9vgts3up1aeklanhmsa; ta_random_userid=s9cfw1a6ol; cid=5b58f21b2099cb8b327c3c71a9581bb01726156949; PHPSESSID=ddabea4a55168ee404f6f19e9f636e0f; wencai_pc_version=1; v=AysXlKL2yaQYXxXC3FxA3wUgukQQQG-WuUMDbZ0sBqbBh0U6JRDPEskkk2au'
    res = pywencai.get(query=query, cookie=cookie, query_type=query_type)
    return res

def lianban():
    wencai(query='连扳天梯，展示涨停原因，非ST')

def 上证指数():
    res = wencai(query='上证指数',query_type='zhishu')
    return res['subjects']

def 深圳成指():
    res = wencai(query='深圳成指',query_type='zhishu')
    return res['subjects']

def 创业板指():
    res = wencai(query='创业板指',query_type='zhishu')
    return res['subjects']

def write_markdown_file():
    # 读取 CSV 文件
    df = pd.read_csv('复盘.csv')

    # 创建 Markdown 表格的表头部分
    markdown_table = "| " + " | ".join(df.columns) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(df.columns)) + " |\n"

    # 添加数据行
    for _, row in df.iterrows():
        markdown_table += "| " + " | ".join(map(str, row)) + " |\n"

    # 将 Markdown 内容写入文件
    with open('output.md', 'w', encoding='utf-8') as file:
        file.write(markdown_table)

zhishu = {
    '上证指数': 上证指数,
    '深证成指': 深圳成指,
    '创业板指': 创业板指,
}
def write_大盘指数():
    markdown_content = "# 大盘指数\n\n"
    markdown_content += "| 指数 | 点位 | 涨跌 |\n"
    markdown_content += "| ---- | --- | --- |\n"

    for zhishuname, zhishufunc in zhishu.items():
        print(zhishuname)
        res = zhishufunc()
        print(res)
        for key, value in res.items():
            markdown_content += f"| {value['name']} | {value['latest_price']} | {value['rise_fall_rate']} |\n"

    with open('output.md', 'w', encoding='utf-8') as file:
     file.write(markdown_content)    

def main():
    write_大盘指数()

if __name__ == "__main__":
    main()