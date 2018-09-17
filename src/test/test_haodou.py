# -*- coding: utf-8 -*-
# create by Aramis
import requests
from urllib import parse
import time
import json
import hashlib

# https://facebook.github.io/react-native/img/favicon.png

# 好豆用户协议（无参）
url = 'http://m2.haodou.com/article/app/58f984940001000038d0c49c'

# http://hop.haodou.com/hop/router/rest.json?action=front.page.get
# _HOP_=%7B%22version%22%3A%221.0%22%2C%22action%22%3A%22front.page.get%22%2C%22secret_id%22%3A%225722f877e4b0d4512e3fd872%22%2C%22current_time%22%3A1535696216%2C%22sign%22%3A%22ef143dc6a253fc9e5dd44b1587e323c9%22%7D&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&id=5a221fee5b8f790590639142&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535696216&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64
# str_home_list_params = '_HOP_={"version":"1.0","action":"front.page.get","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535696216,"sign":"ef143dc6a253fc9e5dd44b1587e323c9"}&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&id=5a221fee5b8f790590639142&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535696216&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
# url_home_list_params = 'http://hop.haodou.com/hop/router/rest.json?action=front.page.get'
# res = requests.get(url)
# print(res.encoding)
# print(res.status_code)
# res.encoding = res.apparent_encoding
# print(res.text)

cc0 = '_HOP_=%7B%22version%22%3A%221.0%22%2C%22action%22%3A%22front.page.get%22%2C%22secret_id%22%3A%225722f877e4b0d4512e3fd872%22%2C%22current_time%22%3A1535696216%2C%22sign%22%3A%22ef143dc6a253fc9e5dd44b1587e323c9%22%7D&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&id=5a221fee5b8f790590639142&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535696216&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
cc1 = '_HOP_=%7B%22version%22%3A%221.0%22%2C%22action%22%3A%22front.page.get%22%2C%22secret_id%22%3A%225722f877e4b0d4512e3fd872%22%2C%22current_time%22%3A1535698064%2C%22sign%22%3A%2238b96ffbc370d27c330eda6eae3fcffe%22%7D&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&id=5b0fd473843c46147449bdf1&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535698064&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
cc2 = '_HOP_=%7B%22version%22%3A%221.0%22%2C%22action%22%3A%22platform.passport.keepalive%22%2C%22secret_id%22%3A%225722f877e4b0d4512e3fd872%22%2C%22current_time%22%3A1535699094%2C%22sign%22%3A%22576ed10a7bb972944512e8eacf9c1699%22%7D&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&device_info=%7B%22os%22%3A%22Android.6.0%22%2C%22brand%22%3A%22Letv%22%2C%22model%22%3A%22Letv+X501%22%2C%22sc_pw%22%3A1920%2C%22sc_ph%22%3A1080%2C%22sc_size%22%3A5%2C%22cpu_type%22%3A%22AArch64+Processor+rev+2+%28aarch64%29%22%2C%22cpu_frequency%22%3A2%2C%22mem_size%22%3A2726%2C%22tel_type%22%3A1%2C%22did%22%3A%22haodou868897020889812%22%7D&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535699094&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
cc3 = '_HOP_=%7B%22version%22%3A%221.0%22%2C%22action%22%3A%22front.page.get%22%2C%22secret_id%22%3A%225722f877e4b0d4512e3fd872%22%2C%22current_time%22%3A1535699100%2C%22sign%22%3A%22b6a127a68e6d05b78f0d668e7e55bd1d%22%7D&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&id=5b0fd473843c46147449bdf1&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535699100&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
cc4 = '_HOP_=%7B%22version%22%3A%221.0%22%2C%22action%22%3A%22platform.passport.keepalive%22%2C%22secret_id%22%3A%225722f877e4b0d4512e3fd872%22%2C%22current_time%22%3A1535700594%2C%22sign%22%3A%2283e9ce52204d77e2e3b3f1df42c0901f%22%7D&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&device_info=%7B%22os%22%3A%22Android.6.0%22%2C%22brand%22%3A%22Letv%22%2C%22model%22%3A%22Letv+X501%22%2C%22sc_pw%22%3A1920%2C%22sc_ph%22%3A1080%2C%22sc_size%22%3A5%2C%22cpu_type%22%3A%22AArch64+Processor+rev+2+%28aarch64%29%22%2C%22cpu_frequency%22%3A2%2C%22mem_size%22%3A2726%2C%22tel_type%22%3A1%2C%22did%22%3A%22haodou868897020889812%22%7D&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535700594&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
cc5 = '_HOP_=%7B%22version%22%3A%221.0%22%2C%22action%22%3A%22api.app.ad.daemon%22%2C%22secret_id%22%3A%225722f877e4b0d4512e3fd872%22%2C%22current_time%22%3A1535700594%2C%22sign%22%3A%22b198f3aec0013be9cc6f6abdfe05c9bb%22%7D&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535700594&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
cc6 = '_HOP_=%7B%22version%22%3A%221.0%22%2C%22action%22%3A%22api.app.ad.daemon%22%2C%22secret_id%22%3A%225722f877e4b0d4512e3fd872%22%2C%22current_time%22%3A1535700834%2C%22sign%22%3A%226ecdcb9f1b593bfa1767f7395f5cec22%22%7D&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535700834&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'

