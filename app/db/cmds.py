# -*- coding:utf-8 -*-
"""
    初始化数据库，并往一些不常改动的表中添加信息

    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2019/12/18 16:39 
"""
import click

from app.db.initializer import (
    generate_role,
    generate_admin,
    generate_article_channel,
    generate_article_category,
    generate_site_desc,
)
from app.extensions import db


def register_dbcmds(app):
    @app.cli.command()
    @click.option("--drop", is_flag=True, help="Create after drop.")
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                "This operation will delete the database, do you want to continue?",
                abort=True,
            )
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialized database.")
        click.echo("Generating the user role....")
        # 初始化用户角色数据
        generate_role()
        click.echo("Generating the channel....")
        # 初始化管理员数据
        generate_admin()
        click.echo("Generating the admin....")
        # 初始化文章专栏数据
        generate_article_channel()
        click.echo("Generating the category....")
        # 初始化文章分类数据
        generate_article_category()
        # 初始化网站描述数据
        click.echo("Generating the siteDesc....")
        generate_site_desc()
        click.echo("Done.")
