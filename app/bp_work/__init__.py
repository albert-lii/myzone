# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/9 20:03
"""
from flask import Blueprint

work_bp = Blueprint(
    "work",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="",
)

from . import routes