dd = parse.unquote(cc6)
print(dd)
print(int(time.time()), time.clock())

ee0 = '_HOP_={"version":"1.0","action":"front.page.get","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535696216,"sign":"ef143dc6a253fc9e5dd44b1587e323c9"}&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&id=5a221fee5b8f790590639142&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535696216&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
ee1 = '_HOP_={"version":"1.0","action":"front.page.get","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535698064,"sign":"38b96ffbc370d27c330eda6eae3fcffe"}&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&id=5b0fd473843c46147449bdf1&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535698064&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
ee2 = '_HOP_={"version":"1.0","action":"platform.passport.keepalive","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535699094,"sign":"576ed10a7bb972944512e8eacf9c1699"}&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&device_info={"os":"Android.6.0","brand":"Letv","model":"Letv+X501","sc_pw":1920,"sc_ph":1080,"sc_size":5,"cpu_type":"AArch64+Processor+rev+2+(aarch64)","cpu_frequency":2,"mem_size":2726,"tel_type":1,"did":"haodou868897020889812"}&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535699094&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
ee3 = '_HOP_={"version":"1.0","action":"front.page.get","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535699100,"sign":"b6a127a68e6d05b78f0d668e7e55bd1d"}&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&id=5b0fd473843c46147449bdf1&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535699100&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
ee4 = '_HOP_={"version":"1.0","action":"platform.passport.keepalive","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535700594,"sign":"83e9ce52204d77e2e3b3f1df42c0901f"}&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&device_info={"os":"Android.6.0","brand":"Letv","model":"Letv+X501","sc_pw":1920,"sc_ph":1080,"sc_size":5,"cpu_type":"AArch64+Processor+rev+2+(aarch64)","cpu_frequency":2,"mem_size":2726,"tel_type":1,"did":"haodou868897020889812"}&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535700594&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
ee5 = '_HOP_={"version":"1.0","action":"api.app.ad.daemon","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535700594,"sign":"b198f3aec0013be9cc6f6abdfe05c9bb"}&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535700594&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'
ee6 = '_HOP_={"version":"1.0","action":"api.app.ad.daemon","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535700834,"sign":"6ecdcb9f1b593bfa1767f7395f5cec22"}&adcode=110100&appid=2&appkey=9ef269eec4f7a9d07c73952d06b5413f&channel=ali_v6164&deviceid=haodou868897020889812&from=Letv-Letv+X501&hduid=33425365&ip=192.168.40.39&network=WIFI&osName=android&osVersion=6.0&token=MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj&ts=1535700834&uid=33425365&uuid=c79cd4c0bb49ff5059e0a66b0512a773&vc=151&virtual=1&vn=6.1.64'

md5str = 'haodoucaipu15357008345722f877e4b0d4512e3fd872'
h1 = hashlib.md5()
h1.update(md5str.encode("utf-8"))
print(h1.hexdigest())


# 576ed10a7bb972944512e8eacf9c1699
# fdbbfd5a0bb427ee7b902f7329cddb59

# j = json.loads(ee0[ee0.index('{'):ee0.index('}') + 1])
# j['current_time'] = '123'
#
# print(str(j).replace('\'', '\"'))


# print(ee0[ee0.index('{'):ee0.index('}')+1])


# 首页列表
def get_home_list():
    url_home_list_params = 'http://hop.haodou.com/hop/router/rest.json?action=front.page.get'
    dict_home_list_params = {
        '_HOP_': '{"version":"1.0","action":"front.page.get","secret_id":"5722f877e4b0d4512e3fd872","current_time":1535696216,"sign":"ef143dc6a253fc9e5dd44b1587e323c9"}',
        'adcode': 110100,
        'appid': 2,
        'appkey': '9ef269eec4f7a9d07c73952d06b5413f',
        'channel': 'ali_v6164',
        'deviceid': 'haodou868897020889812',
        'from': 'Letv-Letv+X501',
        'hduid': 33425365,
        'id': '5a221fee5b8f790590639142',
        'ip': '192.168.40.39',
        'network': 'WIFI',
        'osName': 'android',
        'osVersion': '6.0',
        'token': 'MzM0MjUzNjU6MTUzNTUyNTU5NzU5ODowOjA1MjFmNTVmZWM3NTc5MDNjN2Y1MjlhNzY0MzYyZTdj',
        'ts': '1535696216',
        'uid': '33425365',
        'uuid': 'c79cd4c0bb49ff5059e0a66b0512a773',
        'vc': '151',
        'virtual': '1',
        'vn': '6.1.64'
    }

    j = json.loads(dict_home_list_params.get('_HOP_'))
    j['current_time'] = int(time.time())

    # print(str(j).replace('\'', '\"'))
    dict_home_list_params['_HOP_'] = str(j).replace('\'', '\"')
    print(dict_home_list_params)
    res = requests.post(url=url_home_list_params, data=dict_home_list_params)
    print(res.encoding)
    print(res.status_code)
    res.encoding = res.apparent_encoding
    print(res.text)

# get_home_list()
