# -*- coding:utf-8 -*-
__author__ = 'jiangzhuang'

import hashlib
from url_helper import url_params_encode_str, url_requset
import json
import time


class WxApiConfig():
    def __init__(self, app_id, app_secret, token):
        # 配置参数
        self.appid = app_id
        self.appsecret = app_secret
        self.token = token

        # 接口地址链接
        self._OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize"
        self._ACCESS_URL = "https://api.weixin.qq.com/cgi-bin/token"
        self._CODEACCESS_URL = "https://api.weixin.qq.com/sns/oauth2/access_token"
        self._USER_URL = "https://api.weixin.qq.com/cgi-bin/user/info"
        self._REFRESHTOKRN_URL = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
        self._SNSUSER_URL = "https://api.weixin.qq.com/sns/userinfo"
        self._VALIDATE_URL = "https://api.weixin.qq.com/sns/auth"
        self._SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/custom/send"
        self._JSAPI_URL = "https://api.weixin.qq.com/cgi-bin/ticket/getticket"
        self._MENU_CREATE_URL = "https://api.weixin.qq.com/cgi-bin/menu/create"
        self._MENU_DELETE_URL = "https://api.weixin.qq.com/cgi-bin/menu/delete"

    def __str__(self):
        return "appid:s%,appsecret:s%,token:s%" \
               % (self.appid, self.appsecret, self.token)


class WxHelper(object):
    def __init__(self, wx_api_config):
        self.wx_api_config = wx_api_config

    # 微信签名校验
    @classmethod
    def check_signature(cls, signature, timestamp, nonce):
        tmp = [cls.wx_api_config.token, timestamp, nonce]
        tmp.sort()
        code = hashlib.sha1("".join(tmp)).hexdigest()
        return code == signature

    # 网页授权获取用户信息
    # http://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html
    @classmethod
    def oauth2_info(cls, redirect_uri, state, scope="snsapi_base"):
        '''
        返回授权url地址
        :param redirect_uri:
        :param state:
        :param scope:
        :return:
        '''
        params = {
            "appid": cls.wx_api_config.appid,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": state,
        }
        url_params = url_params_encode_str(params)
        return "%s?%s#%s" % (cls.wx_api_config._OAUTH_URL, url_params, "wechat_redirect")

    # 获取access_token
    # http://mp.weixin.qq.com/wiki/14/9f9c82c1af308e3b14ba9b973f99a8ba.html
    @classmethod
    def get_access_token(cls):
        '''
        公众号的全局唯一票据
        :return:  需要进行缓存，512个字符空间，有效期2个小时
        '''
        params = {
            "grant_type": "client_credential",
            "appid": cls.wx_api_config.appid,
            "secret": cls.wx_api_config.appsecret
        }
        return url_requset(cls.wx_api_config._ACCESS_URL, params)

    # 获取用户基本信息
    # http://mp.weixin.qq.com/wiki/1/8a5ce6257f1d3b2afb20f83e72b72ce9.html
    @classmethod
    def get_user_info(cls, access_token, openid, lang="zh_CN"):
        params = {
            "access_token": access_token,
            "openid": openid,
            "lang": lang
        }
        return url_requset(cls.wx_api_config._USER_URL, params)

    # 通过code换取网页授权access_token ，较短时间 配合 refreshAccessToken使用
    # http://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html
    @classmethod
    def get_access_token_by_code(cls, code):
        '''

        :param code:
        :return:
        '''
        params = {
            "appid": cls.wx_api_config.appid,
            "secret": cls.wx_api_config.appsecret,
            "code": code,
            "grant_type": "authorization_code"
        }
        return url_requset(cls.wx_api_config._CODEACCESS_URL, params)

    # 刷新access_token, 使用getAccessTokenByCode()返回的refresh_token刷新access_token，可获得较长时间有效期
    @classmethod
    def refresh_access_token(cls, refresh_token):
        params = {
            "appid": cls.wx_api_config.appid,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        return url_requset(cls.wx_api_config._REFRESHTOKRN_URL, params)

    # 拉取用户信息(通过网页授权)
    @classmethod
    def get_snsapi_user_info(cls, access_token, openid, lang="zh_CN"):
        params = {
            "access_token": access_token,
            "openid": openid,
            "lang": lang
        }
        return url_requset(cls.wx_api_config._SNSUSER_URL, params)

    # 检验授权凭证（access_token）是否有效
    @classmethod
    def validate_access_token(cls, access_token, openid):
        params = {
            "access_token": access_token,
            "openid": openid
        }
        return url_requset(cls.wx_api_config._VALIDATE_URL, params)

    # 发送客服消息接口
    # http://mp.weixin.qq.com/wiki/11/c88c270ae8935291626538f9c64bd123.html
    @classmethod
    def send(cls, data, access_token):
        params = json.dumps(data, ensure_ascii=False)
        url = cls.wx_api_config._SEND_URL, '&access_token=', access_token
        return url_requset(url, params, "post")

    # 发送文本消息
    @classmethod
    def send_text_message(cls, openid, message, access_token):
        data = {
            "touser": openid,
            "msgtype": "text",
            "text":
                {
                    "content": message
                }
        }
        return cls.send(data, access_token)

    # 发送图文消息
    @classmethod
    def send_news(cls, openid, message, access_token):
        data = {
            "touser": openid,
            "msgtype": "news",
            "news":
                {
                    "articles": [
                        {
                            "title": "tuwen1",
                            "description": "Is Really A Happy Day",
                            "url": "URL",
                            "picurl": "PIC_URL"
                        },
                        {
                            "title": "tuwen2",
                            "description": "Is Really A Happy Day",
                            "url": "URL",
                            "picurl": "PIC_URL"
                        }
                    ]
                }
        }
        return cls.send(data, access_token)

    # 获取jsapi_tocket  http://mp.weixin.qq.com/wiki/11/74ad127cc054f6b80759c40f77ec03db.html
    @classmethod
    def jsapi_ticket(cls, access_token):
        '''
        jsapi_ticket的有效期为7200秒,需要进行缓存
        :param access_token:
        :return:
        '''
        params = {
            "access_token": access_token,
            "type": "jsapi"
        }
        return url_requset(cls.wx_api_config._JSAPI_URL, params)

    # jsapi_ticket 签名
    @classmethod
    def jsapi_sign(cls, jsapi_ticket, url):
        sign = {
            'nonceStr': cls.nonceStr(15),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': int(time.time()),
            'url': url
        }
        signature = '&'.join(['%s=%s' % (key.lower(), sign[key]) for key in sorted(sign)])
        sign["signature"] = hashlib.sha1(signature).hexdigest()
        return sign

    # 创建自定义菜单    https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
    @classmethod
    def create_menu(cls, data, access_token):
        params = json.dumps(data, ensure_ascii=False)
        url = cls.wx_api_config._SEND_URL, '&access_token=', access_token
        return url_requset(cls.wx_api_config._MENU_CREATE_URL, params, "post")

    # 删除自定义菜单    https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=ACCESS_TOKEN
    @classmethod
    def delete_menu(cls, access_token):
        params = {
            "access_token": access_token
        }
        return url_requset(cls.wx_api_config._MENU_DELETE_URL, params)
