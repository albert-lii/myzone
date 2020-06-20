# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2019/11/21 21:39
"""
import arrow
from flask_login import UserMixin

from app.db.model import BaseModel
from app.extensions import db


class Role(db.Model, BaseModel):
    """用户角色表"""

    __tablename__ = "mz_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id，主键，自增
    name = db.Column(db.String(32), nullable=False)  # 用户角色名称
    desc = db.Column(db.String(64), nullable=False)  # 用户角色描述
    create_time = db.Column(
        db.BigInteger, nullable=False, default=arrow.utcnow().timestamp
    )  # 用户角色创建时间
    update_time = db.Column(db.BigInteger)  # 用户角色最近一次的更新时间


class User(db.Model, UserMixin, BaseModel):
    """用户表"""

    __tablename__ = "mz_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id，主键，自增
    username = db.Column(db.String(64), nullable=False)  # 用户名
    password = db.Column(db.String(64), nullable=False)  # 密码
    email = db.Column(db.String(128), nullable=False)  # 邮箱
    personal_site = db.Column(db.String(128))  # 个站的地址
    avatar_url = db.Column(db.String(255))  # 用户头像图片的名称
    create_time = db.Column(
        db.BigInteger, nullable=False, default=arrow.utcnow().timestamp
    )  # 用户创建时间
    login_time = db.Column(db.BigInteger)  # 上一次的登录时间
    update_time = db.Column(db.BigInteger)  # 专栏最近一次的更新时间

    role_id = db.Column(
        db.Integer, db.ForeignKey("mz_role.id", ondelete="CASCADE")
    )  # 用户角色id，外键，
    role = db.relationship(
        "Role", backref=db.backref("users", lazy="dynamic", passive_deletes=True)
    )  # 用户角色数据，父级删除，子级不受影响

    @classmethod
    def query_by_name(cls, username: str):
        """根据用户名查询指定用户信息

        :param username: 用户名
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def query_by_email(cls, email: str):
        """根据邮箱查询指定用户信息

        :param email: 邮箱
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def query_by_account(cls, account: str):
        """根据用户账号查询指定用户信息

        :param account: 用户名/邮箱
        """
        user = cls.query_by_name(account)
        if not user:
            return cls.query_by_email(account)
        return user

    def update_login_time(self):
        """更新最近一次的登录时间"""
        self.login_time = arrow.utcnow().timestamp
        db.session.commit()
