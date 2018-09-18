# -*- coding: utf-8 -*-
# create by Aramis
import requests
import time
from hashlib import md5
import os
import sys
from contextlib import closing
from utils.progress import ProgressBar

print(os.getcwd()[0:-4])

if not os.getcwd()[0:-4] + 'utils' in sys.path:
    sys.path.append(os.getcwd()[0:-4] + 'utils')
    print('append')

if 'ttt' not in sys.modules:
    ttt = __import__('ttt')
    print('import')
else:
    eval('import ttt')
    ttt = eval('reload(ttt)')
    print('eval')

ttt.gogo()


def _get_sign(time_stamp):
    hl = md5()
    hl.update(('我是大帅哥' + time_stamp).encode(encoding='utf-8'))
    mm = hl.hexdigest()
    return mm


def _get_params():
    t = int(time.time())
    return {
        'time_stamp': t,
        'sign': _get_sign(str(t))
    }


def upload_file(ip='192.168.40.6'):
    upload_url = 'http://{ip}:5001/upload'.format(ip=ip)
    upload_path = '/Users/lizhidan/Documents/Project/PythonProject/MovieGetter-Server/src/test/moviegetter-v1.3-test.apk'

    files = {
        'file': open(upload_path, 'rb')
    }

    res = requests.post(url=upload_url, data=_get_params(), files=files)
    return res.text


def download_file(filename: str, ip='192.168.40.6'):
    download_url = 'http://{ip}:5001/download'.format(ip=ip)
    res = requests.get(download_url + '/{}'.format(filename), params=_get_params())
    if res and res.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(res.content)

    return res.text


# print(download_file('moviegetter-v1.3-test.apk', '180.76.190.163'))
# print(upload_file('180.76.190.163'))


def download_file_progress(filename: str, ip='192.168.40.6'):
    download_url = 'http://{ip}:5001/download'.format(ip=ip)
    with closing(requests.get(download_url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        print('content_size', content_size)
        progress = ProgressBar(filename, total=content_size,
                               unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        with open(filename, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))


# download_file_progress('moviegetter-v1.3-test.apk', '180.76.190.163')

def upload_apk(ip='192.168.40.6'):
    upload_url = 'http://{ip}:5001/upload/apk'.format(ip=ip)
    upload_path = '/Users/lizhidan/Documents/Project/AndroidProject/MovieGetter/app/release/moviegetter-v1.3-test.apk'

    files = {
        'file': open(upload_path, 'rb')
    }
    params = {
        'version_code': 5,
        'version_name': '1.5',
        'is_current': 1,
        'is_force': 1,
        'message': '就是这么帅'
    }
    res = requests.post(url=upload_url, data=dict(_get_params(), **params), files=files)
    return res.text


def check_version(ip='192.168.40.6'):
    url = 'http://{ip}:5001/check_version'.format(ip=ip)
    res = requests.get(url=url, params=_get_params())
    return res.text


print(upload_apk())
# print(check_version())
