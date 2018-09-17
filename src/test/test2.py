# -*- coding: utf-8 -*-
# create by Aramis
import requests

url = 'http://www.xfyy166.com'
url1 = 'http://www.4422N.com'
url2 = 'http://www.yyxfxf.com'

res = requests.get(url)
print(res.status_code)
print(res.encoding)

try:
    text = res.text.encode('ISO-8859-1').decode('GBK')
    print('go go go')
    print(text)
except:
    print('no no no')
    print(res.text)
