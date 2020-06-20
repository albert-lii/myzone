# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2019/12/15 14:27
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
