import requests  # 导入 requests 库，用于发送 HTTP 请求
from lxml import etree  # 从 lxml 库导入 etree，用于解析 HTML 文本
import time  # 导入 time 模块，用于执行睡眠等待
import random  # 导入 random 模块，用于生成随机数
from fake_useragent import UserAgent  # 导入 fake_useragent，用于生成随机浏览器 UA
base_url = 'https://www.xzmncy.com'  # 站点基础域名
target_url = base_url + '/list/53542/'  # 目标目录页 URL
headers = {  # 请求头字典，设置 UA 等信息
    'User-Agent' : UserAgent().chrome  # 使用随机的 Chrome UA 字符串；注意：fake_useragent 可能随机到移动端 UA（包含“Mobile”），目标站返回移动版页面导致 XPath 抽取为空，程序无输出但退出码为 0；如遇此问题可多运行几次
}  # 结束请求头定义
response = requests.get(target_url, headers=headers)  # 请求目录页，获取响应
html = etree.HTML(response.text)  # 将目录页 HTML 文本解析为可 XPath 查询的对象
links = html.xpath('//div[@id="list"]//dd/a/@href')  # 提取所有章节相对链接列表
# print(len(links))  # 调试：打印章节数量 查看是否一致
for i, link in enumerate(links, start=1):  # 遍历章节链接；enumerate(links, start=1) 会同时返回序号和元素，这里 i 为从 1 开始的章节序号（因为小说章节是从第一章开始），link 为对应的相对链接
    real_url = base_url + link  # 拼接得到小说章节的完整 URL
    print(f"开始抓取第{i}章:{real_url}")  # 提示开始抓取（此处打印的是当前章节 URL）
    response = requests.get(real_url, headers=headers)  # 请求小说章节页面
    html = etree.HTML(response.text)  # 解析小说章节页面 HTML
    title = html.xpath('//div[@class="bookname"]//h1/text()')  # 提取章节标题文本列表
    contents = html.xpath('//div[@id="htmlContent"]//text()')  # 提取章节内容的所有文本节点
    chapter_text = []  # 用于存放清洗后的段落文本
    for content in contents:  # 遍历每个文本节点
        text = content.strip()  # 去除首尾空白字符
        if text:  # 如果非空字符串
            chapter_text.append(text)  # 收集到章节内容列表中
    if chapter_text:  # 如果本章节有内容
        with open('text.txt', 'a', encoding='utf-8') as f:  # 以追加模式(a)写入到本地文件
            f.write(f"{''.join(title)}\n\n")  # 写入章节标题并空两行；''.join(title) 表示用空字符串作为分隔符，将标题列表合并为一个完整字符串
            f.write('\n'.join(chapter_text))  # 写入章节内容，按行拼接；'\n'.join(chapter_text) 表示用换行符连接列表，生成多行文本
            f.write('\n\n')  # 章节之间分隔两行 方便查看
    else:  # 如果本章节内容为空
        print(f"第{i}章内容为空")  # 控制台提示空内容
    print(f"第{i}章:{title}成功保存在text.txt")  # 提示保存结果
    time.sleep(random.randint(1, 10))  # 随机睡眠 1~10 秒，降低访问频率
