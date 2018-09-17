# -*- coding: utf-8 -*-
# create by Aramis

import requests
from lxml import html
import re
from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup as bs
import json
import os

# directory = os.getcwd() + 'apks'
directory = os.path.abspath(os.path.join(os.getcwd(), '..')) + '/' + 'apks'
print(os.listdir(directory))


def _get_filename(origin: str, dir):
    l = os.listdir(dir)
    fn = origin
    while fn in l:
        if '_' in fn and fn[fn.rindex('_') + 1:fn.rindex('.')].isdigit():
            n = int(fn[fn.rindex('_') + 1:fn.rindex('.')])
            fn = fn[:fn.rindex('_')] + '_%d' % (n + 1) + fn[fn.rindex('.'):]
        else:
            fn = fn[:fn.rindex('.')] + '_1' + fn[fn.rindex('.'):]

    return fn


filename = _get_filename('liuyan_2.jpg', directory)
print(3, filename)
