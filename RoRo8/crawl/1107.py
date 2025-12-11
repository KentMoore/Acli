import requests
import csv
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random

target_url = 'https://shenzhen.qfang.com'

headers = {'User-Agent': UserAgent().chrome}
csv_filename = 'houses-data.csv'
csv_header = ['标题', '户型', '面积', '装修', '楼层', '出租方式', '朝向', '电梯配备', '租金', '小区', '地址']

with open(csv_filename, 'w', encoding='utf-8-sig', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(csv_header)

    for page in range(1, 100):
        every_page_url = target_url + '/rent/' + 'f' + str(page)
        print(f"正在爬取第{page}页:{every_page_url}")
        response = requests.get(every_page_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        houses = soup.select('.list-result li')

        for i, house in enumerate(houses, start=1):
            row_data = [''] * 11  # 初始化11个字段

            allINeed = house.select_one('a.house-title.fl')
            if allINeed:
                titles = allINeed.get_text(strip=True) 
                row_data[0] = titles  # 标题
                print(f"第{i}个: {titles}")

            text_div = house.select_one('div.text.fl.clearfix')
            if text_div:
                community = text_div.select_one('a')
                if community:
                    row_data[9] = community.get_text(strip=True)  # 小区
                full_text = ' '.join(text_div.get_text().split())
                addr_text = full_text.replace(row_data[9], '').strip()
                row_data[10] = addr_text  # 地址

            price_elem = house.select_one('p.bigger')
            if price_elem:
                row_data[8] = price_elem.get_text(strip=True)  # 租金

            meta_elems = house.select('p.meta-items')
            for idx, meta in enumerate(meta_elems):
                if idx < 7:
                    row_data[idx + 1] = meta.get_text(strip=True)

            csv_writer.writerow(row_data)

        time.sleep(random.randint(1, 3))