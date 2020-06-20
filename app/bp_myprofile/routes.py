# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2020/3/13 22:44
"""
from pathlib import Path
from typing import Tuple

import arrow
from flask import request, render_template, current_app, url_for, redirect
from flask_login import login_required, current_user

from app.bp_auth.models import User
from app.bp_myprofile.forms import (
    AvatarForm,
    UserNameForm,
    PasswordForm,
    PersonalSiteForm,
)
from app.bp_work.models import Article, Comment, Like
from app.utils.flashutil import flash_ok, flash_error
from app.utils.checkers import check_username_existed
from app.utils.security import encrypt_password
from app.utils.times import timestamp_to_str
from app.utils.uploads import upload_image, get_local_image
from . import myprofile_bp


def _get_unread_count() -> Tuple[int]:
    """获取未读的消息数"""
    unread_like_num = 0
    unread_comment_num = 0
    received_likes = current_user.received_likes
    received_comments = current_user.received_comments
    if received_likes:
        for like in received_likes:
            if like.status == 1:
                unread_like_num += 1
    if received_comments:
        for comment in received_comments:
            if comment.status == 2:
                unread_comment_num += 1
    return unread_like_num, unread_comment_num


@myprofile_bp.route("/")
@login_required
def index():
    """我的主页首页"""
    return redirect(url_for(".get_my_likes"))


@myprofile_bp.route("/likes/")
@login_required
def get_my_likes():
    """获取我的喜欢"""
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_MYPROFILE_ITEM_PER_PAGE"]  # 每页的喜欢数据数
    pagination = Like.query_by_uid(current_user.id, page, per_page=per_page)  # 创建分页器对象
    likes = pagination.items  # 从分页器中获取查询结果
    unread_array = _get_unread_count()
    return render_template(
        "myprofile/myprofile.html",
        pagination=pagination,
        show_type=0,
        likes=likes,
        timestamp_to_str=timestamp_to_str,
        unread_like_num=unread_array[0],
        unread_comment_num=unread_array[1],
    )


@myprofile_bp.route("/comments/")
@login_required
def get_my_comments():
    """获取我的评论"""
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_MYPROFILE_ITEM_PER_PAGE"]  # 每页的喜欢数据数
    pagination = Comment.query_by_uid(
        current_user.id, page, per_page=per_page
    )  # 创建分页器对象
    comments = pagination.items  # 从分页器中获取查询结果
    unread_array = _get_unread_count()
    return render_template(
        "myprofile/myprofile.html",
        pagination=pagination,
        show_type=1,
        comments=comments,
        timestamp_to_str=timestamp_to_str,
        unread_like_num=unread_array[0],
        unread_comment_num=unread_array[1],
    )


@myprofile_bp.route("/received-likes/")
@login_required
def get_received_likes():
    """获取收到的喜欢"""
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_MYPROFILE_ITEM_PER_PAGE"]  # 每页的喜欢数据数
    pagination = Like.query_received_by_uid(
        current_user.id, page, per_page=per_page
    )  # 创建分页器对象
    received_likes = pagination.items  # 从分页器中获取查询结果
    unread_array = _get_unread_count()
    return render_template(
        "myprofile/myprofile.html",
        pagination=pagination,
        show_type=2,
        received_likes=received_likes,
        timestamp_to_str=timestamp_to_str,
        unread_like_num=unread_array[0],
        unread_comment_num=unread_array[1],
    )


@myprofile_bp.route("/received-comments/")
@login_required
def get_received_comments():
    """获取收到的评论"""
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_MYPROFILE_ITEM_PER_PAGE"]  # 每页的喜欢数据数
    pagination = Comment.query_received_by_uid(
        current_user.id, page, per_page=per_page
    )  # 创建分页器对象
    received_comments = pagination.items  # 从分页器中获取查询结果
    unread_array = _get_unread_count()
    return render_template(
        "myprofile/myprofile.html",
        pagination=pagination,
        show_type=3,
        received_comments=received_comments,
        timestamp_to_str=timestamp_to_str,
        unread_like_num=unread_array[0],
        unread_comment_num=unread_array[1],
    )


@myprofile_bp.route("/private/")
@login_required
def get_private_articles():
    """获取我的私密文章"""
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_MYPROFILE_ITEM_PER_PAGE"]  # 每页的喜欢数据数
    pagination = Article.query_private(
        current_user.id, page, per_page=per_page
    )  # 创建分页器对象
    private_articles = pagination.items  # 从分页器中获取查询结果
    unread_array = _get_unread_count()
    return render_template(
        "myprofile/myprofile.html",
        pagination=pagination,
        show_type=4,
        private_articles=private_articles,
        timestamp_to_str=timestamp_to_str,
        unread_like_num=unread_array[0],
        unread_comment_num=unread_array[1],
    )


@myprofile_bp.route("/avatar/<string:image_name>/", methods=["GET"])
def get_avatar_image(image_name: str):
    """ 获取用户头像图片

    :param image_name: 头像图片名称
    """
    # 图片的完整路径
    return get_local_image(
        Path.joinpath(current_app.config["MYZONE_IMAGE_AVATAR_DIR"], image_name)
    )


@myprofile_bp.route("/setting/", methods=["GET", "POST"])
@login_required
def setting():
    """设置，用于修改用户信息"""
    avatar_form = AvatarForm()
    username_form = UserNameForm()
    pwd_form = PasswordForm()
    site_form = PersonalSiteForm()
    user = User.query_by_id(current_user.id)
    if avatar_form.avatar_submit.data and avatar_form.validate():
        if avatar_form.avatar.data:
            result: dict = upload_image(
                request.files.get("avatar"), 3, user_id=user.id, max_size=500 * 1024
            )
            if result["code"] == 0:
                avatar_url = url_for(".get_avatar_image", image_name=result["data"])
                user.avatar_url = avatar_url
                user.update_time = arrow.utcnow().timestamp
                user.update()
                flash_ok(u"头像修改成功")
                redirect(url_for(".setting"))
            else:
                flash_error(result["msg"])
    elif username_form.username_submit.data:
        if username_form.validate():
            username = username_form.username.data
            if check_username_existed(username):
                flash_error("用户名已存在")
                pass
            else:
                user.username = username
                user.update_time = arrow.utcnow().timestamp
                user.update()
                flash_ok(u"用户名修改成功")
                return redirect(url_for(".setting"))
        else:
            flash_error(username_form.username.errors[0])
    elif pwd_form.password_submit.data:
        if pwd_form.validate():
            user.password = encrypt_password(pwd_form.password.data)
            user.update_time = arrow.utcnow().timestamp
            user.update()
            flash_ok(u"密码修改成功")
            return redirect(url_for(".setting"))
        else:
            flash_error(pwd_form.password.errors[0])
    elif site_form.personal_site_submit.data:
        if site_form.validate():
            user.personal_site = site_form.personal_site.data
            user.update_time = arrow.utcnow().timestamp
            user.update()
            flash_ok(u"个站修改成功")
            return redirect(url_for(".setting"))
        else:
            flash_error(site_form.personal_site_submit.errors[0])
    username_form.username.data = user.username
    site_form.personal_site.data = user.personal_site
    return render_template(
        "myprofile/setting.html",
        avatar_form=avatar_form,
        username_form=username_form,
        pwd_form=pwd_form,
        site_form=site_form,
        email=user.email,
    )
