
import requests
from fake_useragent import UserAgent
url = 'https://tieba.baidu.com/f'
keyword = input("请输入要下载的内容：")
page = int(input("请输入要下载多少页: "))
for i in range(0, page):
    values = {
        'kw': keyword,
        'ie': 'utf-8',
        'pn': str(i * 50),
    }
    headers = {
        'User-Agent': UserAgent().random,
    }
    r = requests.get(url, params=values, headers=headers)
    print(f"第{i + 1}页: {r.url}")
    print(r.status_code)
    filename = f"job02page{i + 1}.html"
    with open(filename, 'wb') as f:
        f.write(r.content)
    print(f"第{i + 1}页下载成功")