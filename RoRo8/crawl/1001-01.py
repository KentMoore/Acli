import requests
from lxml import etree
import json
import os
def downloadFile():
    url = 'https://www.xzmncy.com/list/55379/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0'
    }
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    result01 = html.xpath('//div[starts-with(@id,"list")]//dd/a/text()')
    result02 = html.xpath('//div[starts-with(@id,"list")]//dd/a/@href')
    data = []
    for title, link in zip(result01, result02):
        data.append({
            'title': title,
            'link': 'https://www.xzmncy.com' + link
        })
    with open('./output/json/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到 data.json,共 {len(data)} 条记录")
def downloadChapters():
    with open('./output/json/data.json', 'r', encoding='utf-8') as f:
        chapters = json.load(f)
    print(f"开始下载 {len(chapters)} 个章节...")
    for i, chapter in enumerate(chapters, 1):
        title = chapter['title']
        link = chapter['link']
        filename = os.path.join("./output/txt/", f"{i:04d}_{title}.txt")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0'}
            response = requests.get(link, headers=headers)
            response.encoding = 'utf-8'
            html = etree.HTML(response.text)
            content = html.xpath('//div[@id="htmlContent"]//text()')
            if content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"{title}\n\n")
                    f.write(''.join(content))
                print(f"[{i}/{len(chapters)}] 下载成功: {title}")
            else:
                print(f"[{i}/{len(chapters)}] 内容为空: {title}")
        except Exception as e:
            print(f"[{i}/{len(chapters)}] 下载失败: {title} - {str(e)}")
    print("\n下载完成!")
if __name__ == '__main__':
    if not os.path.exists('./output/json/data.json'):
        downloadFile()
    downloadChapters()
