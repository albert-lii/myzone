# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2020/4/15 21:38
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class SiteDescForm(FlaskForm):
    """网站描述表单"""

    body = TextAreaField(label=u"内容", validators=[DataRequired()])
    submit = SubmitField(label=u"提交")
