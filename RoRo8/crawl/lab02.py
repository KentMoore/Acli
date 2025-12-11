import requests
from lxml import etree
from fake_useragent import UserAgent
import time
import csv
import random

# 使用提供的Cookie
cookies = {
    'clientId': '8f5b76cfc86f152ed997d18ea3242b58',
    'TDC_itoken': '1087558056%3A1763387440',
    'game': '730',
    'acw_tc': '2ff617a117640385434833268edea3ba71a8a26a92366168127fe2eb14',
    'cdn_sec_tc': '2ff617a117640385434833268edea3ba71a8a26a92366168127fe2eb14',
    'userLanguage': 'zh-CN',
    'Hm_lvt_5992affa40e9ccff6f8f8af8d6b6cb13': '1763387426,1763433740,1764039833',
    'HMACCOUNT': 'A79F4D18A88F1815',
    'loginToken': '86641ccf-2d65-4190-a190-c085d4f39e37',
    'refreshToken': '05f80d16-b52f-4795-8943-3111fa420f8b',
    'Hm_lpvt_5992affa40e9ccff6f8f8af8d6b6cb13': '1764039928'
}

headers = {
    'User-Agent': UserAgent().chrome,
    'Referer': 'https://www.ecosteam.cn/',
}

session = requests.Session()
session.headers.update(headers)
session.cookies.update(cookies)

# 创建CSV文件
with (open('goods_data02.csv', 'w', newline='', encoding='utf-8-sig') as csvfile):
    writer = csv.writer(csvfile)
    writer.writerow(['名称', '在售价格', '在售数量'])  # 写入表头

    page = 1
    total_goods = 0
    empty_page_count = 0  # 新增：连续无数据页数计数器
    # 目标网址有1585页，现在仅爬取前100页作为案例
    while page <= 100:
        target_url = f"https://www.ecosteam.cn/market/730-1-0-0-0-0-{page}-a-b-0.html"
        print(f"正在爬第 {page} 页: {target_url}")

        response = session.get(target_url, timeout=20)
        html = etree.HTML(response.text)

        goods = html.xpath('//div[@class="goods"]')
        if not goods:
            empty_page_count += 1  # 无数据，计数器+1
            print(f"第{page}页没有商品数据（连续空页：{empty_page_count}）")
            if empty_page_count >= 5:  # 连续5页无数据，停止爬取
                print("连续5页无商品数据，停止爬取")
                break
        else:
            empty_page_count = 0  # 有数据则重置计数器
            page_goods = len(goods)
            total_goods += page_goods
            print(f"第{page}页找到 {page_goods} 个商品 (总计: {total_goods})")

            for good in goods:
                name = good.xpath('.//div[@class="goodsname"]/a/@title')[0] if good.xpath('.//div[@class="goodsname"]/a/@title') else ''
                price = good.xpath('.//span[@class="price"]/text()')[0] if good.xpath('.//span[@class="price"]/text()') else ''
                number = good.xpath('.//span[@class="number"]/text()')[0] if good.xpath('.//span[@class="number"]/text()') else ''

                # 写入CSV
                writer.writerow([name, price, number])
                print(f"{name} - {price} - {number}")
        page += 1
        time.sleep(random.randint(1, 3))
print(f"总共获取了 {total_goods} 条商品数据")
print(f"数据已保存到 goods_data.csv 文件")