# -*- coding: utf-8 -*-
# create by Aramis
import json

ERROR_PERMISSION_DE = 401
ERROR_PARAMS = 402
ERROR_LOGIC = 403
ERROR_DB = 501


def _get_error_str(code: int):
    switch = {
        ERROR_PERMISSION_DE: '没权限',
        ERROR_PARAMS: '参数错误',
        ERROR_LOGIC: '逻辑错误',
        ERROR_DB: '数据库错误'
    }
    return switch.get(code, 'gg')


def server_error(code: int, extra: str = None):
    d = {'code': code, 'msg': _get_error_str(code), 'extra': extra}
    return json.dumps(d)


def server_success(obj, extra: str = None):
    d = {'code': 200, 'msg': 'success', 'extra': extra, 'result': obj}
    print(d)
    return json.dumps(d)
