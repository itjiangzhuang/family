# -*- coding:utf-8 -*-
__author__ = 'jiangzhuang'

from flask import Blueprint, render_template
index_controller = Blueprint('index_controller', __name__, url_prefix='/')


@index_controller.route('/', methods=['GET'])
def index():
    return render_template('index/index.html')

