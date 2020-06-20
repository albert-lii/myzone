# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/11/6 18:09
"""
import platform
from pathlib import Path


class BaseConfig(object):
    """基础配置"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = "123456"
    JSON_AS_ASCII = False  # jsonify 返回的数据支持中文显示
    JSON_SORT_KEYS = False  # jsonify 返回的 json 数据不根据 key 自动排序

    # ==================================================================
    # 数据库相关配置
    # ==================================================================
    DB_DIALECT = "mysql"  # 使用的数据库
    DB_DRIVER = "pymysql"  # 数据库驱动
    DB_USERNAME = "xxx"  # 数据库用户名
    DB_PASSWORD = "xxxxxx"  # 数据库密码
    DB_HOST = "localhost:3306"  # 数据库服务器
    DB_NAME = "xxxx"  # 数据库名称

    SQLALCHEMY_DATABASE_URI = "{dialect}+{driver}://{username}:{password}@{host}/{dbname}?charset=utf8".format(
        dialect=DB_DIALECT,
        driver=DB_DRIVER,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        dbname=DB_NAME,
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # Flask-SQLAlchemy 将追踪对象的修改并且发送信号
    SQLAlCHEMY_ECHO = True  # 显示 sql 语句

    # ==================================================================
    # 邮箱相关配置
    # ==================================================================
    MAIL_SERVER = "smtp.163.com"  # 发送方电子邮箱服务器的主机名或 IP 地址
    MAIL_PORT = "465"  # 发送方电子邮箱服务器的端口
    # MAIL_USE_TLS = True  # 启用传输层安全 TLS 协议
    MAIL_USE_SSL = True  # 启用安全套接层安全 SSL 协议
    MAIL_USERNAME = "xxx@163.com"  # 发送方邮箱账户的用户名
    MAIL_PASSWORD = "xxx"  # 发送方邮箱账户的密码
    MAIL_DEFAULT_SENDER = "xxx@163.com"  # 默认的发送者

    # ==================================================================
    # admin 相关配置
    # ==================================================================
    # FLASK_ADMIN_SWATCH = "Cerulean"  # admin 主题，有的主题在Centos7上显示样式有问题，此处暂时注释掉
    BABEL_DEFAULT_LOCALE = "zh_CN"  # 英文转中文

    # ==================================================================
    # myzone 相关配置
    # ==================================================================
    MYZONE_VERSION = "1.0.0"  # 当前程序的版本号

    MYZONE_PARENT_PATH = str(Path.cwd()).split("myzone")[0]  # 项目的根路径
    MYZONE_IMAGE_DIR = Path.joinpath(
        Path(MYZONE_PARENT_PATH), "myzone-uploads", "image"
    )  # 上传的图片的所在目录
    MYZONE_IMAGE_BANNER_DIR = Path.joinpath(
        MYZONE_IMAGE_DIR, "banner"
    )  # 上传的banner图片的所在目录
    MYZONE_IMAGE_AVATAR_DIR = Path.joinpath(MYZONE_IMAGE_DIR, "avatar")  # 上传的头像图片的所在目录
    MYZONE_IMAGE_ARTICLE_DIR = Path.joinpath(
        MYZONE_IMAGE_DIR, "article"
    )  # 上传的文章图片的所在目录
    MYZONE_IMAGE_ABOUT_DIR = Path.joinpath(MYZONE_IMAGE_DIR, "about")  # 上传的关于本站图片所在目录
    # 如果文件夹的所在目录不存在，则创建
    if not Path.exists(MYZONE_IMAGE_BANNER_DIR):
        Path.mkdir(MYZONE_IMAGE_BANNER_DIR, parents=True)
    if not Path.exists(MYZONE_IMAGE_AVATAR_DIR):
        Path.mkdir(MYZONE_IMAGE_AVATAR_DIR, parents=True)
    if not Path.exists(MYZONE_IMAGE_ARTICLE_DIR):
        Path.mkdir(MYZONE_IMAGE_ARTICLE_DIR, parents=True)
    if not Path.exists(MYZONE_IMAGE_ABOUT_DIR):
        Path.mkdir(MYZONE_IMAGE_ABOUT_DIR, parents=True)

    MYZONE_ARTICLE_PER_PAGE = 10  # 首页中的每页文章数
    MYZONE_MYPROFILE_ITEM_PER_PAGE = 15  # 我的主页中每页item的个数


class DevelopmentConfig(BaseConfig):
    """开发环境下的配置"""
    DEBUG = True

    # ==================================================================
    # 邮箱相关配置
    # ==================================================================
    MAIL_SERVER = "smtp.163.com"  # 发送方电子邮箱服务器的主机名或 IP 地址
    MAIL_PORT = "465"  # 发送方电子邮箱服务器的端口
    # MAIL_USE_TLS = True  # 启用传输层安全 TLS 协议
    MAIL_USE_SSL = True  # 启用安全套接层安全 SSL 协议
    MAIL_USERNAME = "xxx@163.com"  # 发送方邮箱账户的用户名
    MAIL_PASSWORD = "xxx"  # 发送方邮箱账户的密码
    MAIL_DEFAULT_SENDER = "xxx@163.com"  # 默认的发送者


class TestingConfig(BaseConfig):
    """测试环境下的配置"""
    TESTING = True


class ProductionConfig(BaseConfig):
    """生产环境下的配置"""
    SECRET_KEY = "123456"

    # ==================================================================
    # 数据库相关配置
    # ==================================================================
    DB_DIALECT = "mysql"  # 使用的数据库
    DB_DRIVER = "pymysql"  # 数据库驱动
    DB_USERNAME = "xxx"  # 数据库用户名
    DB_PASSWORD = "xxxxxxxx"  # 数据库密码
    DB_HOST = "localhost:3306"  # 数据库服务器
    DB_NAME = "xxxx"  # 数据库名称

    SQLALCHEMY_DATABASE_URI = "{dialect}+{driver}://{username}:{password}@{host}/{dbname}?charset=utf8".format(
        dialect=DB_DIALECT,
        driver=DB_DRIVER,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        dbname=DB_NAME,
    )
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # Flask-SQLAlchemy 将追踪对象的修改并且发送信号
    SQLAlCHEMY_ECHO = True  # 显示 sql 语句

    # ==================================================================
    # 邮箱相关配置
    # ==================================================================
    MAIL_SERVER = "smtp.163.com"  # 发送方电子邮箱服务器的主机名或 IP 地址
    MAIL_PORT = "465"  # 发送方电子邮箱服务器的端口
    # MAIL_USE_TLS = True  # 启用传输层安全 TLS 协议
    MAIL_USE_SSL = True  # 启用安全套接层安全 SSL 协议
    MAIL_USERNAME = "xxx@163.com"  # 发送方邮箱账户的用户名
    MAIL_PASSWORD = "xxxxxxxx"  # 发送方邮箱账户的密码
    MAIL_DEFAULT_SENDER = "xxx@163.com"  # 默认的发送者


def init_app(app):
    sys = platform.system()
    if sys == "Windows":
        config = DevelopmentConfig
    elif sys == "Linux":
        config = ProductionConfig
    else:
        config = DevelopmentConfig
    app.config.from_object(config)
