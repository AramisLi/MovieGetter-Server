# -*- coding: utf-8 -*-
# create by Aramis
from flask import Flask, g, request

import server_return
from module_mysql import MysqlClient

__all__ = ['app']
app = Flask(__name__)


def client():
    if not hasattr(g, 'client'):
        g.client = MysqlClient()
    return g.client


@app.route('/', methods=['GET'])
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


@app.route('/get_role', methods=['GET'])
def get_role():
    print(type(request.args), request.args)
    if 'imei' in request.args:
        imei = request.args.get('imei')
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)
    return client().select_role(imei)


@app.route('/mark_in', methods=['POST'])
def mark_in():
    local = None
    ip = None
    if 'imei' in request.form:
        imei = request.form['imei']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)
    if 'login_time' in request.form:
        login_time = request.form['login_time']
    else:
        return server_return.server_error(server_return.ERROR_PARAMS)
    if 'local' in request.form:
        local = request.form['local']
    if 'ip' in request.form:
        ip = request.form['ip']

    return client().mark_in(imei, login_time, local, ip)


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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
