# -*- coding:utf-8 -*-
"""
    文章模块的相关表单
    ~~~~~~~~~~~~~~~~~

    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/12 21:13
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm):
    cover = FileField(label=u"封面")
    title = StringField(label=u"标题", validators=[DataRequired(), Length(1, 100)])
    channel = SelectField(label=u"专栏", coerce=int, default=1)
    category = SelectField(label=u"分类", coerce=int, default=1)
    tags = StringField(label=u"标签")
    body = TextAreaField(label=u"内容", validators=[DataRequired()])
    save = SubmitField(label=u"私密保存")
    publish = SubmitField(label=u"发布文章")
