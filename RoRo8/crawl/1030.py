import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random
target_url = 'https://shenzhen.qfang.com'

headers = {'User-Agent': UserAgent().chrome}
with open('job.txt', 'w',encoding='utf-8') as f:
    for page in range(1, 2):
        every_page_url = target_url + '/rent/' + 'f' + str(page)
        print(f"第{page}页:{every_page_url}")
        f.write(f"第{page}页:{every_page_url}" + "\n")

        response = requests.get(every_page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        for i, (source, house) in enumerate(zip(soup.select('a.house-title.fl'), soup.select('div.house-metas')), start=1):
            titles = source['title']
            links = source['href']
            full_url = target_url + links
            house_info = ' '.join([p.get_text(strip=True) for p in house.select('p.meta-items')])
            
            print(f"第{i}个标题:{titles}\n第{i}个链接:{full_url}\n第{i}个房源信息:{house_info}")
            f.write(f"第{i}个链接：{full_url}" + '\n')
            f.write(f"第{i}个标题：{titles}" + '\n')
            f.write(f"第{i}个房源：{house_info}" + '\n')
        time.sleep(random.randint(1, 3))