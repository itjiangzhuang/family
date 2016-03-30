# -*- coding:utf-8 -*-
__author__ = 'jiangzhuang'
import random
import string
import xml.etree.ElementTree as ET
import requests
import sys

PY2 = sys.version_info[0] == 2

# 判断系统版本，如果2.＊版本，字符编码unicode，迭代方式，还有将字符转化为本地字符编码的to_native()方法
if PY2:
    text_type = unicode  # text_type 是全局的
    iteritems = lambda d, *args, **kwargs: d.iteritems(*args, **kwargs)


    def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None or isinstance(x, str):
            return x
        return x.encode(charset, errors)
else:
    text_type = str
    iteritems = lambda d, *args, **kwargs: iter(d.items(*args, **kwargs))


    def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None or isinstance(x, str):
            return x
        return x.decode(charset, errors)


@staticmethod
def nonceStr(length):
    '''
    获取随机字符串 （大小写 + 数字）
    :param length:  长度
    :return:
    '''
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


@staticmethod
def xmlToDict(xml):
    '''
    将xml数据转化成字典对象
    :param xml: xml参数
    :return:
    '''
    return dict((child.tag, child.text) for child in ET.fromstring(xml))


@staticmethod
def urlRequset(url, params, method):
    '''
    获取url返回参数
    :param url:  链接地址
    :param params: 参数
    :param method: 访问方式
    :return:
    '''
    if (method == "post"):
        res = requests.post(url, params=params)
    elif (method == "get"):
        res = requests.get(url, params=params)
    else:
        res = None
    return res
