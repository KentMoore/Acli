import requests
from fake_useragent import UserAgent
from lxml import etree
import time
import random
from concurrent.futures import ThreadPoolExecutor
base_url = 'https://www.xzmncy.com'
url = base_url + '/list/53542/'
headers = {
    'User-Agent' : UserAgent().chrome,
}
response = requests.get(url, headers=headers)
html = etree.HTML(response.text)
links = html.xpath('//div[@id="list"]//dd/a/@href')
print(len(links)) # 判断是否获取到对应数量的链接
# 定义下载单个章节的函数
def getchapter(i, link):
    target_url = base_url + link
    print(f"开始抓取第{i}章:{target_url}")
    response = requests.get(target_url, headers=headers)
    html = etree.HTML(response.text)
    title = html.xpath('//div[@class="bookname"]//h1/text()')
    contents = html.xpath('//div[@id="htmlContent"]//text()')
    chapter_text = []
    for content in contents:
        text = content.strip()
        if text:
            chapter_text.append(text)
    time.sleep(random.randint(1, 10))
    if chapter_text:
        return (i, title, chapter_text)
    else:
        print(f"第{i}章内容为空")
        return (i, None, None)
# 使用线程池下载所有章节
chapters = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(getchapter, i, link) for i, link in enumerate(links, start=1)]
    for future in futures:
        i, title, chapter_text = future.result()
        if title and chapter_text:
            chapters[i] = (title, chapter_text)
# 按顺序写入文件
for i in sorted(chapters.keys()):
    title, chapter_text = chapters[i]
    with open('txt02.txt', 'a', encoding='utf-8') as f:
        f.write(f"{''.join(title)}\n\n")
        f.write('\n'.join(chapter_text))
        f.write('\n\n')
    print(f"第{i}章:{title}成功保存在txt02.txt")
