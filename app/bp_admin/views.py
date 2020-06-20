# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :author: Albert Li
    :time: 2020/3/13 12:21 
"""
from flask import url_for, redirect, request
from flask_admin import AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from jinja2 import Markup

from app.bp_auth.models import Role, User
from app.bp_main.models import Banner
from app.bp_work.models import Channel, Category, Article, Tag, Comment, Like
from app.extensions import admin, db
from app.utils.times import timestamp_to_str


class AuthModelView(ModelView):
    def is_accessible(self):
        """判断用户是否已登录，并且是否是管理员来决定用户是否能访问后台管理系统"""
        return current_user.is_authenticated and current_user.role_id == 3

    def inaccessible_callback(self, name, **kwargs):
        """如果身份验证不通过，则重定向到登录页面"""
        return redirect(url_for("auth.login", next=request.url))


class RoleView(AuthModelView):
    """角色视图"""

    column_labels = {
        "id": u"ID",
        "name": u"角色名称",
        "desc": u"角色描述",
        "create_time": u"创建时间",
        "update_time": u"修改时间",
    }

    # 格式化字段值
    column_formatters = {
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "update_time": lambda v, c, m, p: timestamp_to_str(
            m.update_time, "YYYY-MM-DD HH:mm:ss"
        ),
    }

    def __init__(self):
        super(RoleView, self).__init__(Role, db.session, name="角色")


class UserView(AuthModelView):
    """用户视图"""

    can_view_details = True
    column_searchable_list = ["username", "email"]

    # 将列名替换为指定中文
    column_labels = {
        "id": u"ID",
        "username": u"用户名",
        "email": u"邮箱",
        "personal_site": u"个站地址",
        "avatar_url": u"头像",
        "create_time": u"创建时间",
        "update_time": u"修改时间",
        "login_time": u"上次登录",
        "role_id": u"角色",
    }

    # 格式化字段值
    column_formatters = {
        "avatar_url": lambda v, c, m, p: Markup('<img src="%s" />' % m.avatar_url),
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "update_time": lambda v, c, m, p: timestamp_to_str(
            m.update_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "login_time": lambda v, c, m, p: timestamp_to_str(
            m.login_time, "YYYY-MM-DD HH:mm:ss"
        ),
    }

    def __init__(self):
        super(UserView, self).__init__(User, db.session, name="用戶")


class BannerView(AuthModelView):
    """banner视图"""

    column_labels = {
        "id": u"ID",
        "desc": u"描述",
        "image_url": u"图片链接",
        "link_url": u"跳转链接",
        "create_time": u"创建时间",
        "update_time": u"修改时间",
        "is_used": u"是否使用",
    }

    column_formatters = {
        "image_url": lambda v, c, m, p: Markup('<img src="%s" />' % m.image_url),
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "update_time": lambda v, c, m, p: timestamp_to_str(
            m.update_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "is_used": lambda v, c, m, p: "未使用" if m.is_used == 0 else "使用中",
    }

    column_exclude_list = []

    def __init__(self):
        super(BannerView, self).__init__(
            Banner, db.session, name="banner", category="banner"
        )


class BannerFileView(FileAdmin):
    """banner文件上传视图"""

    def is_accessible(self):
        """判断用户是否已登录，并且是否是管理员来决定用户是否能访问后台管理系统"""
        return current_user.is_authenticated and current_user.role_id == 3

    def inaccessible_callback(self, name, **kwargs):
        """如果身份验证不通过，则重定向到登录页面"""
        return redirect(url_for("auth.login", next=request.url))

    def __init__(self, app):
        super(BannerFileView, self).__init__(
            str(app.config["MYZONE_IMAGE_BANNER_DIR"]),
            name="banner上传",
            category="banner",
        )


class ChannelView(AuthModelView):
    """专栏视图"""

    can_create = True
    edit_modal = True

    column_labels = {
        "id": u"ID",
        "name": u"专栏名称",
        "create_time": u"创建时间",
        "update_time": u"修改时间",
    }

    # 格式化字段值
    column_formatters = {
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "update_time": lambda v, c, m, p: timestamp_to_str(
            m.update_time, "YYYY-MM-DD HH:mm:ss"
        ),
    }

    def __init__(self):
        super(ChannelView, self).__init__(Channel, db.session, name="专栏")


class CategoryView(AuthModelView):
    """分类视图"""

    can_create = True
    edit_modal = True

    column_labels = {
        "id": u"ID",
        "name": u"分类名称",
        "create_time": u"创建时间",
        "update_time": u"修改时间",
        "channel_id": u"专栏ID",
    }

    # 格式化字段值
    column_formatters = {
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "update_time": lambda v, c, m, p: timestamp_to_str(
            m.update_time, "YYYY-MM-DD HH:mm:ss"
        ),
    }

    def __init__(self):
        super(CategoryView, self).__init__(Category, db.session, name="分类")


class ArticleView(AuthModelView):
    """文章视图"""

    can_create = False
    edit_modal = True
    can_export = True
    column_searchable_list = ["title"]

    column_labels = {
        "id": u"ID",
        "title": u"文章标题",
        "body": u"文章内容",
        "body_html": u"文章html",
        "read_count": u"阅读数",
        "create_time": u"创建时间",
        "update_time": u"修改时间",
        "status": u"状态",
        "is_commentable": u"可评论",
        "author_id": u"用户ID",
        "channel_id": u"专栏ID",
        "category_id": u"分类ID",
    }

    # 格式化字段值
    column_formatters = {
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "update_time": lambda v, c, m, p: timestamp_to_str(
            m.update_time, "YYYY-MM-DD HH:mm:ss"
        ),
    }

    def __init__(self):
        super(ArticleView, self).__init__(Article, db.session, name="文章")


class TagView(AuthModelView):
    """标签视图"""

    can_create = False

    column_labels = {"id": u"ID", "name": u"标签名称", "create_time": u"创建时间"}

    column_formatters = {
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        )
    }

    def __init__(self):
        super(TagView, self).__init__(Tag, db.session, name="标签")


class CommentView(AuthModelView):
    """评论视图"""

    can_create = False

    column_labels = {
        "id": u"ID",
        "content": u"评论内容",
        "comment_level": u"评论等级",
        "create_time": u"创建时间",
        "status": u"状态",
        "article_id": u"文章ID",
        "from_uid": u"评论人ID",
        "to_uid": u"被评论人ID",
        "parent_id": u"父评论ID",
        "replied_id": u"被回复评论ID",
    }

    column_formatters = {
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        )
    }

    def __init__(self):
        super(CommentView, self).__init__(Comment, db.session, name="评论")


class LikeView(AuthModelView):
    """评论视图"""

    can_create = False

    column_labels = {
        "id": u"喜欢ID",
        "status": u"状态",
        "create_time": u"创建时间",
        "update_time": u"修改时间",
        "article_id": u"文章ID",
        "user_id": u"用户ID",
    }

    column_formatters = {
        "create_time": lambda v, c, m, p: timestamp_to_str(
            m.create_time, "YYYY-MM-DD HH:mm:ss"
        ),
        "update_time": lambda v, c, m, p: timestamp_to_str(
            m.update_time, "YYYY-MM-DD HH:mm:ss"
        ),
    }

    def __init__(self):
        super(LikeView, self).__init__(Like, db.session, name="喜欢")


def register_views(app):
    admin.index_view = AdminIndexView(template="admin_index.html", url="/admin")
    admin.add_view(RoleView())
    admin.add_view(UserView())
    admin.add_view(BannerView())
    admin.add_view(BannerFileView(app))
    admin.add_view(ChannelView())
    admin.add_view(CategoryView())
    admin.add_view(ArticleView())
    admin.add_view(TagView())
    admin.add_view(CommentView())
    admin.add_view(LikeView())
