# -*- coding: utf-8 -*-
# create by Aramis
import requests
from scrapy.selector import Selector
from fontTools import ttLib
import re
import test.test_maoyan_font_xml

# http://fontstore.baidu.com/static/editor/index.html
URL_TAG1 = 'http://maoyan.com/board/6'
HEADER = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

ocr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

res = requests.get(url=URL_TAG1, headers=HEADER)
# print(res.text)
if res and res.status_code == 200:
    html = res.text
    # with open('test_maoyan_font_woff.html', 'w', encoding='utf-8') as f:
    #     f.write(html)
    font_url = 'http:' + re.findall(re.compile('//vfile.*?.woff'), html)[0]
    print('字体地址', font_url)

    selector = Selector(text=html)
    l = selector.xpath('//dd//p[@class="realtime"]//span[@class="stonefont"]').extract()
    # for i in l:
    #     print(str(i))
    # class ="realtime" > 实时票房: <
    #
    #
    #     span > < span
    #
    #
    # class ="stonefont" >
    print(l[0])
    realtimes = re.findall(re.compile('realtime.*?stonefont\">(.*?)</span>'), html)
    print('realtimes', realtimes)
    total_boxoffice = re.findall(re.compile('total-boxoffice.*?stonefont\">(.*?)</span>'), html)
    print('total_boxoffice', total_boxoffice)
    if font_url:
        font_res = requests.get(font_url)
        if font_res.status_code == 200:
            with open('current.woff', 'wb') as f:
                f.write(font_res.content)

            font = ttLib.TTFont('current.woff')
            cmap = font['cmap']
            cmap_dict = cmap.getBestCmap()
            # print(cmap_dict)
            glyf_list = list(font['glyf'].keys())
            # print(glyf_list)

            mydict = dict((k, v.strip()) for k, v in zip(glyf_list, ocr))
            # print('mydict',mydict)

            # writer=open('current.xml', 'w')
            # font.toXML(writer,)
            font.saveXML('current.xml')
            r_l=test.test_maoyan_font_xml.parse_woff_simple('current.xml')
            print('r_l',r_l)

    pass
else:
    print('访问出错', res.status_code)
