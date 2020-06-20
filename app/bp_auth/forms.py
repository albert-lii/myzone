# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 9:44 
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length

from app.utils.wtf_validators import UserNameValidator, PasswordValidator


class LoginForm(FlaskForm):
    """登录表单"""

    account = StringField(label=u"账号", validators=[DataRequired(message=u"账号不能为空")])
    password = PasswordField(
        label=u"密码", validators=[PasswordValidator(err_informal=u"密码格式错误")]
    )
    remember_me = BooleanField(label=u"记住我")
    submit = SubmitField(label=u"登录")


class RegisterForm(FlaskForm):
    """注册表单"""

    username = StringField(
        label=u"用戶名", validators=[DataRequired(message=u"用户名不能为空"), Length(1, 64, message="用户名长度为1-64位")]
    )
    email = StringField(
        label=u"邮箱",
        validators=[DataRequired(message=u"邮箱不能为空"), Email(message=u"邮箱地址无效")],
    )
    captcha = IntegerField(
        label=u"邮箱验证码", validators=[DataRequired(message=u"验证码不能为空")]
    )
    site = StringField(label=u"个人站点", )
    password = PasswordField(label=u"密码", validators=[PasswordValidator()])
    submit = SubmitField(label=u"注册")


class ForgetPwdForm(FlaskForm):
    """忘记密码表单"""

    email = StringField(
        label=u"邮箱",
        validators=[DataRequired(message=u"邮箱不能为空"), Email(message=u"邮箱地址无效")],
    )
    captcha = IntegerField(
        label=u"邮箱验证码", validators=[DataRequired(message=u"验证码不能为空")]
    )
    password = PasswordField(label=u"密码", validators=[PasswordValidator()])
    submit = SubmitField(label=u"确定")
