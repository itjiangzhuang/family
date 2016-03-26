# -*- coding:utf-8 -*-
__author__ = 'jiangzhuang'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config_dict
import sys
import logging
from logging.handlers import RotatingFileHandler


db = SQLAlchemy()


try:
    from imp import reload
    reload(sys)
    sys.setdefaultencoding('utf8')
except (AttributeError, NameError):
    pass


def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_mode])
    config_dict[config_mode].init_app(app)
    app.config_mode = config_mode

    # 内部日志
    rotating_handler1 = RotatingFileHandler('logs/info.log', maxBytes=1 * 1024 * 1024, backupCount=5)
    rotating_handler2 = RotatingFileHandler('logs/error.log', maxBytes=1 * 1024 * 1024, backupCount=2)

    formatter1 = logging.Formatter("-" * 100 +
                                   '\n %(asctime)s %(levelname)s - '
                                   'in %(funcName)s [%(filename)s:%(lineno)d]:\n %(message)s')

    rotating_handler1.setFormatter(formatter1)
    rotating_handler2.setFormatter(formatter1)
    app.logger.addHandler(rotating_handler1)
    app.logger.addHandler(rotating_handler2)

    app.logger.setLevel(logging.INFO)
    rotating_handler2.setLevel(logging.ERROR)
    if app.config.get("DEBUG"):
        # app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)

    db.init_app(app)

    from .controllers.index_controller import index_controller as index_blueprint
    app.register_blueprint(index_blueprint)
    from .controllers.wechat_controller import wechat_controller as wechat_blueprint
    app.register_blueprint(wechat_blueprint)

    return app

