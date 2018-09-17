# -*- coding: utf-8 -*-
# create by Aramis

import requests

url = 'http://maoyan.com/board/4?offset=0'
url_detail='http://maoyan.com/films/1203'
header = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

res = requests.get(url=url, headers=header)
print(res.status_code)
print(res.encoding)
print(res.headers)

# res.encoding = res.apparent_encoding
print(res.text)


