from concurrent.futures import ThreadPoolExecutor

import requests
import json
import os
import time
from lxml import etree

base_url = 'https://www.qishuxia.com' # 将小说官网定义为基础网址
target_url = base_url + '/book/1/' # 将基础网址加上需爬取小说网址的后缀 并定义为目标网址

# 将设备信息放在函数外，为全局变量
headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Referer' : 'https://www.qishuxia.com/book/1/',
    'Cookie' : 'PHPSESSID=1jo0h286gtb9pet7pkg5fi017d'
}

# 定义获取小说的章节的标题和链接，并以json格式储存在一个json文件里
def getJson(url):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    # 使用xpath获取小说章节标题
    result01 = html.xpath('//div[@class="section-box"]//li/a/text()')
    # 使用xpath获取小说章节链接
    result02 = html.xpath('//div[@class="section-box"]//li/a/@href')
    # 新建一个空列表储存小说章节标题和链接
    data = []
    # 遍历所有章节和标题，并使用zip()函数打包成元组
    for title, link in zip(result01, result02):
        data.append(
            {
                'title' : title,
                'link' : target_url + link
            }
        )
    # 新建一个data.json文件，存放小说的所有章节标题和链接 需导入json库
    with open('./output/json/data02.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{len(data)}条数据保存在./output/json/data02.json中")


# 定义下载函数，直接被主函数调用
def downLoadSingleChapter(i, chapter, total):
    # 从章节获取标题和链接
    title = chapter['title']
    link = chapter['link']
    # 自定义文件名，并指定下载的txt文件的存放位置
    filename = os.path.join('./output/txt', f"{i + 1:04d}_{title}.txt")
    try:
        # 每0.5秒发送一次请求
        time.sleep(0.5)
        response = requests.get(link, headers=headers, timeout=5)
        html = etree.HTML(response.text)

        # 使用xpath获取小说章节的具体内容
        content = html.xpath('//div[@id="content" and @class="content"]//text()')

        # 判断内容是否为空
        if content:
            # 去除多余的符号以及空格
            cleaned_lines = [line.strip() for line in content if line.strip()]
            cleaned_content = '\n'.join(cleaned_lines)
            # 写入下载的文件
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{title}\n\n")
                f.write(cleaned_content)
            print(f"{i+1}/{total} 下载成功 {title}")
        else:
            print(f"{i+1}/{total} 内容为空 {title}")
    # 捕获请求超时异常
    except requests.Timeout:
        print(f"请求超时 {title}")
    # 捕获其他异常
    except Exception as e:
        print(f"[{i+1}/{total}] 下载失败 {title} - {str(e)}")

# 主函数
def main():
    # 读取保存的data02.json文件
    with open('./output/json/data02.json', 'r', encoding='utf-8') as f:
        # 将所有章节和链接赋值给chapters
        chapters = json.load(f)
    print(f"开始下载{len(chapters)}个章节")

    # 使用多线程下载，设置最大线程数为5
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 创建任务列表存储所有线程任务
        futures = []
        # 遍历所有章节，提交下载任务到线程池
        for i, chapter in enumerate(chapters):
            future = executor.submit(downLoadSingleChapter, i, chapter, len(chapters))
            futures.append(future)
        # 等待所有下载任务完成
        for future in futures:
            future.result()
    print(f"{len(chapters)}个章节下载完成")
if __name__ == '__main__':
    if not os.path.exists('./output/json/data02.json'):
        getJson(target_url)
    main()