import requests #导入requests模块
from fake_useragent import UserAgent
from bs4 import BeautifulSoup                  #导入BeautifulSoup模块
url = 'https://shenzhen.qfang.com/rent' #定义url字符串
headersvalue = {
    'User-Agent':UserAgent().chrome
}
#发送请求，并将返回结果赋值给r
r = requests.get(url,headers=headersvalue)
#创建BeautifulSoup对象，并设置使用lxml解析器
soup = BeautifulSoup(r.text, features='lxml')
#获取第一个class属性值为'items clearfix'的li节点，包含第一个租房信息
house = soup.select('.list-result li')[0]
#获取第一个房源信息，包括户型、面积、装修、楼层和出租方式
#赋值给house_metas
house_metas=house.select('[class="house-metas clearfix"] p')
for item in house_metas:                         #遍历
    print(item.text.strip())                     #输出第一个房源信息
#获取第一个房源租金，并赋值给list_price
list_price=house.select('[class="list-price"] span')
# 输出第一个房源租金
print(list_price[0].string + list_price[1].string)
