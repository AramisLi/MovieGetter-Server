# -*- coding: utf-8 -*-
# create by Aramis

import re


d1={
    'a':1,
    'b':2
}

d2={
    'c':3,
    'd':4
}

d3=dict(d1,**d2)

print(d3)
