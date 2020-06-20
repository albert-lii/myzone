# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2020/3/29 15:39
"""
import os
from pathlib import Path
from typing import List

import arrow
from flask import current_app, Response
from lxml import html

from app.response.maker import make_response_ok, make_response_error
from app.response.status import Status

# 文章封面图片命名规则
ARTICLE_IMAGE_COVER_PATTERN = "img_u{uid}a{aid}_cover"
# 文章内容图片命名规则
ARTICLE_IMAGE_PATTERN = "img_u{uid}aid"
# 用户头像图片命名规则
USER_AVATAR_PATTERN = "img_avatar_u{uid}"
# 关于中图片命名规则
ABOUT_IMAGE_PATTERN = "img_about"


def upload_image(
    image_file,
    image_type: int = 1,
    user_id: int = None,
    article_id: int = None,
    max_size: int = 2 * 1024 * 1024,
) -> dict:
    """上传图片

    :param image_file: 图片文件
    :param image_type: 1-文章封面 2-文章图片 3-用户头像 4-关于本站
    :param user_id: 用户id
    :param article_id: 文章id
    :param max_size: 图片大小的最大限制
    """
    if not image_file:
        # 文件为空
        return make_response_error(Status.ERROR_FILE_NOTFOUND).to_dict()
    if len(image_file.read()) > max_size:
        # 文件大小超过最大限制
        return make_response_error(Status.ERROR_FILE_OVERSIZE).to_dict()
    image_file.seek(0)  # 因为之前使用了 read() 方法，所以此处加上 seek(0)，否则会读取不到 file
    ex: str = os.path.splitext(image_file.filename)[1]  # 文件扩展名
    if image_type == 1:
        # 上传的是文章封面
        image_dir = Path.joinpath(
            current_app.config["MYZONE_IMAGE_ARTICLE_DIR"], "u" + str(user_id)
        )
        image_name: str = (ARTICLE_IMAGE_COVER_PATTERN + "{ex}").format(
            uid=user_id, aid=article_id, ex=ex
        )
    elif image_type == 2:
        # 上传的是文章内容图片
        image_dir = Path.joinpath(
            current_app.config["MYZONE_IMAGE_ARTICLE_DIR"], "u" + str(user_id)
        )
        image_name: str = (ARTICLE_IMAGE_PATTERN + "_{timestamp}{ex}").format(
            uid=user_id, timestamp=arrow.utcnow().timestamp, ex=ex
        )
    elif image_type == 3:
        # 上传的是用户头像
        image_dir = current_app.config["MYZONE_IMAGE_AVATAR_DIR"]
        image_name: str = (USER_AVATAR_PATTERN + "{ex}").format(uid=user_id, ex=ex)
    elif image_type == 4:
        # 上传的是关于中的图片
        image_dir = current_app.config["MYZONE_IMAGE_ABOUT_DIR"]
        image_name: str = (ABOUT_IMAGE_PATTERN + "_{timestamp}{ex}").format(
            timestamp=arrow.utcnow().timestamp, ex=ex
        )
    if not Path.exists(image_dir):
        Path.mkdir(image_dir, parents=True)
    image_path: Path = Path.joinpath(image_dir, image_name)  # 图片的完整路径
    image_file.save(str(image_path))
    return make_response_ok(u"上传成功", image_name).to_dict()


etree = html.etree


def get_local_image(image_path):
    """获取本地资源中的图片"""
    with open(str(image_path), "rb") as f:
        resp = Response(f.read(), mimetype="image/png")
    return resp


def _get_local_image_from_html(html_text: str, pattern: str) -> List[str]:
    """从html文本中获取所有存储在本地的图片的链接

    :param html_text: html文本
    :param pattern: 图片名称的部分片段
    """
    dom = etree.HTML(html_text)
    imgs = dom.xpath("//body//img/@src")  # 获取body标签下所有图片的链接
    local_imgs: List[str] = []
    for img in imgs:
        if pattern in img:
            local_imgs.append(img)
    return local_imgs


def rename_image_from_local(dst_dir: Path, article_id: int = None, user_id: int = None):
    """重命名本地资源中的图片

    :param dst_dir: 目标文件夹
    :param article_id: 文章id
    :param user_id: 用户id
    """
    if not Path.exists(dst_dir):
        # 图片文件夹不存在
        return
    dst_imgs = os.listdir(str(dst_dir))  # 获取该目录下所有图片的名称
    if not dst_imgs:
        # 图片文件夹中没有图片
        return
    pattern = ARTICLE_IMAGE_PATTERN
    pattern = pattern.format(uid=user_id)
    rename_imgs: List[str] = []  # 需要被重命名的图片
    for img in dst_imgs:
        if pattern in img:
            rename_imgs.append(img)
    if not rename_imgs:
        # 没有需要重命名的图片
        return
    for img in rename_imgs:
        os.rename(
            str(Path.joinpath(dst_dir, img)),
            str(
                Path.joinpath(
                    dst_dir, img.replace("aid", "a{aid}".format(aid=article_id))
                )
            ),
        )


def remove_unused_image_from_local(
    dst_dir: Path,
    html_text: str,
    article_type: int = 1,
    article_id: int = None,
    user_id: int = None,
):
    """从本地资源中，移除指定文章中不使用的图片

    :param dst_dir: 目标文件夹
    :param html_text: 文章的html文本
    :param article_type: 文章类型 1-普通博文 2-关于本站
    :param article_id: 文章id
    :param user_id: 用户id
    """
    if not Path.exists(dst_dir):
        # 图片文件夹不存在
        return
    dst_imgs = os.listdir(str(dst_dir))  # 获取该目录下所有图片的名称
    if not dst_imgs:
        # 图片文件夹中没有图片
        return
    if article_type == 1:
        pattern = ARTICLE_IMAGE_PATTERN
        pattern = pattern.format(uid=user_id).replace(
            "aid", "a{aid}".format(aid=article_id)
        )
        relate_imgs: List[str] = []  # 用于存储当前文章使用过的本地图片
        for img in dst_imgs:
            if pattern in img:
                if article_type == 1 and "cover" in img:
                    pass
                else:
                    relate_imgs.append(img)
    else:
        pattern = ABOUT_IMAGE_PATTERN
        relate_imgs = dst_imgs
    if not relate_imgs:
        # 当前文章未使用过本地图片
        return
    used_imgs: List[str] = _get_local_image_from_html(
        html_text, pattern
    )  # 当前文章中正在使用的本地图片路径列表
    if not used_imgs:
        # 当前文章中未使用图片，移除废弃的图片
        for img in relate_imgs:
            if article_type == 1 and "cover" in img:
                # 如果是文章封面图片，则不处理
                pass
            else:
                os.remove(str(Path.joinpath(dst_dir, img)))
        return
    for relate_img in relate_imgs:
        is_used = False
        for used_img in used_imgs:
            if relate_img in used_img:
                is_used = True
        if not is_used:
            os.remove(str(Path.joinpath(dst_dir, relate_img)))
