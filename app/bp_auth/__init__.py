# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 9:43 
"""
from flask import Blueprint

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="",
)

from . import routes
