# -*- coding: utf-8 -*-
# create by Aramis
import re
import requests

url1 = 'http://www.xfa78.com/list/index1.html'
url2 = 'http://www.xo52.com'
url3 = 'http://www.54xfw.com'
url4 = 'http://www.xfyy166.com/toupai/index2.html'
url5 = 'http://www.xfyy166.com/toupai/2018-8/105078.html'
url6 = 'http://www.xfyy166.com/toupai/2018-8/105078/player.html?105078-0-0'
url7 = 'http://www.xfyy166.com/playdata/118/105078.js?79943.38'
url8 = 'http://www.xfa50.com'
url9 = 'http://www.xfa50.com/js/ads/caonimei.js'
url10 = 'http://www.xfa50.com/list/index1.html'
url11 = 'http://www.xfa50.com/view/index28322.html'

res = requests.get(url11)
res.encoding = res.apparent_encoding
print(res.text)

# video_json = '''var VideoListJson=[['xfplay',['\u7B2C1\u96C6$xfplay://dna=meMcD0IbmeDZDHAfDZpWmxHXDHAbDxiXDGLZEwi0mda1AGL2D0m0ED|dx=177263274|mz=\u9152\u5E97\u5927\u621898\u5E74\u6E05\u7EAF\u5C0F\u5E08\u59B9,\u4E0D\u6562\u592A\u5927\u58F0\u53EB\u6015\u9694\u58C1\u6295\u8BC9,\u4E0D\u592A\u8010\u64CD\u641E\u5B8C\u540E\u53C8\u4ECB\u7ECD\u62A4\u58EB\u73ED\u6027\u611F\u6F02\u4EAE\u5C0F\u5E08\u59B9\u7B2C\u4E8C\u5929\u7ED9\u6211\u64CD!_onekeybatch.mp4|zx=nhE0pdOVl3P5mF5xqzD5Ac5wo206BGa4mc94MzXPozS|zx=nhE0pdOVl3Ewpc5xqzD4AF5wo206BGa4mc94MzXPozS$xfplay']]],urlinfo='http://'+document.domain+'/toupai/2018-8/105078/player.html?105078-<from>-<pos>';'''
# video_json = '''var VideoListJson=
# [['xfplay',
# ['\u7B2C1\u96C6$xfplay://dna=meMcD0IbmeDZDHAfDZpWmxHXDHAbDxiXDGLZEwi0mda1AGL2D0m0ED|dx=177263274|mz=\u9152\u5E97\u5927\u621898\u5E74\u6E05\u7EAF\u5C0F\u5E08\u59B9,\u4E0D\u6562\u592A\u5927\u58F0\u53EB\u6015\u9694\u58C1\u6295\u8BC9,\u4E0D\u592A\u8010\u64CD\u641E\u5B8C\u540E\u53C8\u4ECB\u7ECD\u62A4\u58EB\u73ED\u6027\u611F\u6F02\u4EAE\u5C0F\u5E08\u59B9\u7B2C\u4E8C\u5929\u7ED9\u6211\u64CD!_onekeybatch.mp4|zx=nhE0pdOVl3P5mF5xqzD5Ac5wo206BGa4mc94MzXPozS|zx=nhE0pdOVl3Ewpc5xqzD4AF5wo206BGa4mc94MzXPozS$xfplay']]],urlinfo='http://'+document.domain+'/toupai/2018-8/105078/player.html?105078-<from>-<pos>';'''
#
# q = re.findall(re.compile("\'(.*?)\'"), video_json)
# print(q)
