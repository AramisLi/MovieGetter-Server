# -*- coding: utf-8 -*-
# create by Aramis
import time
import pymysql
import requests

a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print(a)

# HOST = '180.76.190.163'
# pymysql.connect(host=HOST, user='root', password='uu@5!uacqr!qGZly', database='',
#                 port=3306, chartset='utf8')

response = requests.get('http://cupertino.nextra.homes.co.jp/Code/MasterApp.json?code=area_addr11_sorted')
print(response.status_code)
print(response.text)
