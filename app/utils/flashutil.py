# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li
    :time: 2020/1/17 17:06 
"""
from flask import flash


def flash_ok(msg):
    flash(msg, "success")


def flash_info(msg):
    flash(msg, "info")


def flash_warning(msg):
    flash(msg, "warning")


def flash_error(msg):
    flash(msg, "error")
