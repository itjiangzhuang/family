# -*- coding:utf-8 -*-
__author__ = 'jiangzhuang'

import requests
from flask import json


def post(url, payload):
    r = requests.post(url, data=payload)
    print(r.text)


def get(url):
    r = requests.get(url)
    print(r.text)


def delete(url):
    r = requests.delete(url)
    print(r.text)


def put(url, payload):
    r = requests.put(url, data=payload)
    print(r.text)

# =======================================================================================================


def test_index():
    url = 'http://127.0.0.1:5000/wechat'
    get(url)
    pass


def test_post():
    url = 'http://127.0.0.1:5000/wechat/post'
    payload = {'id': 1, 'name': ''}
    post(url, payload)
    pass


if __name__ == '__main__':
    test_index()
    pass
