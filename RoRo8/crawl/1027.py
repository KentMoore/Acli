import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random

target_url = 'https://shenzhen.qfang.com'
headers = {'User-Agent': UserAgent().chrome}
# 使用 'with' 语句打开（或创建）一个名为 'output.txt' 的文件
# 'w' 模式表示写入（会覆盖原有内容），encoding='utf-8' 确保支持中文
with open('job.txt', 'w', encoding='utf-8') as f:
    for i in range(1, 100):
        # 构造每一页的完整URL
        every_page_url = target_url + '/rent/' + 'f' + str(i)
        # 向文件中写入当前页码和URL
        f.write(f"                              第{i}页:{every_page_url}\n")
        response = requests.get(every_page_url, headers=headers)
        # 使用BeautifulSoup和'lxml'解析器解析返回的HTML文本
        soup = BeautifulSoup(response.text, 'lxml')
        # 使用CSS选择器 '.list-result li' 选取所有房源的列表项 (li)
        houses = soup.select('.list-result li')  # 获取所有房源
        # 遍历当前页面获取到的所有房源信息
        # enumerate(houses, start=1) 会同时提供索引（从1开始）和房源项
        for index, house in enumerate(houses, start=1):
            # 写入房源分隔符和序号
            f.write(f"{'-' * 50}房源{index}{'-' * 70}\n")
            # 选取房源标题的 'a' 标签
            title = house.select_one('a.house-title')
            # 检查是否成功找到了标题
            if title:
                # 获取 'href' 属性，即房源详情页的相对链接
                href = title['href']  # 获取链接
                full_url = target_url + href
                f.write(f"                      链接: {full_url}\n")
                # 获取标题的文本内容，strip=True 去除首尾空白
                title_text = title.get_text(strip=True)  # 获取标题
                f.write(f"                      标题: {title_text}\n")
            # 选取小区名称的 'a' 标签
            community = house.select_one('[class="house-location clearfix"] a')  # 获取小区
            if community:
                community_text = community.text.strip()
                f.write(f"                      小区: {community_text}\n")
            # 选取包含位置信息的 'div' 标签（取第1个），并获取文本、去除首尾空白
            location = house.select('[class="house-location clearfix"] div')[0].text.strip()  # 获取地址
            # 清理位置信息中的多余空白（例如换行符和多余空格）
            location_cleaned = ' '.join(location.split())
            # 如果前面成功获取了小区信息
            if community:
                # 从清理后的位置信息中移除小区名称和连字符，得到更纯粹的地址
                address = location_cleaned.replace(community.text.strip(), '').replace('-', '').strip()
                f.write(f"                      位置: {address}\n")
            # 选取包含房源详细信息（户型、面积等）的所有 'p' 标签
            house_metas = house.select('[class="house-metas clearfix"] p')  # 获取房源信息
            # 定义一个标签列表，用于对应房源信息的各个 'p' 标签
            labels = ['户型', '面积', '装修', '楼层', '出租方式', '朝向', '配备电梯']
            # 遍历所有获取到的房源信息 'p' 标签
            for i, item in enumerate(house_metas):
                # 获取 'p' 标签的文本并去除首尾空白
                meta_text = item.text.strip()
                # 根据索引从 labels 列表中获取对应的标签名，如果索引超出列表范围，则使用'信息'
                label = labels[i] if i < len(labels) else '信息'
                f.write(f"                      {label}: {meta_text}\n")
            price = house.select_one('span.amount')
            if price:
                price_text = price.get_text(strip=True)
                f.write(f"                      价格: {price_text}元/月\n")
        time.sleep(random.randint(1, 3))
