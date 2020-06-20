# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2020/4/15 21:30
"""
import arrow

from app.db.model import BaseModel
from app.extensions import db


class Banner(db.Model, BaseModel):
    """banner表"""

    __tablename__ = "mz_banner"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )  # id，主键，
    desc = db.Column(db.String(64))  # banner描述
    image_url = db.Column(db.String(255))  # 图片链接
    link_url = db.Column(db.String(255))  # 跳转链接
    create_time = db.Column(
        db.BigInteger, nullable=False, index=True, default=arrow.utcnow().timestamp
    )  # 文章创建时间
    update_time = db.Column(db.BigInteger)  # 最近一次的更新时间
    is_used = db.Column(db.Integer, default=0)  # 是否在使用中，0-不在使用 1-使用中

    @classmethod
    def query_used(cls):
        """查询正在使用中的banner """
        return cls.query.filter_by(is_used=1).all()


class SiteDesc(db.Model, BaseModel):
    """网站说明表"""

    __tablename__ = "mz_site_desc"
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )  # id，主键，自增
    body = db.Column(db.Text, nullable=False)  # markdown格式的文章内容
    create_time = db.Column(
        db.BigInteger, nullable=False, index=True, default=arrow.utcnow().timestamp
    )  # 文章创建时间
    update_time = db.Column(db.BigInteger)  # 文章最近一次的更新时间
