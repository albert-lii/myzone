# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 10:06 
"""
from pathlib import Path

import arrow
from flask import (
    render_template,
    request,
    current_app,
    redirect,
    url_for,
    jsonify,
    Response,
)
from flask_login import login_required, current_user

from app.bp_main.forms import SiteDescForm
from app.bp_main.models import Banner, SiteDesc
from app.bp_work.models import Article, Category, Tag
from app.extensions import csrf
from app.utils.times import timestamp_to_str
from app.utils.uploads import (
    upload_image,
    get_local_image,
    remove_unused_image_from_local,
)
from . import main_bp


@main_bp.route("/banner/image/<string:image_name>/", methods=["GET"])
@csrf.exempt  # 此路由去除 csrf 保护
def get_banner_image(image_name: str):
    """ 获取banner图片

    :param image_name: 图片名称
    """
    # 图片的完整路径
    image_path = Path.joinpath(
        current_app.config["MYZONE_IMAGE_BANNER_DIR"], image_name
    )
    with open(str(image_path), "rb") as f:
        resp = Response(f.read(), mimetype="image/png")
    return resp


@main_bp.route("/", methods=["GET"])
def index():
    """首页"""
    banners = Banner.query_used()
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_ARTICLE_PER_PAGE"]  # 每页的文章数
    pagination = Article.query_order_by_createtime(page, per_page=per_page)  # 创建分页器对象
    articles = pagination.items  # 从分页器中获取查询结果
    categories = Category.query_all()
    tags = Tag.query_all()
    return render_template(
        "main/index.html",
        pagination=pagination,
        articles=articles,
        categories=categories,
        tags=tags,
        timestamp_to_strftime=timestamp_to_str,
        func_id=0,
        banners=banners,
    )


@main_bp.route("/channel/<int:channel_id>/", methods=["GET"])
def get_articles_by_channel(channel_id: int):
    """分页查询指定专栏的文章"""
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_ARTICLE_PER_PAGE"]  # 每页的文章数
    pagination = Article.query_by_channel(
        channel_id, page, per_page=per_page
    )  # 创建分页器对象
    articles = pagination.items  # 从分页器中获取查询结果
    categories = Category.query_by_channel(channel_id)
    tags = Tag.query_all()
    return render_template(
        "main/index.html",
        pagination=pagination,
        articles=articles,
        categories=categories,
        tags=tags,
        timestamp_to_strftime=timestamp_to_str,
        func_id=channel_id,
    )


@main_bp.route("/category/<int:category_id>/", methods=["GET"])
def get_articles_by_category(category_id: int):
    """分页查询指定分类的文章"""
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_ARTICLE_PER_PAGE"]  # 每页的文章数
    pagination = Article.query_by_category(
        category_id, page, per_page=per_page
    )  # 创建分页器对象
    articles = pagination.items  # 从分页器中获取查询结果
    category = Category.query_by_id(category_id)
    tags = Tag.query_all()
    return render_template(
        "main/index.html",
        pagination=pagination,
        articles=articles,
        categories=category.channel.categories,
        tags=tags,
        timestamp_to_strftime=timestamp_to_str,
        func_id=category.channel_id,
    )


@main_bp.route("/category/<int:tag_id>/", methods=["GET"])
def get_articles_by_tag(tag_id: int):
    """分页查询拥有指定标签的文章"""
    page = request.args.get("page", 1, type=int)  # 指定的页码
    per_page = current_app.config["MYZONE_ARTICLE_PER_PAGE"]  # 每页的文章数
    tag = Tag.query_by_id(tag_id)
    pagination = tag.query_articles(page, per_page=per_page)  # 创建分页器对象
    articles = pagination.items  # 从分页器中获取查询结果
    categories = Category.query_all()
    tags = Tag.query_all()
    return render_template(
        "main/index.html",
        pagination=pagination,
        articles=articles,
        categories=categories,
        tags=tags,
        timestamp_to_strftime=timestamp_to_str,
        func_id=-1,
    )


@main_bp.route("/search/", methods=["GET"])
@csrf.exempt  # 此路由去除 csrf 保护
def get_articles_by_fullsearch():
    """全文搜索"""
    keyword = request.args.get("keyword", type=str)
    page = request.args.get("page", 1, type=int)  # 指定的页码
    if not keyword:
        return redirect(url_for(".index"))
    per_page = current_app.config["MYZONE_ARTICLE_PER_PAGE"]  # 每页的文章数
    pagination = Article.query_in_full_by_key(
        keyword, page, per_page=per_page
    )  # 创建分页器对象
    articles = pagination.items  # 从分页器中获取查询结果
    categories = Category.query_all()
    tags = Tag.query_all()
    return render_template(
        "main/index.html",
        pagination=pagination,
        articles=articles,
        categories=categories,
        tags=tags,
        timestamp_to_strftime=timestamp_to_str,
        func_id=-1,
    )


@main_bp.route("/about/", methods=["GET"])
def show_about():
    """关于本站"""
    site_desc = SiteDesc.query_by_id(1)
    return render_template("main/about.html", site_desc=site_desc, channel_id=3)


@main_bp.route("/about/edit/", methods=["GET", "POST"])
@login_required
def edit_about():
    """编辑网站说明"""
    if current_user.role_id != 3:
        # 只有管理员才能编辑网站说明
        return redirect(url_for(".index"))
    site_desc = SiteDesc.query_by_id(1)

    form = SiteDescForm()
    if form.validate_on_submit():
        site_desc.body = form.body.data
        body_html = request.form[
            "my-editormd-html-code"
        ]  # html 格式的文章內容，由 Editor.MD 自动生成的 textarea
        # site_desc.body_html = body_html
        site_desc.update_time = arrow.utcnow().timestamp
        site_desc.update()
        remove_unused_image_from_local(
            current_app.config["MYZONE_IMAGE_ABOUT_DIR"], body_html, 2
        )
        return redirect(url_for(".show_about"))
    form.body.data = site_desc.body
    return render_template("main/edit_about.html", form=form)


@main_bp.route("/about/upload-image/", methods=["POST"])
@login_required
@csrf.exempt  # 此路由去除 csrf 保护
def upload_about_image():
    """上传文章中的图片"""
    image_file = request.files.get("editormd-image-file")
    result: dict = upload_image(image_file, 4)
    if result["code"] == 0:
        res = {
            "success": 1,
            "message": "上传成功",
            "url": url_for(".get_about_image", image_name=result["data"]),
        }
    else:
        res = {"success": 0, "message": result["msg"]}
    return jsonify(res)


@main_bp.route("/about/image/<string:image_name>", methods=["GET"])
@csrf.exempt  # 此路由去除 csrf 保护
def get_about_image(image_name: str):
    """ 获取关于中的图片

    :param image_name: 图片名称
    """
    return get_local_image(
        Path.joinpath(current_app.config["MYZONE_IMAGE_ABOUT_DIR"], image_name)
    )
