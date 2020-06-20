# -*- coding:utf-8 -*-
"""
    手动往数据库中添加信息，初始化一些不怎么变动的表中的信息

    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/12/18 16:12
"""
from app.extensions import db
from app.bp_main.models import SiteDesc
from app.bp_work.models import Channel, Category
from app.bp_auth.models import Role, User


def add_data(obj):
    db.session.add(obj)


def commit_data():
    db.session.commit()


def generate_role():
    """初始化用户角色表的信息"""
    add_data(Role(name="NormalUser", desc="普通用戶"))
    add_data(Role(name="Author", desc="网站作者"))
    add_data(Role(name="Admin", desc="管理员"))
    commit_data()


def generate_admin():
    """初始化管理员表的信息"""
    add_data(
        User(
            username="李益",
            password="bJWB+AVv6vuoYBX/9QIdnNOjuxUnUBDa1novL09mRtBU8L7aRUmSUxX1j9xgZJva",
            email="albertlii@163.com",
            role_id=3,
        )
    )


def generate_article_channel():
    """初始化文章专栏表的信息"""
    add_data(Channel(name="技术杂谈"))
    add_data(Channel(name="生活有道"))
    commit_data()


def generate_article_category():
    """初始化文章分类表的信息"""
    # 技术杂谈专栏的分类
    add_data(Category(name="技术杂谈", channel_id=1))
    add_data(Category(name="Android", channel_id=1))
    add_data(Category(name="Python", channel_id=1))
    add_data(Category(name="Kotlin", channel_id=1))
    add_data(Category(name="前端", channel_id=1))
    add_data(Category(name="小程序", channel_id=1))
    add_data(Category(name="Linux", channel_id=1))
    add_data(Category(name="数据库", channel_id=1))

    # 生活有道专栏的分类
    add_data(Category(name="生活有道", channel_id=2))
    add_data(Category(name="职场杂谈", channel_id=2))

    commit_data()


def generate_site_desc():
    """初始化网站描述表的信息"""
    add_data(SiteDesc(body="关于"))
    commit_data()
