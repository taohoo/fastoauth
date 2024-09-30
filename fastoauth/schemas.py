# -*- coding: utf-8 -*-
"""
@author: hubo
@project: bb_fast_oauth2
@file: schemas.py
@time: 2023/11/01
@desc: oauth2请求和返回的数据模型
"""
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str    # 直接使用access_token进行刷新
    token_type: str
    expires_in: int

