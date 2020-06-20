# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 18:01 
"""
from flask import render_template
from flask_wtf.csrf import CSRFError


def register_errors(app):
    """设置蓝图的自定义错误处理"""

    @app.errorhandler(400)
    def bad_request(e):
        return render_template("error/400.html"), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("error/500.html"), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template("error/400.html", description=e.description), 400
