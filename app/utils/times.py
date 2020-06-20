# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2020/2/13 14:29
"""

import arrow


def timestamp_to_str(timestamp: int, pattern: str = "YYYY-MM-DD HH:mm"):
    """时间戳转格式化日期字符串

    :param timestamp: 时间戳
    :param pattern: 日期格式
    :return: 格式化后的日期字符串
    """
    return arrow.get(timestamp).to("local").format(pattern)
