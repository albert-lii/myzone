# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2020/4/13 17:31
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired, Length

from app.utils.wtf_validators import PasswordValidator


class AvatarForm(FlaskForm):
    """头像表单"""

    avatar = FileField(label=u"更换头像")
    avatar_submit = SubmitField(label=u"更换")


class UserNameForm(FlaskForm):
    """昵称表单"""

    username = StringField(label=u"修改用户名",
                           validators=[DataRequired(message="用户名不能为空"), Length(1, 64, message="用户名长度为1-64位")])
    username_submit = SubmitField(label=u"修改")


class PasswordForm(FlaskForm):
    """密码表单"""

    password = PasswordField(
        label=u"重置密码", validators=[PasswordValidator(err_informal=u"密码格式错误")]
    )
    password_submit = SubmitField(label=u"重置")


class PersonalSiteForm(FlaskForm):
    """个站表单"""

    personal_site = StringField(label=u"修改个人站点")
    personal_site_submit = SubmitField(label=u"修改")
