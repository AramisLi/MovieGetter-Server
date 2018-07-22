# -*- coding: utf-8 -*-
# create by Aramis
import json

CODE_DB = 500
CODE_PARAMS = 501
CODE_LOGIC = 502
CODE_OTHER = 503


def success(result: None, extra: None):
    return _public_return(200, 'success', result, extra)


def fail(code: int, msg: str, extra: None):
    return _public_return(code, msg, None, extra)


def fail_default(code: int):
    error_str = {
        CODE_DB: '数据库错误',
        CODE_PARAMS: '参数错误',
        CODE_LOGIC: '逻辑错误',
        CODE_OTHER: '其他错误'
    }
    return _public_return(code, error_str.get(code, 'fail'), None, None)


def _public_return(code: int, msg: str, result: None, extra: None):
    return json.dumps({'code': code, 'msg': msg, 'result': result, 'extra': extra})
