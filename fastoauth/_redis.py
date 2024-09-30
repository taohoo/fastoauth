# -*- coding: utf-8 -*-
"""
@author: hubo
@project: bb-py
@file: _redis.py
@time: 2023/11/10 16:06
@desc:
"""
import redis
from .util.singleton import Singleton


@Singleton
class _Redis:
    def __init__(self):
        """
        初始化redis
        :param url:类似这样的格式redis://user:password@localhost:6379/db
        """
        self.r = None

    def enabled_from(self, url):
        if self.r is None and url:
            self.r = redis.from_url(url)
        return self.r is not None

    def set(self, key, value, expire_in):
        self.r.set(key, value)
        self.r.expireat(key, expire_in)

    def set_expire_in(self, key, expire_in):
        self.r.expireat(key, expire_in)

    def get(self, key):
        return self.r.get(key)

    def delete(self, key):
        self.r.delete(key)

