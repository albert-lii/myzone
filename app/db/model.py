# -*- coding:utf-8 -*-
"""
    :author: Albert Li
    :copyright: © 2019 Albert Li 
    :time: 2020/3/27 22:15
"""
from app.extensions import db


class BaseModel(object):
    def insert_single(self):
        """插入单条数据"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def insert_all(instances: list):
        """插入多条数据"""
        db.session.add_all(instances)
        db.session.commit()

    @classmethod
    def query_all(cls: db.Model):
        """查询表中所有的信息"""
        return cls.query.all()

    @classmethod
    def query_by_id(cls: db.Model, data_id: int):
        """根据 id 查询数据"""
        return cls.query.get(data_id)

    @classmethod
    def query_by_id_or_404(cls: db.Model, data_id: int):
        """根据 id 查询数据，如果数据不存存在则抛出 404 异常"""
        return cls.query.get_or_404(data_id)

    def update(self):
        """更新数据"""
        db.session.commit()

    def delete(self):
        """删除数据"""
        db.session.delete(self)
        db.session.commit()
