# -*- coding: utf-8 -*-
# create by Aramis
import requests
from scrapy.selector import Selector

res = requests.get('http://ip.zxinc.org/ipquery/?ip=136.110.14.107')
print(res.status_code)
print(res.encoding)

html = res.text
if html:
    # print(html)
    selector = Selector(text=html)
    form = selector.xpath('//form[@method="get"]//tr[4]/td[2]/text()').extract_first()
    print(form)
