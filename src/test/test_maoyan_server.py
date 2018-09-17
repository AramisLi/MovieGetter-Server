# -*- coding: utf-8 -*-
# create by Aramis
import requests
import hashlib
import time
import json

time_stamp = int(time.time())
hl = hashlib.md5()
hl.update(str('我是大帅哥' + str(time_stamp)).encode(encoding='utf-8'))
sign = hl.hexdigest()
date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

params = {'sign': sign, 'time_stamp': time_stamp, 'tag': 0, 'page_num': 0, 'page_size': 10, 'date': date}
print('params', params)
res = requests.get('http://localhost:5001/maoyan/board', params=params)
# print(res.text.encode('utf-8').decode('utf-8'))
print(res.encoding)
res.encoding=res.apparent_encoding
print(res.text)

hour = int(time.strftime('%H', time.localtime(time.time())))
# date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# if hour < 12:
#     date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 3600))

date = time.strftime('%Y-%m-%d', time.localtime((time.time() - 24 * 3600) if hour < 10 else time.time()))

print('date', date)
