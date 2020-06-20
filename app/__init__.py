# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 9:43 
"""
from flask import Flask


def create_app():
    """ 创建 flask app

    :return: app
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    import settings
    settings.init_app(app)

    from app.extensions import register_extensions
    register_extensions(app)

    from app.error_page import register_errors
    register_errors(app)

    register_blueprints(app)

    from app.db.cmds import register_dbcmds
    register_dbcmds(app)
    return app


def register_blueprints(app):
    """注册蓝图"""
    # 验证模块蓝图
    from app.bp_auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    # 主模块蓝图
    from app.bp_main import main_bp

    app.register_blueprint(main_bp)

    # 文章模块蓝图
    from app.bp_work import work_bp

    app.register_blueprint(work_bp, url_prefix="/article")

    # 个人中心模块
    from app.bp_myprofile import myprofile_bp

    app.register_blueprint(myprofile_bp, url_prefix="/myprofile")

    # 管理模块
    from app.bp_admin.views import register_views

    register_views(app)
