# -*- coding: utf-8 -*-
# create by Aramis
import requests
from fontTools import ttLib
import re

URL_TAG1 = 'http://maoyan.com/board/6'
HEADER = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

res = requests.get(url=URL_TAG1, headers=HEADER)
if res and res.status_code == 200:
    html = res.text
    font_url = 'http:' + re.findall(re.compile('//vfile.*?.woff'), html)[0]
    print(font_url)
    if font_url:
        font_res = requests.get(font_url)
        if font_res.status_code == 200:
            with open('current.woff', 'wb') as f:
                f.write(font_res.content)
            current_woff = ttLib.TTFont('current.woff')
            # base_font_woff.s

    pass
else:
    print('访问出错', res.status_code)

# http://fontstore.baidu.com/static/editor/index.html