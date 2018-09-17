# -*- coding: utf-8 -*-
# create by Aramis
import os

from flask import Flask, g, request, send_from_directory, make_response

import server_return
from module_mysql import MysqlClient
from hashlib import md5
from my_controller import MyController
import time

__all__ = ['app']
app = Flask(__name__)


def client():
    if not hasattr(g, 'client'):
        g.client = MysqlClient()
    return g.client


def get_maoyan_control():
    if not hasattr(g, 'maoyan_control'):
        g.maoyan_control = MyController()
    return g.maoyan_control


@app.route('/index', methods=['GET'])
def test():
    return '我是大帅哥'


@app.route('/create_user', methods=['POST'])
def create_user():
    role = None
    usable = None
    name = None
    if 'root_imei' in request.form:
        root_imei = request.form['root_imei']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)
    if 'imei' in request.form:
        imei = request.form['imei']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)
    if 'role' in request.form:
        role = request.form['role']
    if 'usable' in request.form:
        usable = request.form['usable']
    if 'name' in request.form:
        name = request.form['name']

    return client().create_user(root_imei, imei, role, usable, name)


@app.route('/get_role', methods=['POST'])
def get_role():
    # print(type(request.args), request.args)
    if 'imei' in request.form:
        imei = request.form.get('imei')
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)
    return client().select_role(imei)


@app.route('/mark_in', methods=['POST'])
def mark_in():
    print(request.form)
    if 'imei' in request.form:
        imei = request.form['imei']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, "imei")
    if 'login_time' in request.form:
        login_time = request.form['login_time']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, "login_time")
    local = request.form.get('local', None)
    ip = request.form.get('ip', None)
    version_code = request.form.get('version_code', None)
    version_name = request.form.get('version_name', None)

    return client().mark_in(imei, login_time, local, ip, version_code, version_name)


@app.route('/mark_in_ip', methods=['POST'])
def mark_in_ip():
    ip = request.form.get('ip', None)
    mark_id = request.form.get('mark_id', None)
    if not ip:
        return server_return.server_error(server_return.ERROR_PARAMS, "ip")
    if not mark_id:
        return server_return.server_error(server_return.ERROR_PARAMS, "mark_id")
    return client().mark_in_ip(ip, mark_id)


@app.route('/mark_out', methods=['POST'])
def mark_out():
    if 'logout_time' in request.form:
        logout_time = request.form['logout_time']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)
    if 'mark_id' in request.form:
        mark_id = request.form['mark_id']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)

    return client().mark_out(mark_id, logout_time)


@app.route('/mark_movie', methods=['POST'])
def mark_movie():
    if 'imei' in request.form:
        imei = request.form['imei']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, 'imei')
    if 'movieId' in request.form:
        movie_id = request.form['movieId']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, 'movieId')
    if 'movieName' in request.form:
        movie_name = request.form['movieName']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, 'movieName')
    if 'downloaded_time' in request.form:
        downloaded_time = request.form['downloaded_time']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, 'downloaded_time')
    if 'downloaded_timestamp' in request.form:
        downloaded_timestamp = request.form['downloaded_timestamp']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, 'downloaded_timestamp')

    return client().mark_movie(imei, movie_id, movie_name, downloaded_time, downloaded_timestamp)


def get_post_params(param_name: str):
    if 'logout_time' in request.form:
        logout_time = request.form['logout_time']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)


@app.route('/download/apk', methods=['GET'])
def download_apks():
    # directory = '../apks'
    directory = os.getcwd()[0:-2] + 'apks'
    print(directory)
    # response=make_response(send_from_directory(directory,'test_file.txt',as_attachment=True))
    # response.headers['']='attachment; filename={}'.format(file_name.encode())
    # dirpath = os.path.join(app.root_path, 'apks')
    # print(dirpath)
    # return send_from_directory(directory, 'test_file.txt')

    response = make_response(send_from_directory(directory, 'test_file.txt', as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(
        'test_file.txt'.encode().decode('latin-1'))

    print(response)
    return response


def _check_sign(params):
    b = False
    if 'sign' in params and 'time_stamp' in params and params.get('sign', None) == _get_sign(
            params.get('time_stamp', None)):
        b = True
    return b


@app.route('/download/<string:filename>', methods=['GET'])
def download_file(filename):
    print(request.args)
    print(dict(request.args))

    if _check_sign(request.args):
        print('go go go')
        directory = os.path.abspath(os.path.join(os.getcwd(), '..')) + '/' + 'apks'
        b = os.path.isfile(directory + '/' + filename)
        print(b)
        if b:
            response = make_response(send_from_directory(directory, filename, as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                filename.encode().decode('latin-1'))
            return response

    return server_return.server_error(server_return.ERROR_PARAMS)


@app.route('/pic/<string:filename>', methods=['GET'])
def show_pic(filename):
    directory = os.path.abspath(os.path.join(os.getcwd(), '..')) + '/' + 'apks'
    f = directory + '/' + filename
    b = os.path.isfile(f)
    if b:
        image_f = open(f, 'rb')
        image_data = image_f.read()
        image_f.close()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    return server_return.server_success({'b': b})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files and 'sign' in request.form and 'time_stamp' in request.form:
        if request.form.get('sign', None) == _get_sign(request.form.get('time_stamp', None)):
            directory = os.path.abspath(os.path.join(os.getcwd(), '..')) + '/' + 'apks'
            file = request.files['file']
            print(file, type(file))
            file.save(directory + '/' + _get_filename(file.filename, directory))

            return server_return.server_success({'m': '上传成功'})
        else:
            return server_return.server_error(server_return.ERROR_SIGN)
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)


def _get_filename(origin: str, dirr):
    l = os.listdir(dirr)
    fn = origin
    while fn in l:
        if '_' in fn and fn[fn.rindex('_') + 1:fn.rindex('.')].isdigit():
            n = int(fn[fn.rindex('_') + 1:fn.rindex('.')])
            fn = fn[:fn.rindex('_')] + '_%d' % (n + 1) + fn[fn.rindex('.'):]
        else:
            fn = fn[:fn.rindex('.')] + '_1' + fn[fn.rindex('.'):]

    return fn


# 检查MG版本
@app.route('/check_version', methods=['POST'])
def check_version():
    version_code = request.form.get('version_code', None)
    version_name = request.form.get('version_name', None)
    if version_code and version_name:
        return client().check_version(int(version_code), version_name)
    else:
        return server_return.server_error(server_return.ERROR_DB)


# 爬取猫眼电影排行榜
@app.route('/maoyan/board')
def maoyan_board():
    sign = request.args.get('sign', None)
    tag = request.args.get('tag', 0)
    page_num = request.args.get('page_num', 1)
    page_size = request.args.get('page_size', 10)
    time_stamp = request.args.get('time_stamp', 0)

    print(time_stamp, int(time.time()))
    if sign and time_stamp:
        hl = md5()
        hl.update(('我是大帅哥' + time_stamp).encode(encoding='utf-8'))
        mm = hl.hexdigest()
        print('sign:{sign},mm:{mm}'.format(sign=sign, mm=mm))
        if sign == mm:
            j = get_maoyan_control().get_data(tag=tag, page_num=page_num, page_size=page_size)
            return server_return.server_success(j)
        else:
            return server_return.server_error(server_return.ERROR_PARAMS)
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)


def _get_sign(time_stamp):
    hl = md5()
    hl.update(('我是大帅哥' + time_stamp).encode(encoding='utf-8'))
    mm = hl.hexdigest()
    return mm


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
