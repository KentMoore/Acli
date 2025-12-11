import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random

target_url = 'https://www.baidu.com'
headers = {'User-Agent': UserAgent().chrome}

response = requests.get(target_url, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

titles = soup.find_all('span', class_='title-content-title')
print(len(titles))
for title in titles:
    print(title.get_text(strip=True))
    time.sleep(random.randint(1,3))

