# -*- coding: utf-8 -*-
# create by Aramis

def gogo():
    print('gogo')


import socket

# 获取本机电脑名
myname = socket.getfqdn(socket.gethostname())
# 获取本机ip
myaddr = socket.gethostbyname(myname)
print(myname)
print(myaddr)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


print(get_host_ip())
