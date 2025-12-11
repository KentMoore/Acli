import requests
from fake_useragent import UserAgent
url = 'https://img3.doubanio.com/view/group_topic/l/public/p699540277.webp'


headers_values = {
        'User-Agent':UserAgent().random,

}

r = requests.get(url,headers = headers_values)

with open('','wb') as f:
    f.write(r.content)
    print("Download Successfully")

