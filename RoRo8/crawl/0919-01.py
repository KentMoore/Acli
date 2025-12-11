import requests
from fake_useragent import UserAgent
def xixi(url):
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
        filename = f"{keyword}_page_{i + 1}.html"  # 使用关键词和页码命名
        with open("./output/html/" + filename, 'w',encoding='UTF-8') as f:
            f.write(r.text)
        print(f"第{i + 1}页下载成功，保存为：{filename}")
xixi('https://tieba.baidu.com/f')
