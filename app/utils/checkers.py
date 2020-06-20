# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/12/30 18:00
"""
import re

from wtforms.validators import HostnameValidation

from app.bp_auth.models import User


def check_username_valid(
    username: str, min_length: int = 0, max_length: int = 20
) -> bool:
    """检查用户名是否规范，用户名只能以英文字母开头，只能包含大小写字母、数字和下划线

    :param username: 用户名
    :param min_length: 用户名的最小长度
    :param max_length: 用户名的最大长度
    """
    regex = "^[a-zA-Z][a-zA-Z0-9_]{%d,%d}$" % (min_length, max_length)
    return re.match(regex, username)


def check_username_existed(username: str) -> User or None:
    """检查用户名是否已经存在

    :param username: 用户名
    """
    user = User.query.with_entities(User.id).filter_by(username=username).first()
    return True if user else False


def check_email_valid(email: str) -> bool:
    """检查邮箱是否有效，此处直接使用 wtforms.validators 中的 Email()

    :param email: 邮箱地址
    """
    if not email or "@" not in email:
        return False
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE,
    )
    user_part, domain_part = email.rsplit("@", 1)
    if not user_regex.match(user_part):
        return False
    if not HostnameValidation(require_tld=True)(domain_part):
        return False
    return True


def check_useremail_existed(email: str) -> bool:
    """检查用户邮箱是否已经存在

    :param email: 邮箱
    """
    user = User.query.with_entities(User.id).filter_by(email=email).first()
    return True if user else False


def check_password_valid(password: str, min: int = 6, max: int = 32) -> bool:
    """检查密码是否规范，密码只能以英文字母开头，只能包含大小写字母、数字和下划线

    :param password: 密码
    :param min: 密码最小长度
    :param max: 密码最大长度
    :return:
    """
    # ^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z\\W]{%d,%d}$
    # (?![0-9]+$) 排除纯数字组合
    # (?![a-zA-Z]+$) 排除纯字母组合
    # \\W 特殊字符
    regex = "^[0-9A-Za-z\\W]{%d,%d}$" % (min, max)
    return re.match(regex, password)
