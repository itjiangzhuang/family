# -*- coding:utf-8 -*-
__author__ = 'jiangzhuang'

from app import db


class TestModel(db.Model):
    __tablename__ = 'test_models'
    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.Integer)  # 0: 正常, -1: 删除

    def __repr__(self):
        return '<test_models %r>' % self.id



