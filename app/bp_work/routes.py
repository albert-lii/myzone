# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/10 15:45
"""
from pathlib import Path
from typing import List, Tuple
import arrow

from flask import (
    render_template,
    redirect,
    request,
    url_for,
    jsonify,
    current_app,
    abort,
)
from flask_login import login_required, current_user

from app.bp_work import work_bp
from app.bp_work.forms import ArticleForm
from app.bp_work.models import Channel, Category, Article, Tag, Comment, Like
from app.extensions import csrf, db
from app.response.maker import make_response_ok, make_response_error
from app.response.status import Status
from app.utils.flashutil import flash_ok, flash_error
from app.utils.times import timestamp_to_str
from app.utils.uploads import (
    upload_image,
    get_local_image,
    rename_image_from_local,
    remove_unused_image_from_local,
)


@work_bp.route("/upload-image/", methods=["POST"])
@login_required
@csrf.exempt  # 此路由去除 csrf 保护
def upload_article_image():
    """上传文章中的图片"""
    image_file = request.files.get("editormd-image-file")
    result: dict = upload_image(image_file, 2, current_user.id)
    if result["code"] == 0:
        res = {
            "success": 1,
            "message": "上传成功",
            "url": url_for(".get_article_image", image_name=result["data"]),
        }
    else:
        res = {"success": 0, "message": result["msg"]}
    return jsonify(res)


@work_bp.route("/image/<string:image_name>", methods=["GET"])
@csrf.exempt  # 此路由去除 csrf 保护
def get_article_image(image_name: str):
    """ 获取文章图片

    :param image_name: 图片名称
    """
    # 图片的完整路径
    start_index = image_name.find("u")
    end_index = image_name.find("a")
    uid = image_name[start_index:end_index]
    return get_local_image(
        Path.joinpath(current_app.config["MYZONE_IMAGE_ARTICLE_DIR"], uid, image_name)
    )


@work_bp.route("/new/", methods=["GET", "POST"])
@login_required
def new_article():
    """新建文章"""
    form = ArticleForm()
    channels = Channel.query_all()  # 所有的文章专栏
    chan_choices: List[Tuple[int, str]] = []  # 所有的专栏选项
    for chan in channels:
        chan_choices.append((chan.id, chan.name))
    form.channel.choices = chan_choices
    categories = Category.query_all()  # 所有的文章分类
    cate_choices: List[dict] = []  # 所有的分类选项
    tags = Tag.query_all()  # 所有的标签
    tags_values: List[dict] = []  # 传递给前端，用于标签的自动提示
    if tags:
        for tag in tags:
            tags_values.append({"value": tag.name})
    for cate in categories:
        cate_choices.append(
            {"id": cate.id, "name": cate.name, "channel_id": cate.channel_id}
        )
    if request.method == "GET":
        def_channel_categories = channels[0].categories  # 获取默认的文章专栏下对应的文章分类信息
        def_cate_choices: List[Tuple[int, str]] = []  # 默认的专栏对应的文章分类选项列表
        for cate in def_channel_categories:
            def_cate_choices.append((cate.id, cate.name))
        form.category.choices = def_cate_choices
    else:
        cur_channel_categories = channels[form.channel.data - 1].categories
        cur_cate_choices: List[Tuple[int, str]] = []
        for cate in cur_channel_categories:
            cur_cate_choices.append((cate.id, cate.name))
        form.category.choices = cur_cate_choices
    if form.validate_on_submit():
        if form.publish.data:
            # 发布文章按钮被点击
            status = 3  # 默认状态为发布审核通过
        else:
            # 私密保存按钮被点击
            status = 0
        title = form.title.data
        body = form.body.data
        body_html = request.form[
            "my-editormd-html-code"
        ]  # html 格式的文章內容，由 Editor.MD 自动生成的 textarea
        category_id = form.category.data
        selected_cate: Category = None  # 当前选择的文章分类
        for cate in categories:
            if cate.id == category_id:
                selected_cate = cate
                break
        selected_channel: Channel = selected_cate.channel  # 选择的文章专栏
        article = Article()
        article.title = title
        article.body = body
        article.body_html = body_html
        article.status = status
        article.author_id = current_user.id
        article.author = current_user
        article.channel_id = selected_channel.id
        article.channel = selected_channel
        article.category_id = selected_cate.id
        article.category = selected_cate
        if form.tags.data:
            input_tags: List[str] = form.tags.data.split(",")
            for tag_name in input_tags:
                # 遍历标签，去除每个输入标签的首尾空格
                tag_name = tag_name.strip()
                tag = Tag.query_by_name(tag_name)
                if tag:
                    # 如果标签已在数据库中存在，则直接添加到当前文章的标签列表中
                    article.tags.append(tag)
                else:
                    # 如果标签不在数据库中存在，则先将标签添加到数据库中，在添加到当前文章的标签列表中
                    tag = Tag(name=tag_name)
                    tag.insert_single()
                    article.tags.append(tag)
        db.session.add(article)
        db.session.flush()
        if form.cover.data:
            # 如果有文章封面
            result: dict = upload_image(
                request.files.get("cover"), 1, current_user.id, article.id
            )
            if result["code"] == 0:
                cover_url = url_for(".get_article_image", image_name=result["data"])
                article.cover_url = cover_url
            else:
                flash_error(u"{}，文章封面上传失败".format(result["msg"]))
        rename_image_from_local(
            Path.joinpath(
                current_app.config["MYZONE_IMAGE_ARTICLE_DIR"],
                "u{uid}".format(uid=current_user.id),
            ),
            article.id,
            current_user.id,
        )
        article.body = body.replace(
            "/article/image/img_u{uid}aid_".format(uid=current_user.id),
            "/article/image/img_u{uid}a{aid}_".format(
                uid=current_user.id, aid=article.id
            ),
        )
        body_html = body_html.replace(
            "/article/image/img_u{uid}aid_".format(uid=current_user.id),
            "/article/image/img_u{uid}a{aid}_".format(
                uid=current_user.id, aid=article.id
            ),
        )
        article.body_html = body_html
        db.session.commit()
        remove_unused_image_from_local(
            Path.joinpath(
                current_app.config["MYZONE_IMAGE_ARTICLE_DIR"],
                "u{uid}".format(uid=current_user.id),
            ),
            body_html,
            1,
            article.id,
            current_user.id,
        )
        flash_ok(u"文章发布成功")
        return redirect(url_for(".show_article", article_id=article.id))
    return render_template(
        "work/edit_article.html", form=form, cate_choices=cate_choices, tags_values=tags_values
    )


@work_bp.route("/edit/<int:article_id>/", methods=["GET", "POST"])
@login_required
def edit_article(article_id: int):
    """编辑文章

    :param article_id: 文章 id
    """
    form = ArticleForm()
    article = Article.query_by_id_or_404(article_id)
    if article.author_id != current_user.id:
        return redirect(url_for(".new_article"))
    else:
        channels = Channel.query_all()  # 所有的文章专栏
        chan_choices: List[Tuple[int, str]] = []  # 所有的专栏选项
        for chan in channels:
            chan_choices.append((chan.id, chan.name))
        form.channel.choices = chan_choices
        categories = Category.query_all()  # 所有的文章分类
        cate_choices: List[dict] = []  # 所有的分类选项
        for cate in categories:
            cate_choices.append(
                {"id": cate.id, "name": cate.name, "channel_id": cate.channel_id}
            )
        tags = Tag.query_all()  # 所有的标签
        tags_values: List[dict] = []  # 传递给前端，用于标签的自动提示
        if tags:
            for tag in tags:
                tags_values.append({"value": tag.name})
        if request.method == "GET":
            form.title.data = article.title  # 设置文章的当前标题
            form.body.data = article.body  # 设置文章的当前内容
            if article.tags:
                cur_tags = article.tags  # 文章的当前标签
                input_tags = ""
                for tag in cur_tags:
                    input_tags += tag.name + ","
                input_tags = input_tags[:-1]
                form.tags.data = input_tags  # 设置文章的当前标签
            cur_channel = article.channel  # 文章的当前专栏
            form.channel.data = cur_channel.id  # 设置文章的当前专栏
            cur_channel_categories = cur_channel.categories  # 文章当前专栏下的分类列表
            cur_category = article.category  # 文章的当前分类
            cur_cate_choices: List[Tuple[int, str]] = []  # 文章当前专栏下对应的所有分类选项
            for cate in cur_channel_categories:
                cur_cate_choices.append((cate.id, cate.name))
            form.category.choices = cur_cate_choices
            form.category.data = cur_category.id  # 设置文章的当前分类
        else:
            cur_channel_categories = channels[form.channel.data - 1].categories
            cur_cate_choices: List[Tuple[int, str]] = []
            for cate in cur_channel_categories:
                cur_cate_choices.append((cate.id, cate.name))
            form.category.choices = cur_cate_choices
        if form.validate_on_submit():
            if form.publish.data:
                # 发布文章按钮被点击
                status = 3  # 默认状态为发布审核通过
            else:
                # 私密保存按钮被点击
                status = 0
            title = form.title.data
            body = form.body.data
            body_html = request.form[
                "my-editormd-html-code"
            ]  # html 格式的文章內容，由 Editor.MD 自动生成的 textarea
            category_id: int = form.category.data
            selected_cate: Category = None  # 当前选择的文章分类
            for cate in categories:
                if cate.id == category_id:
                    selected_cate = cate
                    break
            selected_channel = selected_cate.channel  # 选择的文章专栏
            article.title = title
            article.body = body
            article.body_html = body_html
            article.status = status
            article.channel_id = selected_channel.id
            article.channel = selected_channel
            article.category_id = selected_cate.id
            article.category = selected_cate
            # article.author = current_user
            if form.tags.data:
                input_tags: List[str] = form.tags.data.split(",")
                for tag_name in input_tags:
                    # 遍历标签，去除每个输入标签的首尾空格
                    tag_name = tag_name.strip()
                    tag = Tag.query_by_name(tag_name)
                    if tag:
                        # 如果标签已在数据库中存在，则直接添加到当前文章的标签列表中
                        article.tags.append(tag)
                    else:
                        # 如果标签不在数据库中存在，则先将标签添加到数据库中，在添加到当前文章的标签列表中
                        tag = Tag(name=tag_name)
                        tag.insert_single()
                        article.tags.append(tag)
            if form.cover.data:
                result: dict = upload_image(
                    request.files.get("cover"), 1, current_user.id, article.id
                )
                if result["code"] == 0:
                    cover_url = url_for(".get_article_image", image_name=result["data"])
                    article.cover_url = cover_url
                else:
                    flash_error(u"文章封面上传失败")
            rename_image_from_local(
                Path.joinpath(
                    current_app.config["MYZONE_IMAGE_ARTICLE_DIR"],
                    "u{uid}".format(uid=current_user.id),
                ),
                article.id,
                current_user.id,
            )
            article.body = body.replace(
                "/article/image/img_u{uid}aid_".format(uid=current_user.id),
                "/article/image/img_u{uid}a{aid}_".format(
                    uid=current_user.id, aid=article.id
                ),
            )
            body_html = body_html.replace(
                "/article/image/img_u{uid}aid_".format(uid=current_user.id),
                "/article/image/img_u{uid}a{aid}_".format(
                    uid=current_user.id, aid=article.id
                ),
            )
            article.body_html = body_html
            article.update_time = arrow.utcnow().timestamp
            article.update()
            remove_unused_image_from_local(
                Path.joinpath(
                    current_app.config["MYZONE_IMAGE_ARTICLE_DIR"],
                    "u{uid}".format(uid=current_user.id),
                ),
                body_html,
                1,
                article.id,
                current_user.id,
            )
            flash_ok("文章发布成功")
            return redirect(url_for(".show_article", article_id=article.id))
        return render_template(
            "work/edit_article.html",
            form=form,
            cate_choices=cate_choices,
            cover_url=article.cover_url,
            tags_values=tags_values
        )


@work_bp.route("/<int:article_id>/", methods=["GET"])
def show_article(article_id: int):
    """显示文章

    :param article_id: 文章id
    """
    origin = request.args.get("from", type=int, default=-1)  # -1-其他 0-首页 1-技术杂谈 2-生活有道
    article = Article.query_by_id_or_404(article_id)
    if article.status == 3:
        # 如果是审核通过，发布的文章
        article.increase_read_count()
    elif article.status == 0:
        # 如果是私密文章
        if not current_user.is_authenticated or current_user.id != article.author_id:
            # 没有登录，或者登录用户不是私密文章作者，不得观看私密文章
            abort(404)
    else:
        abort(404)
    pre_article = Article.query_pre(article_id)
    next_article = Article.query_next(article_id)
    lv1_comments: List[Comment] = []  # 一级评论列表
    if article.comments:
        for comment in article.comments:
            if comment.comment_level == 1:
                lv1_comments.insert(0, comment)  # 按照评论时间降序排列
    my_like = {"status": 0}
    if current_user.is_authenticated:
        comments = article.comments
        for cmt in comments:
            if cmt.to_uid == current_user.id and cmt.status == 2:
                cmt.status = 3  # 未读的评论标记为已读
                cmt.update()
        likes = article.likes
        for like in likes:
            if like.to_uid == current_user.id and like.status == 1:
                like.status = 2  # 未读的喜欢标记为已读
                like.update()
            if like.from_uid == current_user.id:
                my_like["status"] = like.status
    return render_template(
        "work/article.html",
        article=article,
        comments=lv1_comments,
        like=my_like,
        timestamp_to_str=timestamp_to_str,
        pre_article=pre_article,
        next_article=next_article,
        channel_id=origin,
    )


@work_bp.route("/comment/add/", methods=["POST"])
@login_required
def add_comment():
    """添加评论 """
    args = request.json
    article_id: int = args.get("article_id")
    content: str = args.get("content")
    comment: Comment = Comment()
    comment.content = content
    comment.comment_level = 1
    comment.article_id = article_id
    comment.article = Article.query_by_id(article_id)
    comment.from_uid = current_user.id
    comment.from_user = current_user
    comment.to_uid = comment.article.author_id
    comment.to_user = comment.article.author
    comment.insert_single()
    return make_response_ok("评论已发布").to_json()


@work_bp.route("/comment/reply/", methods=["POST"])
@login_required
def reply_comment():
    """回复评论"""
    args: dict = request.json
    parent_id: int = args.get("parent_id")  # 父评论 id
    replied_id: int = args.get("replied_id")  # 被回复的评论 id
    content: str = args.get("content")
    parent_comment = Comment.query_by_id(parent_id)  # 父评论
    replied_comment = Comment.query_by_id(replied_id)  # 被回复的评论
    comment = Comment()
    comment.content = content
    comment.comment_level = 2
    comment.article_id = parent_comment.article.id
    comment.article = parent_comment.article
    comment.from_uid = current_user.id
    comment.from_user = current_user
    comment.to_uid = replied_comment.from_uid
    comment.to_user = replied_comment.from_user
    comment.parent_id = parent_id
    comment.parent_comment = parent_comment
    comment.replied_id = replied_id
    comment.replied_comment = replied_comment
    comment.insert_single()
    return make_response_ok("评论已发布").to_json()


@work_bp.route("/like/", methods=["POST"])
@login_required
def do_like():
    """喜欢操作"""
    args: dict = request.json
    article_id: int = args.get("article_id")
    action: int = args.get("action")  # 操作，0-取消喜欢 1-喜欢
    article = Article.query_by_id(article_id)
    like = Like.query_by_aid(article_id, current_user.id)
    if like:
        if action == 0:
            like.status = 0
        elif action == 1:
            like.status = 2
        else:
            return make_response_error(Status.ERROR_INVALID_LIKE_ACTION).to_json()
        like.update()
    else:
        like = Like()
        like.status = action
        like.article_id = article_id
        like.article = article
        like.from_uid = current_user.id
        like.from_user = current_user
        like.to_uid = article.author_id
        like.to_user = article.author
        like.insert_single()
    return make_response_ok("操作成功").to_json()
