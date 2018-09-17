# -*- coding: utf-8 -*-
# create by Aramis
import requests
from scrapy.selector import Selector

url1 = 'https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9286217699096966359%22%7D&n_type=0&p_from=1'
url2 = 'http://ip.zxinc.org/ipquery/?ip=136.110.14.107'
url3 = 'http://www.guangyuanol.cn/news/newspaper/2018/0803/884834.html'
url4 = 'http://www.xfa50.com/view/index41538.html'  # 1的detail
# url4 = 'http://www.xfa50.com/pic/uploadimg/2018-8/2018838212380983.jpg'
url5 = 'http://www.xfa50.com/list/index3.html'
url6 = 'http://www.xfa50.com/view/index41524.html'  # 2的detail
url7 = 'http://www.xfa50.com/view/index40243.html'  # 3的detail

url8 = 'http://www.xfyy166.com'
url9 = 'http://www.xfyy166.com/toupai/'
url10 = 'http://www.xfyy166.com/toupai/2018-8/104972.html'
url11 = 'http://www.xfyy166.com/toupai/2018-8/104972/player.html?104972-0-0'
url12 = 'http://www.xfyy166.com/playdata/12/104972.js'

url13 = 'http://www.xfyy166.com/html/picture1'
url14 = 'http://www.xfyy166.com/html/picture1/131642/'
url15 = 'http://www.xfyy166.com/html/picture4/152683/'

url16 = 'http://www.ssssbb.com'
url17 = 'http://www.ssssbb.com/html/part/index15.html'
url18 = 'http://www.ssssbb.com/html/article/index7626.html'

url20 = 'http://www.ssssbb.com/yyxf/index1.html'
url21 = 'http://www.ssssbb.com/movie/index33063.html'
url25 = 'http://www.ssssbb.com/yyxfplay/33063-1-0.html'

url26='https://imageking.eu/images/n668aczmz.jpg'

index = 1
url = url26
res = requests.get(url)
print(res.status_code)
print(res.encoding)
print(res.apparent_encoding)
res.encoding = res.apparent_encoding


def savePic():
    if '.jpg' in url:
        pic_name = url[url.rindex('/') + 1:]
        print(pic_name)
        with open(pic_name, 'wb') as f:
            f.write(res.content)

    else:
        print(res.text)


savePic()

if index == 1:
    pass
elif index == 2:
    pass
