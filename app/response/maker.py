# -*- coding:utf-8 -*-
"""
    响应生成工具文件

    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/12/20 15:13 
"""
from flask import jsonify
from .status import Status


class Response(object):
    def __init__(self, code: int, msg: str, data=None):
        self._code = code
        self._msg = msg
        self._data = data

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg

    @property
    def data(self):
        return self._data

    def to_dict(self):
        return {"code": self._code, "msg": self._msg, "data": self._data}

    def to_json(self):
        return jsonify(self.to_dict())


def make_response(code: int, msg: str, data) -> Response:
    """生成响应

    :param code: 响应码
    :param msg: 响应信息
    :param data: 响应内容
    :return: 响应字典对象
    """
    return Response(code, msg, data)


def make_response_ok(msg: str = None, data=None) -> Response:
    """生成成功的响应

    :param msg: 响应信息
    :param data: 响应内容
    :return: 成功的响应字典对象
    """
    if msg is None:
        msg = Status.OK.msg
    return make_response(Status.OK.code, msg, data)


def make_response_error(status: Status = Status.FAIL, data=None) -> Response:
    """生成错误的响应

    :param status: 错误状态
    :param data: 错误内容
    :return: 错误的响应字典对象
    """
    return make_response(status.code, status.msg, data)
