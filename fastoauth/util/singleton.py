# -*- coding: utf-8 -*-
"""
@author: hubo
@project: bbb_utils
@file: singleton.py
@time: 2023/11/01
@desc: 通过@Singleton将类设置为单例模式
"""


class Singleton(object):
    """
    python版的单例模式
    使用例子
    @Singleton
    class Signle:
        def __init__(self):
            self.count = 0

        def add_count(self):
            self.count += 1
            return self.count


    print(Signle().add_count()) # 1
    print(Signle().add_count()) # 2
    """
    _INSTANCE = {}
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        instance = self._INSTANCE.get(self.cls, None)
        if not instance:
            instance = self.cls(*args, **kwargs)
            self._INSTANCE[self.cls] = instance
        return instance

    def __getattr__(self, key):
        return getattr(self.cls, key, None)


