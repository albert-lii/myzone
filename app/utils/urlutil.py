# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2019/12/22 8:58
"""
from flask import request, redirect, url_for


def redirect_back(default_url: str = None, **kwargs):
    """重定向回到上一页

    :param default_url: 默认的上一页地址
    """
    next_url = request.args.get("next")  # 在 URL中手动加入的包含访问来源的地址 URL 的查询参数，一般把参数命名为 next
    # 访问来源的地址。当用户直接在浏览器地址栏中输入 url 或者因防火墙或浏览器设置自动清除或修改 referrer 字段时，referrer 可能为空值
    referrer_url = request.referrer
    if default_url is None:
        default_url = url_for("main.index")  # 默认的上一页地址，当 next_url 与 referrer_url 都失效时使用
    for target in (next_url, referrer_url):
        if target:
            return redirect(target)
    return redirect(url_for(default_url, **kwargs))
