# -*- coding:utf-8 -*-
"""
    响应体的状态码

    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/12/20 15:18 
"""
import enum


class Status(enum.Enum):
    OK = 0, "请求成功"
    FAIL = -1, "请求失败"

    # 1 开头的错误码分配给文件上传功能
    ERROR_FILE_NOTFOUND = 1001, "未找到文件"
    ERROR_FILE_OVERSIZE = 1002, "文件大小不得超过2M"

    # 4 开头的错误码分配给 auth 模块
    ERROR_INVALID_USERNAME = 4001, "用户名只能以英文字母开头，只能包含大小写字母、数字和下划线"
    ERROR_USERNAME_EXISTED = 4002, u"该用户名已被使用，请选用其他名称"
    ERROR_INVALID_EMAIL = 4003, u"邮箱地址无效"
    ERROR_EMAIL_EXISTED = 4004, u"该邮箱已被使用，请选用其他邮箱"

    # 5 开头的错误码分配给 work 模块
    ERROR_INVALID_LIKE_ACTION = 5001, u"喜欢操作的action值无效"

    def __init__(self, code: int, msg: str):
        self._code = code
        self._msg = msg

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg
