# -*- coding:utf-8 -*-
__author__ = 'jiangzhuang'

from flask import Blueprint, current_app, request
from app.weixin.weixin_helper import WxHelper,WxApiConfig
from app.helpers.common_helper import xmlToDict

wechat_controller = Blueprint('wechat_controller', __name__, url_prefix='/wx')

# 初始化微信工具类
def _get_wx_helper():
    app_id=current_app.config.get("APPID"),
    app_secret=current_app.config.get("APPSECRET"),
    token=current_app.config.get("TOKEN")
    current_app.logger.debug("app_id=",app_id,",app_secret=",app_secret,",token=",token)
    wx_api_config = WxApiConfig(app_id,app_secret,token)
    wx_helper = WxHelper(wx_api_config)
    return wx_helper

# 微信<->服务器 消息验证处理器
@wechat_controller.route('/', methods=['GET'])
def index():
    try:
        wx_helper =_get_wx_helper()

        current_app.logger.debug("GET")
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        # 微信消息验证
        if wx_helper.check_signature(signature, timestamp, nonce):
           return echostr
        else:
           return ''
    except Exception, e:
        current_app.logger.error(str(e))
        return ''

# 微信<->服务器 核心消息处理器
@wechat_controller.route('/', methods=['POST'])
def index():
    try:
        body_xml = request.data
        current_app.logger.debug(body_xml)
        xml_dic = xmlToDict(body_xml)
        # 明文处理
        msgtype = xml_dic.MsgType
        if msgtype == "event":
            key = xml_dic.Event
            if key == 'subscribe':  # 关注
                # TODO
                return
            elif key == 'unsubscribe': # 取消关注
                # TODO
                return
            else:
                return
                raise Exception(' unhandle event ' + key)
        elif msgtype == "text":
            key = "all"
            current_app.logger.debug(' the content : '+ xml_dic.Content)
            return
        else:
            raise Exception(' unhandle msgtype ' + msgtype)
            return
    except Exception, e:
        current_app.logger.error(e.args)
        return
