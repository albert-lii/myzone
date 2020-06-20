# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2020/3/13 22:25
"""
from flask import Blueprint

myprofile_bp = Blueprint(
    "myprofile",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="",
)

from . import routes
