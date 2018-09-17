# -*- coding: utf-8 -*-
# create by Aramis

import requests
import json

b = True

while b:
    a = input()
    print(a)

    if a.isdigit():

        page = int(a)
        url = 'https://api.github.com/search/repositories?q=Android&sort=starts&page={page}'.format(page=page)
        res = requests.get(url)
        text = res.text
        # print(text)
        j = json.loads(text)

        for i in j['items']:
            print(i['owner']['avatar_url'])
    else:
        if a is 'q' or a is 'quit':
            b = False
        else:
            print('请输入数字，输入q退出')
