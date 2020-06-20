# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/12/30 18:00
"""

from wtforms.validators import ValidationError

from app.utils.checkers import check_username_valid, check_password_valid
from app.utils.security import encrypt_md5


class UserNameValidator(object):
    """自定义用户名校验器"""

    def __init__(
        self,
        min_length: int = 1,
        max_length: int = 20,
        err_none: str = None,
        err_min: str = None,
        err_max: str = None,
        err_informal: str = None,
    ):
        assert 0 < min_length <= max_length
        if err_none is None:
            err_none = u"用户名不能为空"
        if err_min is None:
            err_min = u"用户名长度不能小于%d位" % min_length
        if err_max is None:
            err_max = u"用户名长度不能超过%d位" % max_length
        if err_informal is None:
            err_informal = u"用户名只能以字母开头，可以包含大小写字母、数字和下划线"
        self.min_length = min_length
        self.max_length = max_length
        self.err_none = err_none
        self.err_min = err_min
        self.err_max = err_max
        self.err_informal = err_informal

    def __call__(self, form, field):
        data: str = field.data
        if not data or len(data) == 0:
            # 用户名为空，抛出错误
            raise ValidationError(message=self.err_none)
        if len(data) < self.min_length:
            # 用户名长度小于最小限制，抛出错误
            raise ValidationError(message=self.err_min)
        if len(data) > self.max_length:
            # 用户名长度超过最大限制，抛出错误
            raise ValidationError(message=self.err_max)
        if not check_username_valid(data, self.min_length, self.max_length):
            # 用户名不规范，抛出错误
            raise ValidationError(message=self.err_informal)


class PasswordValidator(object):
    """自定义密码校验器"""

    def __init__(
        self,
        min_length: int = 6,
        max_length: int = 32,
        err_none: str = None,
        err_min: str = None,
        err_max: str = None,
        err_informal: str = None,
    ):
        assert 0 < min_length <= max_length
        if err_none is None:
            err_none = u"密码不能为空"
        if err_min is None:
            err_min = u"密码长度不能小于%d位" % min_length
        if err_max is None:
            err_max = u"密码长度不能超过%d位" % max_length
        if err_informal is None:
            err_informal = u"密码只能包含大小写字母、数字和特殊字符"
        self.min_length = min_length
        self.max_length = max_length
        self.err_none = err_none
        self.err_min = err_min
        self.err_max = err_max
        self.err_informal = err_informal

    def __call__(self, form, field):
        data: str = field.data
        if not data or len(data) == 0:
            # 密码为空，抛出错误
            raise ValidationError(message=self.err_none)
        if len(data) < self.min_length:
            # 密码长度小于最小限制，抛出错误
            raise ValidationError(message=self.err_min)
        if len(data) > self.max_length:
            # 密码长度超过最大限制，抛出错误
            raise ValidationError(message=self.err_max)
        if not check_password_valid(data):
            # 密码不规范，抛出错误
            raise ValidationError(message=self.err_informal)
        # 密码传输前，用 md5 加密一下，防止明文传输
        field.data = encrypt_md5(data)
