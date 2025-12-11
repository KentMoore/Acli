import requests
from lxml import etree

all_data = []

for i in range(1, 51):
    real_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
    print(f"正在爬第 {i} 页: {real_url}")

    res = requests.get(real_url, timeout=5)
    if res.status_code != 200:
        print(f"第 {i} 页返回状态码 {res.status_code}，停止。")
        break

    res.encoding = res.apparent_encoding
    html = etree.HTML(res.text)

    books = html.xpath("//article[contains(@class, 'product_pod')]")
    print(f"第 {i} 页找到 {len(books)} 本书")

    for b in books:
        title = b.xpath("normalize-space(.//h3/a/@title)")
        price = b.xpath("normalize-space(.//p[contains(@class, 'price_color')]/text())")
        availability = b.xpath("normalize-space(.//p[contains(@class, 'instock')])")

        all_data.append({
            "title": title,
            "price": price,
            "availability": availability
        })

print("总共抓到：", len(all_data), "本书")
for item in all_data:
    print(item)
