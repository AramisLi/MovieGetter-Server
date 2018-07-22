# -*- coding: utf-8 -*-
# create by Aramis
import re
import requests

a = 2 + 2
print(a)
base_url = 'http://www.xfa50.com'
cnm = '/js/ads/caonimei.js'
res = requests.get(base_url)
print(res.encoding)
try:
    res_str = res.text.encode('ISO-8859-1').decode('gbk')
    print(res_str)
except:
    print(res.text)
    f = re.findall('<b>(www.*?)</b>', res.text)[0]
    print(f)
