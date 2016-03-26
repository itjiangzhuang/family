# -*- coding:utf-8 -*-
__author__ = 'jiangzhuang'

from flask import Blueprint, render_template
wechat_controller = Blueprint('wechat_controller', __name__, url_prefix='/wechat')


@wechat_controller.route('/', methods=['GET'])
def index():
    return render_template('wechat/index.html')

