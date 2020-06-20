# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2020 Albert Li
    :time: 2020/1/14 11:33 
"""
from threading import Thread

from flask import current_app
from flask_mail import Message

from app.extensions import mail


def _send_async_mail(app, message: Message):
    """异步发送邮件"""
    # 异步发送将开启一个新的线程, 执行上下文已经不在 app 内, 必须使用 with 语句进入 app 上下文才可以执行 mail 对象
    with app.app_context():
        mail.send(message)


def send_mail(
    to: list, title: str, mail_html: str = None, mail_body: str = None
) -> Thread:
    """发送邮件

    :param to: 收信人的邮箱地址列表
    :param title: 邮件的标题
    :param mail_html: html 格式的邮件内容
    :param mail_body: 纯文本的邮件内容，收信人会优先读取 html，如果邮件系统不支持，再读取 body
    """
    app = current_app._get_current_object()  # 获取原始的 app 实例
    message = Message(title, recipients=to)
    message.html = mail_html
    message.body = mail_body
    thr = Thread(target=_send_async_mail, args=[app, message])  # 异步发送邮件
    thr.start()
    return thr


def send_register_mail(to: str, captcha: str) -> Thread:
    """用户注册时，发送的验证码邮件

    :param to: 收信人的邮箱地址
    :param captcha: 验证码
    """
    return send_mail(
        [to],
        u"iGank 用户注册验证码",
        u'<p>您正在进行【iGank】的用户注册操作，您的验证码是<b style="font-size:1.5rem;color:#1F58B6;"> {captcha}</b>，10分钟内有效。</p>'.format(
            captcha=captcha
        ),
        u"您正在进行【iGank】的用户注册操作，您的验证码是 {captcha}，10分钟内有效".format(captcha=captcha),
    )


def send_forgetpwd_mail(to: str, captcha: str) -> Thread:
    """忘记密码时，发送的验证码邮件

    :param to: 收信人的邮箱地址
    :param captcha: 验证码
    """
    return send_mail(
        [to],
        u"iGank 忘记密码验证码",
        u'<p>您正在进行【iGank】的忘记密码操作，您的验证码是<b style="font-size:1.5rem;color:#1F58B6;"> {captcha}</b>，10分钟内有效。</p>'.format(
            captcha=captcha
        ),
        u"您正在进行【iGank】的忘记密码操作，您的验证码是 {captcha}，10分钟内有效".format(captcha=captcha),
    )
