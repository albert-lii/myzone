# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 17:49 
"""
from flask_admin import Admin, AdminIndexView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

bootstrap = Bootstrap()
csrf = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
admin = Admin(
    name="iGank",
    template_mode="bootstrap3",
    index_view=AdminIndexView(template="admin_index.html", url="/admin"),
)


def register_extensions(app):
    """註冊所有的插件"""
    bootstrap.init_app(app)
    csrf.init_app(app)
    # 登录扩展
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.login_message = "请登录"
    login_manager.init_app(app)
    # sqlalchemy的扩展
    db.init_app(app)
    db.app = app
    # 数据库迁移扩展
    migrate.init_app(app, db)
    # 发送邮件扩展
    mail.init_app(app)
    # 后端管理扩展
    admin.init_app(app)
