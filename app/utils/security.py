# -*- coding:utf-8 -*-
"""
    签名与加密工具文件

    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/12/20 10:54 
"""
import base64
import hashlib
import os
import random

SALT_LENGTH = 16  # 盐值长度
ITERATION_NUM = 10  # 加密迭代次数


def encrypt_md5(s):
    """md5 加密"""
    new_md5 = hashlib.md5()  # 创建 md5 对象
    # 这里必须用 encode() 函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding="utf-8"))
    # 加密
    return new_md5.hexdigest()


def encrypt_password(password: str, salt: bytes = None, dklen: int = None) -> bytes:
    """加密用户密码

    :param password: 明文密码
    :param salt: 盐值
    :param dklen: 密文密码长度
    :return: base64 格式的密文密码
    """
    if salt is None:
        salt = os.urandom(SALT_LENGTH)  # 随机生成 salt

    assert len(salt) == SALT_LENGTH  # 判断盐值的长度是否为16位，如果不是则抛出异常
    assert isinstance(salt, bytes)  # 判断盐值是否是字节类型，如果不是字节则抛出异常
    assert isinstance(password, str)  # 判断密码是否是字符串类型，如果不是字符串则抛出异常

    if isinstance(password, str):
        # 如果 password 是 str 类型，则将 password 转为 bytes 类型
        password = password.encode("utf-8")

    assert isinstance(password, bytes)  # 判断编码后的密码是否是字节类型，如果是字节则抛出异常

    dk = hashlib.pbkdf2_hmac(
        "sha256", password, salt, ITERATION_NUM, dklen
    )  # 选择 SHA256 算法，使用 HMAC 对密码和 salt 进行 10 次叠代加密混淆
    result = salt + dk
    return base64.b64encode(result).decode()


def validate_password(encrypted_password, password: str) -> bool:
    """验证密码是否正确

    :param encrypted_password: 密文密码
    :param password: 明文密码
    :return True: 密码正确  False: 密码错误
    """
    pw_bytes = base64.b64decode(encrypted_password)
    return encrypted_password == encrypt_password(password, salt=pw_bytes[:SALT_LENGTH])


def generate_randint_captcha(captcha_length: int = 6) -> str:
    """随机生成 6 位数字验证码

    :param captcha_length: 验证码长度
    """
    captcha = ""
    for i in range(captcha_length):
        captcha += str(random.randint(0, 9))
    return captcha
