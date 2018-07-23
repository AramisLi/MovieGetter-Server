# -*- coding: utf-8 -*-
# create by Aramis
import os

from flask import Flask, g, request, send_from_directory, make_response

import server_return
from module_mysql import MysqlClient

__all__ = ['app']
app = Flask(__name__)


def client():
    if not hasattr(g, 'client'):
        g.client = MysqlClient()
    return g.client


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
    local = None
    ip = None
    print(request.form)
    if 'imei' in request.form:
        imei = request.form['imei']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, "imei")
    if 'login_time' in request.form:
        login_time = request.form['login_time']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS, "login_time")
    # if 'local' in request.form:
    # local = request.form['local']
    # if 'ip' in request.form:
    #     ip = request.form['ip']
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
def download_aps():
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


@app.route('/check_version', methods=['POST'])
def check_version():
    version_code = request.form.get('version_code', None)
    version_name = request.form.get('version_name', None)
    if version_code and version_name:
        return client().check_version(int(version_code), version_name)
    else:
        return server_return.server_error(server_return.ERROR_DB)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
